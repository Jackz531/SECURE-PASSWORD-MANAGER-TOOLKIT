import socket
import mysql.connector
import struct
import hashlib


def find_email(email):
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="DBMS_project9",
    database="spmt")
    cursor = conn.cursor()
    query="SELECT * FROM master WHERE email = %s"
    value=(email,)
    cursor.execute(query,value)
    rows=cursor.fetchall()
    conn.close()
    if len(rows)==0:
        return True
    else:
        return False

def retrieve_n(email):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="DBMS_project9",
        database="spmt")
    cursor = conn.cursor()
    query = "Select* from master where email=%s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    if result is None:
        return "Email Doesn't Exist"
    print(result)
    return result[3]


def checksql(email, pwd):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="DBMS_project9",
        database="spmt")

    cursor = conn.cursor()
    query = "SELECT * FROM master where email=%s"
    value = (email,)
    cursor.execute(query, value)
    rows = cursor.fetchall()
    cursor.close()
    password = hashlib.sha512(pwd.encode()).hexdigest()
    print(password)

    if len(rows) == 0:
        x1 = "Email Doesn't Exist"
    else:
        stored_hash = rows[0][2]
        n = rows[0][3]
        if password == stored_hash:
            cursor = conn.cursor()
            n = n - 1
            query = "Update master set n = %s where email = %s"
            cursor.execute(query, (n,email))
            conn.commit()
            query = "Update master set hash = %s where email = %s"
            cursor.execute(query, (pwd,email))
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
        password="DBMS_project9",
        database="spmt")

    cursor = conn.cursor()
    query = "insert into master(email,hash,n) values (%s,%s,%s)"
    n = 3
    value = (email, pwd, n)
    cursor.execute(query, value)
    conn.commit()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
server_socket.bind(('localhost', 5000))  # connect to the server

server_socket.listen(1)
conn, addr = server_socket.accept()

while True:
    # conn.send("True".encode())
    homebuttonclicked = ""
    homebuttonclicked = conn.recv(1024).decode()
    # print(homebuttonclicked)
    while homebuttonclicked == "login":
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
        login_status = checksql(email,pwd)
        print(login_status)
        conn.send(login_status.encode())
        if login_status == "Login Successful":
            conn.send(struct.pack('i',retrieve_n(email)))
            break
            while True:
                pass
    while homebuttonclicked == "signup":
        signupbuttonclicked = ""
        print(signupbuttonclicked)
        signupbuttonclicked = conn.recv(1024).decode()
        if signupbuttonclicked == "signup":
            email = conn.recv(1024).decode()
            print(email)
            conn.send(struct.pack('?',find_email(email)))
            validity = conn.recv(1024).decode()
            print(validity)
            if validity == "Signup successful":
                email = conn.recv(1024).decode()
                pwd = conn.recv(1024).decode()
                insert(email,pwd)
            else:
                break
        if signupbuttonclicked == "Go Back":
            break

