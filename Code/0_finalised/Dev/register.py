from tkinter import *
from tkinter import messagebox
import sqlite3

con=sqlite3.connect('dat/db.db')
cur=con.cursor()

root=Tk()
root.title("Register Panel")
root.geometry('355x315')
root.resizable(height=False, width=False)
root.configure(bg='#737171')
root.iconbitmap('dat/form.ico')

Label(root,bg="#b6c71c",height=220,width=1).place(x=220,y=0)#lime-yellow 1
Label(root,bg="#f59911",height=220,width=1).place(x=245,y=0)#orange 1
Label(root,bg="#cc4235",height=220,width=1).place(x=270,y=0)#red 1
Label(root,bg="#f59911",height=220,width=1).place(x=295,y=0)#orange 2
Label(root,bg="#b6c71c",height=220,width=1).place(x=320,y=0)#lime-yellow 2

Label(root,text="Create new account :",relief=RAISED,font=("helvetica",12),width=20,bg='grey',
      fg='white').place(x=21,y=15)

def GetCode():
    print("The security code returns here")

def Login():
    root.destroy()
    exec(open('login.py').read())

def Check():
    if len(pswd.get()) > 10 or len(cnfrm.get()) > 10 or len(usrnme.get()) > 10:
        messagebox.showerror("Register Panel","Entries exceed limit")
    elif pswd.get() != cnfrm.get():
        messagebox.showerror("Register Panel","Passwords do not match")
    else:
        GetCode()

def Help():
    messagebox.showinfo("Register Help","Username, Password and Confirm Password entries must be less than 10 characters long")

def View1():
    if pswd.cget('show')=='':
        pswd.config(show='*')
    else:
        pswd.config(show='')

def View2():
    if cnfrm.cget('show')=='':
        cnfrm.config(show='*')
    else:
        cnfrm.config(show='')

Label(root,text="Username:",bg='grey',fg='white').place(x=21,y=50)#username
usrnme=Entry(root,width=30)
usrnme.place(x=21,y=70)

Label(root,text="Password:",bg='grey',fg='white').place(x=21,y=110)#password
pswd=Entry(root,width=25,show='*')
pswd.place(x=21,y=130)

Label(root,text="Confirm Password:",bg='grey',fg='white').place(x=21,y=170)#confirm password
cnfrm=Entry(root,width=25,show='*')
cnfrm.place(x=21,y=190)

Label(root,text="",bg='grey',width=20).place(x=40,y=230)
Label(root,text="Security Code:",bg='grey',fg='white').place(x=21,y=230)#security code
#Label on screen with randomly generated security code matching new user account, 4 digits
Label(root,text="0 0 0 0",font=("",9),bg='grey',fg='white',width=10).place(x=130,y=230)

Button(root,text="Create Account",height=1,width=13,bg="grey",fg="white",command=Check).place(x=21,y=270)
#creates account by appending to database


Button(root,text="Login",height=1,width=6,bg="grey",fg="white",command=Login).place(x=125,y=270)

ques_img=PhotoImage(file='dat/question_mark.png')
ques=Button(root,text="",command=Help)
ques.config(image=ques_img)
ques.place(x=180,y=270)

see1_img=PhotoImage(file='dat/view.png')
see1=Button(root,text="",command=View1)
see1.config(image=see1_img)
see1.place(x=180,y=130)

see2_img=PhotoImage(file='dat/view.png')
see2=Button(root,text="",command=View2)
see2.config(image=see2_img)
see2.place(x=180,y=190)

root.mainloop()
