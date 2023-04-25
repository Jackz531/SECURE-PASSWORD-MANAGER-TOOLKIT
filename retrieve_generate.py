from tkinter import *
import tkinter.font as font
import re
import sample
import retrieve
from functools import partial

c='#A6A9AD'#green
c2='#00008B' #darkblue
c3='#DBDBDB'#grey

def retrieve():
    retrieve.home()
def generate():
    pass

def retrieve_generate():
    master1 = Toplevel()

    master1.geometry("600x450")
    master1.config(bg=c)
    master1.title("Secure password manage toolkit")

    myFont1 = font.Font(size=25)
    myFont = font.Font(size=20)
    myFont2 = font.Font(size=15)

    label11 = Label(master1, text="CHOOSE YOUR OPTION",font=myFont1,bg=c,fg="black")
    label11.place(relx=0.5,rely=0.1,anchor=CENTER)

    b1=Button(master1,text="GENERATE PASSWORD",font=myFont,padx=30,bg=c3,command=generate)
    b1.place(relx=0.5,rely=0.35,anchor=CENTER)

    b1=Button(master1,text="RETRIEVE PASSWORD",font=myFont,padx=30,bg=c3,command=retrieve)
    b1.place(relx=0.5,rely=0.5,anchor=CENTER)

    b2=Button(master1,text="Go Back",font=myFont2,padx=30,bg=c3,command=master1.destroy)
    b2.place(relx=0.5,rely=0.70,anchor=CENTER)


    master1.mainloop()