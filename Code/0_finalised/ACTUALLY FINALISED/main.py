from tkinter import *
import time
import datetime as dt
import sqlite3
from tkinter import messagebox
import threading
import random
from PIL import ImageTk, Image

con=sqlite3.connect('dat/db.db')
cur=con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS
users(user_id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT,
security_code TEXT);""")

cur.execute("""CREATE TABLE IF NOT EXISTS
sessions(session_id INTEGER PRIMARY KEY AUTOINCREMENT,
start_time TEXT,
end_time TEXT,
user_id INTEGER,
FOREIGN KEY(user_id) REFERENCES users(user_id));""")

cur.execute("""CREATE TABLE IF NOT EXISTS
timetables(timetable_id INTEGER PRIMARY KEY AUTOINCREMENT,
path TEXT,
user_id INTEGER,
FOREIGN KEY(user_id) REFERENCES users(user_id));""")

cur.execute("""CREATE TABLE IF NOT EXISTS
scores(score_id INTEGER PRIMARY KEY,
score INTEGER,
session_id INTEGER,
user_id INTEGER,
FOREIGN KEY(session_id) REFERENCES sessions(session_id),
FOREIGN KEY(user_id) REFERENCES users(user_id));""")

con.commit()

class main():
    def __init__(self):
        self.root=Tk()
        self.root.title("Assignment Organiser")
        self.root.geometry('1400x700')
        self.root.resizable(height=False,width=False)
        self.root.configure(bg='#6B8282')
        self.root.iconbitmap('dat/notebook.ico')
        
        Label(self.root,bg="#EB998E",height=70,width=7).place(x=0,y=0)
        
        logout_img=PhotoImage('dat/logout.png')
        

#DO NOT UNDO """
    class login():
        def __init__(self):
            self.root=Tk()
            self.root.title("Login Panel")
            self.root.geometry('355x220')
            self.root.resizable(height=False, width=False)
            self.root.configure(bg='#737171')
            self.root.iconbitmap('dat/lock.ico')

            Label(self.root,text="Login Credentials :",relief=RAISED,font=("helvetica",15),width=16,bg='grey',
                fg='white').place(x=21,y=15)

            Label(self.root,bg="#b6c71c",height=22,width=1).place(x=220,y=0)#lime-yellow 1
            Label(self.root,bg="#f59911",height=22,width=1).place(x=245,y=0)#orange 1
            Label(self.root,bg="#cc4235",height=22,width=1).place(x=270,y=0)#red 1
            Label(self.root,bg="#f59911",height=22,width=1).place(x=295,y=0)#orange 2
            Label(self.root,bg="#b6c71c",height=22,width=1).place(x=320,y=0)#lime-yellow 2
            self.clock=Label(self.root,font=("helvetica",15,'bold'),bg="grey",fg="white",width=9,height=1)
            self.clock.place(x=220,y=15)

            Label(self.root,text="Username:",bg="grey",fg="white").place(x=20,y=55)
            self.usrnme=Entry(self.root,width=30)
            self.usrnme.place(x=20,y=75)

            Label(self.root, text="Password:",bg="grey",fg="white").place(x=20,y=115)
            self.pswd=Entry(self.root,width=25,show='*')
            self.pswd.place(x=20,y=135)

            Button(self.root,text="Register",width=10,height=1,bg="grey",fg="white",
                    command=self.Register).place(x=20,y=175)

            Button(self.root,text="Login",width=10,height=1,bg="grey",fg="white",
                    command=self.AuthCred).place(x=125,y=175)

            Label(self.root,text=f"{dt.datetime.now():%a %b%d %Y}",fg="white",bg="grey",font=("",11),width=12,
                height=1).place(x=220,y=50)

            see_img=PhotoImage(file='dat/view.png')
            see=Button(self.root,text="",command=self.ViewEyeLogin,image=see_img)
            see.place(x=180,y=135)

            self.DigClockLogin()
            self.root.mainloop()

        def Register(self):
            self.root.destroy()
            main.register()

        def ViewEyeLogin(self):
            if self.pswd.cget('show')=='':
                self.pswd.config(show='*')
            else:
                self.pswd.config(show='')

        def AuthCred(self):
            UName=self.usrnme.get()
            PWord=self.pswd.get()
            cur.execute((f"SELECT username FROM users WHERE username='{UName}' AND password='{PWord}';"))
            if not cur.fetchall():
                messagebox.showerror("Login Panel","Invalid credentials")
            else:
                self.root.destroy()
                main()

        def DigClockLogin(self):
            try:
                text_input= time.strftime("%H:%M:%S")
                self.clock.config(text=text_input)
                self.clock.after(2,self.DigClockLogin)
            except:
                pass

    class register():
        def __init__(self):
            self.root=Tk()
            self.root.title("Register Panel")
            self.root.geometry('355x315')
            self.root.resizable(height=False, width=False)
            self.root.configure(bg='#737171')
            self.root.iconbitmap('dat/form.ico')

            Label(self.root,bg="#b6c71c",height=220,width=1).place(x=220,y=0)#lime-yellow 1
            Label(self.root,bg="#f59911",height=220,width=1).place(x=245,y=0)#orange 1
            Label(self.root,bg="#cc4235",height=220,width=1).place(x=270,y=0)#red 1
            Label(self.root,bg="#f59911",height=220,width=1).place(x=295,y=0)#orange 2
            Label(self.root,bg="#b6c71c",height=220,width=1).place(x=320,y=0)#lime-yellow 2

            Label(self.root,text="Create new account :",relief=RAISED,font=("helvetica",12),width=20,bg='grey',
                fg='white').place(x=21,y=15)

            Label(self.root,text="Username:",bg='grey',fg='white').place(x=21,y=50)#username
            self.usrnme=Entry(self.root,width=30)
            self.usrnme.place(x=21,y=70)

            Label(self.root,text="Password:",bg='grey',fg='white').place(x=21,y=110)#password
            self.pswd=Entry(self.root,width=25,show='*')
            self.pswd.place(x=21,y=130)

            Label(self.root,text="Confirm Password:",bg='grey',fg='white').place(x=21,y=170)#confirm password
            self.cnfrm=Entry(self.root,width=25,show='*')
            self.cnfrm.place(x=21,y=190)

            Label(self.root,text="",bg='grey',width=20).place(x=40,y=230)
            Label(self.root,text="Security Code:",bg='grey',fg='white').place(x=21,y=230)#security code

            Button(self.root,text="Create Account",height=1,width=13,bg="grey",fg="white",command=self.CheckCreds).place(x=21,y=270)
            Button(self.root,text="Login",height=1,width=6,bg="grey",fg="white",command=lambda: [self.root.destroy(), main.login()]).place(x=125,y=270)

            ques_img=PhotoImage(file='dat/question_mark.png')
            ques=Button(self.root,text="",command=self.HelpRegister)
            ques.config(image=ques_img)
            ques.place(x=180,y=270)

            see1_img=PhotoImage(file='dat/view.png')
            see1=Button(self.root,text="",command=self.ViewTopEye)
            see1.config(image=see1_img)
            see1.place(x=180,y=130)

            see2_img=PhotoImage(file='dat/view.png')
            see2=Button(self.root,text="",command=self.ViewBottomEye)
            see2.config(image=see2_img)
            see2.place(x=180,y=190)

            self.root.mainloop()

        def LoginButtonRegister(self):
            self.root.destroy()
            login()

        def CheckCreds(self):
            UName=self.usrnme.get()
            PWord=self.pswd.get()
            CFirm=self.cnfrm.get()
            cur.execute(f"SELECT username FROM users WHERE username='{UName}';")
            if UName=="" or PWord=="":
                messagebox.showerror("Register Panel","No entries given")
            elif len(PWord)>10 or len(CFirm)>10 or len(UName)>10:
                messagebox.showerror("Register Panel","Entries exceed limit")
            elif PWord!=CFirm:
                messagebox.showerror("Register Panel","Passwords do not match")
            elif cur.fetchall():
                messagebox.showerror("Register Panel","This username is already taken")
            else:
                if 0<len(UName)<10 and 0<len(PWord)<10 and 0<len(CFirm)<10:
                    UID=random.randint(1000,9999)
                    cur.execute(f"SELECT security_code FROM users WHERE security_code='{UID}';")    
                    if not cur.fetchall():
                        cur.execute(f"INSERT INTO users(username,password,security_code) VALUES('{UName}','{PWord}','{UID}');")
                        Label(self.root,text=UID,font=("",9),bg='grey',fg='white',width=10).place(x=130,y=230)
                        messagebox.showwarning("Register Panel","Please take note of your security code then proceed to login")

        def HelpRegister(self):
            messagebox.showinfo("Register Help","Username, Password and Confirm Password entries must be less than 10 chara"
                                "cters long. Take note of your security code upon creating an account")

        def ViewTopEye(self):
            if self.pswd.cget('show')=='':
                self.pswd.config(show='*')
            else:
                self.pswd.config(show='')

        def ViewBottomEye(self):
            if self.cnfrm.cget('show')=='':
                self.cnfrm.config(show='*')
            else:
                self.cnfrm.config(show='')

main.login()
#change to main.login() after completing main program
#DO NOT UNDO """ ^^^
