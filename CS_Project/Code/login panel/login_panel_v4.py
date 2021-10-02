from tkinter import *
import time
import datetime as dt
import sqlite3
from tkinter import messagebox

con=sqlite3.connect('C:/Users/ridwa/Documents/CS_Project/Code/database/db.db')
cur=con.cursor()

root=Tk()
root.title("Login Screen")
root.geometry('355x220')
root.resizable(height=False, width=False)
root.configure(bg='#737171')
root.iconbitmap('lock.ico')

Label(root,text="Login Credentials:",relief=RAISED,font=("helvetica",15),
      width=16,bg='grey',fg='white').place(x=21,y=15)

def AuthCred():
    UName=usrnme_inp.get()
    PWord=pw_inp.get()
    ### Search for UName and PWord from database ###
    
    if UName == "" or PWord == "":
        messagebox.showerror("Login Screen","Please enter both Username and Password")
    elif len(UName)>10:
        messagebox.showerror("Login Screen","Please enter a valid username")

Label(root,text="Username:",bg="grey",fg="white").place(x=20,y=55)
usrnme_inp=Entry(root,width=30)
usrnme_inp.place(x=20,y=75)

Label(root, text="Password:",bg="grey",fg="white").place(x=20,y=115)
pw_inp=Entry(root,width=30,show='*')
pw_inp.place(x=20,y=135)

usr_reg=Button(root,text="Register",width=10,height=1,bg="grey",fg="white"
               ).place(x=20,y=175)

usr_log=Button(root,text="Login",width=10,height=1,bg="grey",fg="white",
               command=AuthCred).place(x=125,y=175)

Label(root,text=f"{dt.datetime.now():%a %b%d %Y}",fg="white",
               bg="grey",font=("",11),width=12,height=1).place(x=220,y=50)

clock=Label(root,font=("helvetica",15,'bold'),bg="grey",fg="white",
              width=9,height=1,relief=RAISED)
clock.place(x=220,y=15)

def Digitalclock():
   text_input=time.strftime("%H:%M:%S")
   clock.config(text=text_input)
   clock.after(200,Digitalclock)

Digitalclock()
