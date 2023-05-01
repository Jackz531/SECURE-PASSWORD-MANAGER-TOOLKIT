import hashlib
from tkinter import *
import tkinter.font as font
import re
import sample
from functools import partial
import socket
import mysql.connector
import hashlib
import decryption
import encryption
import struct
import retrieve_generate

c='#A6A9AD'#green
c2='#00008B' #darkblue
c3='#DBDBDB'#grey

def change_key(password,masterpassold,sock):
    # email=""  #get this
    # conn = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password="",
    #     database="spmt")
    # cursor = conn.cursor()
    # query="SELECT * FROM passwords inner join master where master.email=%s and master.email=passwords.email"
    # value = (email,)
    # cursor.execute(query, value)
    # rows = cursor.fetchall()

    key=masterpassold[0:8] #idont have these
    key=key.encode().hex()
    key2=password[0:8]
    key2=key2.encode().hex()

    l = struct.unpack('i',sock.recv(struct.calcsize('i')))[0]

    for i in range(l):
        dbpwd=sock.recv(1024).decode()
        s = encryption.encryption("abcdefgh".encode().hex(),key)
        plain=decryption.decryption(dbpwd)
        encpwd=encryption.encryption(plain,key2)
        print("original="+dbpwd+" plain="+plain+" enc="+encpwd)
        sock.send(encpwd.encode())


def enter_details(pwd,sock,oldpass):
    #print(email,pwd)
    #sock.send(email.encode())
    password=pwd
    for i in range(3):
        pwd = hashlib.sha512(pwd.encode()).hexdigest()
    sock.send(pwd.encode())
    #sock.send(pwd.encode())
    # sample.insert(email,pwd)

    change_key(password,oldpass,sock)

def removemessage(label):
    label.destroy()
    
def printmessage(x,color,master1):
    inv=Label(master1, text=x,font=font.Font(size=15),bg=c,foreground=color)
    inv.place(relx=0.5,rely=0.9,anchor=CENTER)
    master1.after(2000,removemessage,inv)
   
def check_password_strength(e2,e3,master1,sock,pwd):
    password=e2.get()
    conf_pwd=e3.get()
    min_length = 8
    has_uppercase = False
    has_lowercase = False
    has_digit = False
    has_special = False
    if(password!=conf_pwd):
        return "passwords doesnt match"
    
    special_chars = '!@#$%^&*()_-+={}[]\\|:;"<>,.?/'

    if len(password) < min_length:
        return "Password is too short."

    for char in password:
        if char.isupper():
            has_uppercase = True
        elif char.islower():
            has_lowercase = True
        elif char.isdigit():
            has_digit = True
        elif char in special_chars:
            has_special = True
    
    if has_uppercase and has_lowercase and has_digit and has_special:
        printmessage("Successful","black",master1)
        enter_details(password,sock,pwd)
        master1.destroy()
        retrieve_generate.retrieve_generate(sock, password)
    else:
        printmessage("Weak password","red",master1)

def destroy(sock,master1):
    #sock.send("Go Back".encode())
    master1.destroy()


def resignup(sock,password):
    master1 = Toplevel() #use toplevel when u join

    master1.geometry("600x450")
    master1.config(bg=c)
    master1.title("Secure password manage toolkit")

    myFont1 = font.Font(size=25)
    myFont = font.Font(size=15)
    myFont2 = font.Font(size=13)

    label11 = Label(master1, text="RESTORE PASSWORD",font=myFont1,bg=c,fg="black")
    label11.place(relx=0.5,rely=0.1,anchor=CENTER)

    label13 = Label(master1, text="Enter your new password",font=myFont,bg=c,fg="black")
    label13.place(relx=0.5,rely=0.45,anchor=CENTER)

    e2=Entry(master1,width=40,font=myFont2,show='*',bg=c3,fg="black")
    e2.place(relx=0.5,rely=0.5,anchor=CENTER)

    label14 = Label(master1, text="Re-enter new password",font=myFont,bg=c,fg="black")
    label14.place(relx=0.5,rely=0.60,anchor=CENTER)
    e3=Entry(master1,width=40,font=myFont2,show='*',bg=c3,fg="black")
    e3.place(relx=0.5,rely=0.65,anchor=CENTER)

    b1=Button(master1,text="Re-Sign-Up",font=myFont,padx=30,bg=c3,command=partial(check_password_strength,e2,e3,master1,sock,password))
    b1.place(relx=0.5,rely=0.8,anchor=CENTER)
    
    # b2=Button(master1,text="Go Back",font=myFont,padx=30,bg=c3,command=lambda: destroy(sock,master1))
    # b2.place(relx=0.5,rely=0.90,anchor=CENTER)
    
    master1.mainloop()

# resignup(0)