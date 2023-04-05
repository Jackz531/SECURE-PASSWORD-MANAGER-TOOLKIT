from tkinter import *
import tkinter.font as font
import sample
import signup

#c='#ABFFA4' green
#c='#FFB675' cream
c='#A6A9AD'  
#c='#34353D'
c2='#DBDBDB' 
c3='#DBDBDB' 


def removemessage(label):
    label.destroy()

def printmessage(x,color):
    inv=Label(master, text=x,font=myFont,bg=c,foreground=color)
    inv.place(relx=0.5,rely=0.6,anchor=CENTER)
    master.after(2000, removemessage, inv)

def takedetails():
    email=e1.get()
    pwd=e2.get()
    x=sample.validate(email,pwd)
    printmessage(x,'red')

def go():
    signup.signup()

if __name__== '__main__':
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

    b1=Button(master,text="Login",font=myFont,padx=30,bg=c2,command=takedetails,fg='black')
    b1.place(relx=0.5,rely=0.72,anchor=CENTER)

    b1=Button(master,text="Sign Up",font=myFont,padx=30,bg=c2,command=go,fg='black')
    b1.place(relx=0.5,rely=0.85,anchor=CENTER)

    master.mainloop()
