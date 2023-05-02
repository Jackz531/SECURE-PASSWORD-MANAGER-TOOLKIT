import socket
import mysql.connector
import struct
import hashlib
import encryption
import decryption


def find_email(email):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="spmt")
    cursor = conn.cursor()
    query = "SELECT * FROM master WHERE email = %s"
    value = (email,)
    cursor.execute(query, value)
    rows = cursor.fetchall()
    conn.close()
    if len(rows) == 0:
        return True
    else:
        return False


def retrieve_n(email):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="spmt")
    cursor = conn.cursor()
    query = "Select* from master where email=%s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    if result is None:
        return "Email Doesn't Exist"
    # print(result)
    return result[2]


def checksql(email, pwd):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="spmt")

    cursor = conn.cursor()
    query = "SELECT * FROM master where email=%s"
    value = (email,)
    cursor.execute(query, value)
    rows = cursor.fetchall()
    cursor.close()
    password = hashlib.sha512(pwd.encode()).hexdigest()

    if len(rows) == 0:
        x1 = "Email Doesn't Exist"
    else:
        stored_hash = rows[0][1]
        n = rows[0][2]
        if password == stored_hash:
            cursor = conn.cursor()
            n = n - 1
            query = "Update master set n = %s where email = %s"
            cursor.execute(query, (n, email))
            conn.commit()
            query = "Update master set hash = %s where email = %s"
            cursor.execute(query, (pwd, email))
            conn.commit()
            conn.close()
            return "Login Successful"
        else:
            return "Incorrect Password"

    conn.close()

    return x1


def insert(email, pwd):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="spmt")

    cursor = conn.cursor()
    query = "insert into master(email,hash,n) values (%s,%s,%s)"
    n = 3
    value = (email, pwd, n)
    cursor.execute(query, value)
    conn.commit()


def change_key(password, email, sock):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="spmt")
    cursor = conn.cursor()
    # query="SELECT * FROM passwords inner join master where master.email=%s and master.email=passwords.email"
    query = "SELECT * FROM passwords where email=%s"
    value = (email,)
    cursor.execute(query, value)
    rows = cursor.fetchall()

    # key=masterpassold[0:8]
    # key=key.encode().hex()
    # key2=password[0:8]
    # key2=key2.encode().hex()

    sock.send(struct.pack('i', len(rows)))
    for i in rows:
        sock.send(i[3].encode())
        encpwd = sock.recv(1024).decode()
        print(i[3], encpwd)
        query2 = "update passwords set pwd = %s where email=%s and domain=%s and user_id=%s"
        values = (encpwd, email, i[2], i[1])
        cursor.execute(query2, values)

    query = "Update master set hash = %s, n = 3 where email=%s"
    cursor.execute(query, (password, email))
    conn.commit()


def generate(master_email, sock):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="spmt")
    domainname = sock.recv(1024).decode()
    sock.send("x".encode())
    userid = sock.recv(1024).decode()
    sock.send("x".encode())
    encpwd = sock.recv(1024).decode()
    print(domainname, userid, encpwd)
    cursor = conn.cursor()

    q = "insert into passwords values (%s,%s,%s,%s)"
    value = (master_email, userid, domainname, encpwd)
    cursor.execute(q, value)
    conn.commit()


def get_domains(email, sock):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="spmt")

    # create cursor to execute SQL queries
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT distinct domain FROM passwords WHERE email = %s", (email,))
    domain_names = mycursor.fetchall()
    domain_names = [x[0] for x in domain_names]
    n = len(domain_names)
    sock.send(struct.pack('i', n))
    x = sock.recv(1024).decode()
    for i in range(n):
        sock.send(domain_names[i].encode())
        x = sock.recv(1024).decode()


def get_user_ids(domain_name, sock, email):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="spmt")

    # create cursor to execute SQL queries
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT user_id FROM passwords WHERE domain = %s and email=%s", (domain_name, email))
    user_ids = mycursor.fetchall()
    user_ids = [x[0] for x in user_ids]
    n = len(user_ids)
    sock.send(struct.pack('i', n))
    x = sock.recv(1024).decode()
    for i in range(n):
        sock.send(user_ids[i].encode())
        x = sock.recv(1024).decode()


def getpassword(dname, user_id, sock):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="spmt")

    cursor = conn.cursor()
    q = "SELECT * FROM passwords WHERE domain= %s AND user_id = %s"
    values = (dname, user_id)
    cursor.execute(q, values)
    rows = cursor.fetchall()
    sock.send(rows[0][3].encode())


server_socket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)  # instantiate
server_socket.bind(('localhost', 5000))  # connect to the server

server_socket.listen(1)
conn, addr = server_socket.accept()


while True:
    # conn.send("True".encode())
    homebuttonclicked = ""
    homebuttonclicked = conn.recv(1024).decode()
    # print(homebuttonclicked)
    flag = 0
    while homebuttonclicked == "login":
        if flag == 1:
            flag = 0
            break
        email = conn.recv(1024).decode()
        n = retrieve_n(email)
        if n != "Email Doesn't Exist":
            conn.send("int".encode())
            conn.send(struct.pack('i', retrieve_n(email)))
        else:
            conn.send("string".encode())
            conn.send(n.encode())
            break
        pwd = conn.recv(1024).decode()
        login_status = checksql(email, pwd)
        conn.send(login_status.encode())
        if login_status == "Login Successful":
            n = retrieve_n(email)
            conn.send(struct.pack('i', n))
            if n == 1:
                newpass = conn.recv(1024).decode()
                change_key(newpass, email, conn)
            while True:
                genret = ""
                genret = conn.recv(1024).decode()
                print("genret="+genret)
                while genret == "generate":
                    gen = ""
                    gen = conn.recv(1024).decode()
                    print("gen="+gen)
                    if gen == "generate":
                        generate(email, conn)
                    elif gen == "Go Back":
                        break
                if genret == "retrieve":
                    get_domains(email, conn)
                    while True:
                        domain_name = conn.recv(1024).decode()
                        print("domain name="+domain_name)
                        if domain_name == "Go Back":
                            break
                        get_user_ids(domain_name, conn, email)
                        user_id = conn.recv(1024).decode()
                        print("user id=" + user_id)
                        if user_id == "Go Back":
                            break
                        ret = ""
                        ret = conn.recv(1024).decode()
                        print("ret="+ret)
                        if ret == "retrieve":
                            getpassword(domain_name, user_id, conn)
                        elif ret == "Go Back":
                            break
                if genret == "Go Back":
                    flag = 1
                    break
        else:
            break
    while homebuttonclicked == "signup":
        signupbuttonclicked = ""
        signupbuttonclicked = conn.recv(1024).decode()
        print(signupbuttonclicked)
        if signupbuttonclicked == "signup":
            email = conn.recv(1024).decode()
            print(email)
            conn.send(struct.pack('?', find_email(email)))
            validity = conn.recv(1024).decode()
            print(validity)
            if validity == "Signup successful":
                email = conn.recv(1024).decode()
                pwd = conn.recv(1024).decode()
                insert(email, pwd)
            else:
                pass
        if signupbuttonclicked == "Go Back":
            break
