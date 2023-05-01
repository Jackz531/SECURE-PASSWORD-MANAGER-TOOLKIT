from tkinter import *
import tkinter.font as font
import re
import sample
import retrieve
import generation
from functools import partial

c='#A6A9AD'#green
c2='#00008B' #darkblue
c3='#DBDBDB'#grey

def ret(sock,masterpass):
    sock.send("retrieve".encode())
    retrieve.home(sock,masterpass)
def generate(sock,masterpass):
    sock.send("generate".encode())
    generation.gen_ui(sock,masterpass)

def destroy(sock,master1):
    sock.send("Go Back".encode())
    master1.destroy()

def retrieve_generate(sock,masterpass):
    master1 = Toplevel()

    master1.geometry("600x450")
    master1.config(bg=c)
    master1.title("Secure password manage toolkit")

    myFont1 = font.Font(size=25)
    myFont = font.Font(size=20)
    myFont2 = font.Font(size=15)

    label11 = Label(master1, text="CHOOSE YOUR OPTION",font=myFont1,bg=c,fg="black")
    label11.place(relx=0.5,rely=0.1,anchor=CENTER)

    b1=Button(master1,text="GENERATE PASSWORD",font=myFont,padx=30,bg=c3,command=lambda: generate(sock,masterpass))
    b1.place(relx=0.5,rely=0.35,anchor=CENTER)

    b1=Button(master1,text="RETRIEVE PASSWORD",font=myFont,padx=30,bg=c3,command=lambda: ret(sock,masterpass))
    b1.place(relx=0.5,rely=0.5,anchor=CENTER)

    b2=Button(master1,text="Log Out",font=myFont2,padx=30,bg=c3,command=lambda: destroy(sock,master1))
    b2.place(relx=0.5,rely=0.70,anchor=CENTER)


    master1.mainloop()