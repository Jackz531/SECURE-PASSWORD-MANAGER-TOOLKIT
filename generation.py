from tkinter import *
import tkinter.font as font
import mysql.connector
import string
import random
import encryption
from functools import partial



def gen_ui(sock,masterpass):
    c = '#A6A9AD'
    c2 = '#DBDBDB'
    c3 = '#DBDBDB'

    def generate_password(length):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(length))
        return password

    def genfunc(master, e1, e2, sock, masterpass):
        sock.send("generate".encode())
        pwd = generate_password(8)
        print(pwd)
        # x=pwd
        # x=x.encode().hex()
        # print(x)
        key = masterpass[0:8]

        encpwd = encryption.encryption(pwd.encode().hex(), key.encode().hex())
        domainname = e1.get()
        userid = e2.get()
        sock.send(domainname.encode())
        x = sock.recv(1024).decode()
        sock.send(userid.encode())
        x = sock.recv(1024).decode()
        sock.send(encpwd.encode())
        # master_email="teju@gmail.com"  #get it

        # conn = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     password="",
        #     database="spmt")

        # cursor = conn.cursor()
        # q="insert into passwords values (%s,%s,%s,%s)"
        # value=(master_email,userid,domainname,encpwd)
        # cursor.execute(q, value)
        # conn.commit()

        labelx = Label(master, text="New Password: " + pwd, font=myFont, bg=c2, fg='black', height=2, width=30)
        labelx.place(relx=0.5, rely=0.65, anchor=CENTER)

    def destroy(sock, master):
        sock.send("Go Back".encode())
        master.destroy()

    master = Tk()

    master.geometry("600x450")
    master.config(bg=c)
    master.title("Secure password manage toolkit")

    myFont1 = font.Font(size=25)
    myFont = font.Font(size=15)
    myFont2 = font.Font(size=13)

    label11 = Label(master, text="SECURE PASSWORD MANAGER",font=myFont1,bg=c,fg='black')
    label11.place(relx=0.5,rely=0.1,anchor=CENTER)

    label12 = Label(master, text="Enter Domain Name",font=myFont,bg=c,fg='black')
    label12.place(relx=0.5,rely=0.3,anchor=CENTER)
    e1=Entry(master,width=40,font=myFont2,bg=c3,fg='black')
    e1.place(relx=0.5,rely=0.35,anchor=CENTER)

    label13 = Label(master, text="Enter User_ID",font=myFont,bg=c,fg='black')
    label13.place(relx=0.5,rely=0.45,anchor=CENTER)
    e2=Entry(master,width=40,font=myFont2,bg=c3,fg='black')
    e2.place(relx=0.5,rely=0.5,anchor=CENTER)

    b1=Button(master, text="Generate Password", font=myFont, padx=30, bg=c2, fg='black', command=lambda: genfunc(master,e1,e2,sock,masterpass))
    b1.place(relx=0.5,rely=0.65,anchor=CENTER)

    b2=Button(master, text="Go back", font=myFont, padx=30, bg=c2, fg='black',command=lambda: destroy(sock,master))
    b2.place(relx=0.5,rely=0.85,anchor=CENTER)

    master.mainloop()