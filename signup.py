from tkinter import *
import tkinter.font as font
import re
import sample
from functools import partial

c='#A6A9AD'#green
c2='#00008B' #darkblue
c3='#DBDBDB'#grey

def enter_details(email,pwd):
    print(email,pwd)
    sample.insert(email,pwd)

def removemessage(label):
    label.destroy()
    
def printmessage(x,color,master1):
    inv=Label(master1, text=x,font=font.Font(size=15),bg=c,foreground=color)
    inv.place(relx=0.5,rely=0.9,anchor=CENTER)
    master1.after(2000,removemessage,inv)

def check(x):
     pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
     match = re.search(pattern,x)
     if match:
        return True
     else:
        return False
     
#primary funcion for checking email id
def check_email(e1,e2,e3,master1):
    email=e1.get()
    x=check(email)
    z=sample.find_email(email)
    if x==True and z==True:  
         y=check_password_strength(e2,e3)
         if(y!=None):
            printmessage(y,'red',master1)
            # e1.delete(0,END)
            e2.delete(0,END)
            e3.delete(0,END)
         else: 
          z="Signup successfull"
          printmessage(z,'red',master1)  
          enter_details(email,e2.get())
    elif(z==False):
          y="You already have an account"
          printmessage(y,'red',master1)
          return
    else:
        y="Enter a valid email-id"
        printmessage(y,'red',master1)
   
def check_password_strength(e2,e3):
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
        return 
    elif has_uppercase and has_lowercase and has_digit:
        return 
    else:
        return "Weak password."


def signup():
    master1 = Toplevel()

    master1.geometry("600x450")
    master1.config(bg=c)
    master1.title("Secure password manage toolkit")

    myFont1 = font.Font(size=25)
    myFont = font.Font(size=15)
    myFont2 = font.Font(size=13)

    label11 = Label(master1, text="SIGNUP PAGE",font=myFont1,bg=c,fg="black")
    label11.place(relx=0.5,rely=0.1,anchor=CENTER)

    label12 = Label(master1,text="Enter your email id",font=myFont,bg=c,fg="black")
    label12.place(relx=0.5,rely=0.3,anchor=CENTER)

    e1=Entry(master1,width=40,font=myFont2,bg=c3,fg='black',)
    e1.place(relx=0.5,rely=0.35,anchor=CENTER)

    label13 = Label(master1, text="Enter your new password",font=myFont,bg=c,fg="black")
    label13.place(relx=0.5,rely=0.45,anchor=CENTER)

    e2=Entry(master1,width=40,font=myFont2,show='*',bg=c3,fg="black")
    e2.place(relx=0.5,rely=0.5,anchor=CENTER)

    label14 = Label(master1, text="Re-enter new password",font=myFont,bg=c,fg="black")
    label14.place(relx=0.5,rely=0.60,anchor=CENTER)
    e3=Entry(master1,width=40,font=myFont2,show='*',bg=c3,fg="black")
    e3.place(relx=0.5,rely=0.65,anchor=CENTER)

    b1=Button(master1,text="Sign Up",font=myFont,padx=30,bg=c3,command=partial(check_email,e1,e2,e3,master1))
    b1.place(relx=0.5,rely=0.8,anchor=CENTER)

    master1.mainloop()