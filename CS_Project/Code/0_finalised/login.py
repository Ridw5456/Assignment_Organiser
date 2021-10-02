from tkinter import *
from tkinter import messagebox
import sqlite3
import time as t
import datetime as dt

con=sqlite3.connect('dat/db.db')
cur=con.cursor()

root=Tk()
root.title("Login Panel")
root.geometry('355x220')
root.resizable(height=False, width=False)
root.configure(bg='#737171')
root.iconbitmap('dat/lock.ico')

Label(root,text="Login Credentials :",relief=RAISED,font=("helvetica",15),width=16,bg='grey',
      fg='white').place(x=21,y=15)

Label(root,bg="#b6c71c",height=220,width=1).place(x=220,y=0)#lime-yellow 1
Label(root,bg="#f59911",height=220,width=1).place(x=245,y=0)#orange 1
Label(root,bg="#cc4235",height=220,width=1).place(x=270,y=0)#red 1
Label(root,bg="#f59911",height=220,width=1).place(x=295,y=0)#orange 2
Label(root,bg="#b6c71c",height=220,width=1).place(x=320,y=0)#lime-yellow 2

def Register():
    root.destroy()
    exec(open('register.py').read())

def View():
    if pswd.cget('show')=='':
        pswd.config(show='*')
    else:
        pswd.config(show='')

def AuthCred():
    UName=usrnme.get()
    PWord=pswd.get()
    cur.execute((f"SELECT username FROM users WHERE username='{UName}' AND password='{PWord}';"))
    if not cur.fetchall():
        messagebox.showerror("Login Panel","Invalid credentials")
    else:
        root.destroy()
        exec(open('main.py').read())

def TogglePW():
    if pswd.cget('show')=='':
        pswd.config(show='*')

def Digitalclock():
   text_input=t.strftime("%H:%M:%S")
   clock.config(text=text_input)
   clock.after(200,Digitalclock)

Label(root,text="Username:",bg="grey",fg="white").place(x=20,y=55)
usrnme=Entry(root,width=30)
usrnme.place(x=20,y=75)

Label(root, text="Password:",bg="grey",fg="white").place(x=20,y=115)
pswd=Entry(root,width=25,show='*')
pswd.place(x=20,y=135)

Button(root,text="Register",width=10,height=1,bg="grey",fg="white",
        command=Register).place(x=20,y=175)

Button(root,text="Login",width=10,height=1,bg="grey",fg="white",
        command=AuthCred).place(x=125,y=175)

Label(root,text=f"{dt.datetime.now():%a %b%d %Y}",fg="white",bg="grey",font=("",11),width=12,
      height=1).place(x=220,y=50)

clock=Label(root,font=("helvetica",15,'bold'),bg="grey",fg="white",width=9,height=1)
clock.place(x=220,y=15)
Digitalclock()

see_img=PhotoImage(file='dat/view.png')
see=Button(root,text="",command=View)
see.config(image=see_img)
see.place(x=180,y=135)

root.mainloop()
