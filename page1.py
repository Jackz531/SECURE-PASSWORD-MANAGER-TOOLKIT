import struct
from tkinter import *
import tkinter.font as font
import sample
import signup
import socket


#c='#ABFFA4' green
#c='#FFB675' cream
c='#A6A9AD'  
#c='#34353D'
c2='#DBDBDB' 
c3='#DBDBDB' 

def home(sock):

    def removemessage(label):
        label.destroy()

    def printmessage(x, color):
        inv = Label(master, text=x, font=myFont, bg=c, foreground=color)
        inv.place(relx=0.5, rely=0.6, anchor=CENTER)
        master.after(2000, removemessage, inv)

    def takedetails(sock):
        sock.send("login".encode())
        email = e1.get()
        pwd = e2.get()
        # return ["login",email,pwd]
        x = sample.validate(sock,email, pwd)
        printmessage(x, 'red')
        if x == "Login Successful":
            n = struct.unpack('i',sock.recv(struct.calcsize('i')))[0]
            if n == 1:
                print("Time to change password")


    def go(sock):
        sock.send("signup".encode())
        signup.signup(sock)

    master = Tk()

    master.geometry("600x450")
    master.config(bg=c)
    master.title("Secure password manage toolkit")

    myFont1 = font.Font(size=25)
    myFont = font.Font(size=15)
    myFont2 = font.Font(size=13)

    label11 = Label(master, text="SECURE PASSWORD MANAGER",font=myFont1,bg=c,fg='black')
    label11.place(relx=0.5,rely=0.1,anchor=CENTER)

    label12 = Label(master, text="Enter email",font=myFont,bg=c,fg='black')
    label12.place(relx=0.5,rely=0.3,anchor=CENTER)
    e1=Entry(master,width=40,font=myFont2,bg=c3,fg='black')
    e1.place(relx=0.5,rely=0.35,anchor=CENTER)

    label13 = Label(master, text="Enter password",font=myFont,bg=c,fg='black')
    label13.place(relx=0.5,rely=0.45,anchor=CENTER)
    e2=Entry(master,width=40,font=myFont2,show='*',bg=c3,fg='black')
    e2.place(relx=0.5,rely=0.5,anchor=CENTER)

    b1=Button(master, text="Login", font=myFont, padx=30, bg=c2, command=lambda: takedetails(sock), fg='black')
    b1.place(relx=0.5,rely=0.72,anchor=CENTER)

    b1=Button(master,text="Sign Up",font=myFont,padx=30,bg=c2,command=lambda: go(sock),fg='black')
    b1.place(relx=0.5,rely=0.85,anchor=CENTER)

    master.mainloop()
