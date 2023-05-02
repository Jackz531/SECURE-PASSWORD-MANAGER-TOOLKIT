import mysql.connector
import sample
import tkinter.font as font
from tkinter import *
from tkinter import ttk

dname = ""
user_id = ""

c = '#A6A9AD'  # green
c2 = '#00008B'  # darkblue
c3 = '#DBDBDB'  # grey
# create connection to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="spmt")

# create cursor to execute SQL queries
mycursor = mydb.cursor()
# retrieve domain names from database
mycursor.execute("SELECT DISTINCT domain FROM passwords")
domain_names = mycursor.fetchall()
domain_names = [x[0] for x in domain_names]


def printmessage(x,color):
    print(x)
    inv=Label(root,text=x,font=font.Font(size=15),bg=c,fg=color)
    inv.place(relx=0.5,rely=0.9,anchor=CENTER)


def getpassword():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="spmt")
    
    cursor = conn.cursor()
    q = "SELECT * FROM passwords WHERE domain= %s AND user_id = %s"
    values = (dname,user_id)
    cursor.execute(q,values)
    rows = cursor.fetchall()
    printmessage(rows[0][3],'red')


# define function to retrieve user ids based on selected domain name

def get_domains(email):
    mycursor.execute(
        "SELECT distinct domain FROM passwords WHERE email = %s", (email,))
    domain_names = mycursor.fetchall()
    domain_names = [x[0] for x in domain_names]
    domain_name_dropdown.config(values=domain_names)
    
def get_user_ids(domain_name):
    global dname
    dname = domain_name
    mycursor.execute(
        "SELECT user_id FROM passwords WHERE domain = %s", (domain_name,))
    user_ids = mycursor.fetchall()
    user_ids = [x[0] for x in user_ids]
    user_id_dropdown.config(values=user_ids)

def get_userid(userid):
   global user_id
   user_id=userid



if __name__ == '__main__':
    global root
    root = Tk()
    root.geometry("600x450")
    root.config(bg=c)
    root.title("Secure password manage toolkit")
    # root.title("Retrieve Password")
    myFont1 = font.Font(size=25)
    myFont = font.Font(size=20)
    myFont2 = font.Font(size=18)

    label11 = Label(root, text="RETRIEVE PASSWORD",
                    font=myFont1, bg=c, fg="black")
    label11.place(relx=0.5, rely=0.1, anchor=CENTER)

    # create label and dropdown for domain name
    domain_name_label = Label(
        root, text="Domain Name:", font=myFont, bg=c, fg="black")
    domain_name_label.place(relx=0.5, rely=0.27, anchor=CENTER)

    domain_name_var = StringVar()

    domain_name_dropdown = ttk.Combobox(
        root, textvariable=domain_name_var, values=domain_names, state="readonly", width=40, font=myFont2)
    domain_name_dropdown.place(relx=0.5, rely=0.35, anchor=CENTER)

    domain_name_var.trace_add("write", lambda name, index, mode,
                              domain_name_var=domain_name_var: get_user_ids(domain_name_var.get()))
    # create label and dropdown for user id
    user_id_label = Label(root, text="User ID:", font=myFont, bg=c, fg="black")
    user_id_label.place(relx=0.5, rely=0.5, anchor=CENTER)
    user_id_var = StringVar()
    user_id_dropdown = ttk.Combobox(
        root, textvariable=user_id_var, state="readonly", width=40, font=myFont2)
    user_id_dropdown.place(relx=0.5, rely=0.58, anchor=CENTER)
    user_id_var.trace_add("write", lambda name, index, mode,
                          user_id_var=user_id_var: get_userid(user_id_var.get()))

    # create button to retrieve password
    retrieve_button = Button(root, text="Retrieve Password",
                             font=myFont2, padx=30, bg=c2, fg='black', command=getpassword)
    retrieve_button.place(relx=0.5, rely=0.72, anchor=CENTER)

    root.mainloop()
