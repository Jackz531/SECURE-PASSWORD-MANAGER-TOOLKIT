import mysql.connector
import hashlib
import socket
import struct

def insert(email,pwd):

    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="spmt")
    
    cursor = conn.cursor()
    query="insert into master values (%s,%s,%s,%s)"
    hash=pwd
    n=3
    value = (2,email,hash,n)
    cursor.execute(query, value)
    conn.commit()

def validate_pwd(pwd,stored_hash,n):
    hash_object = hashlib.sha512()


def checksql(email,pwd):

    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="spmt")

    cursor = conn.cursor()
    query="SELECT * FROM master where email=%s"
    value = (email,)
    cursor.execute(query, value)
    rows = cursor.fetchall()

    if len(rows)==0:
        x1 = "Email Doesn't Exist"
    else: 
        stored_hash=rows[0][2]
        n=rows[0][3]
        validate_pwd(pwd,stored_hash,n)
        x1 = "ok"

    cursor.close()
    conn.close()

    return x1


def find_email(email):
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
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
    

def validate(sock, email,pwd):
    if email=="" or pwd=="":
        return "Enter credentials properly"
    else:
        sock.send(email.encode())
        typen = sock.recv(1024).decode()
        if typen == 'int':
            n = struct.unpack('i',sock.recv(struct.calcsize('i')))[0]
        else:
            n = sock.recv(1024).decode()
            return n
        for i in range(1,n):
            print(pwd)
            pwd = hashlib.sha512(pwd.encode()).hexdigest()
        print(pwd)
        sock.send(pwd.encode())
        login_status = sock.recv(1024).decode()
        return login_status

