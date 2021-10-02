from tkinter import *
import time
import datetime as dt
import sqlite3
from tkinter import messagebox
import threading


con=sqlite3.connect('db.db')
cur=con.cursor()




class main():
    def __init__(self):
        self.root=Tk()
        self.root.title("Assignment Organiser")
        self.root.geometry('1400x700')
        self.root.resizable(height=False, width=False)
        self.root.configure(bg='grey')

        self.root.mainloop()
    class login():
        def __init__(self):
            self.root=Tk()
            self.root.title("Login Panel")
            self.root.geometry('355x220')
            self.root.resizable(height=False, width=False)
            self.root.configure(bg='#737171')
            self.root.iconbitmap('./lock.ico')

            Label(self.root,text="Login Credentials :",relief=RAISED,font=("helvetica",15),width=16,bg='grey',
                fg='white').place(x=21,y=15)

            Label(self.root,bg="#b6c71c",height=220,width=1).place(x=220,y=0)#lime-yellow 1
            Label(self.root,bg="#f59911",height=220,width=1).place(x=245,y=0)#orange 1
            Label(self.root,bg="#cc4235",height=220,width=1).place(x=270,y=0)#red 1
            Label(self.root,bg="#f59911",height=220,width=1).place(x=295,y=0)#orange 2
            Label(self.root,bg="#b6c71c",height=220,width=1).place(x=320,y=0)#lime-yellow 2
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

            see_img=PhotoImage(file='./view.png')
            see=Button(self.root,text="",command=self.View)
            see.config(image=see_img)
            see.place(x=180,y=135)
            self.Digitalclock()
            self.root.mainloop()
        def Register(self):
            self.root.destroy()
            main.register()

        def View(self):
            if self.pswd.cget('show')=='':
                self.pswd.config(show='*')
            else:
                self.pswd.config(show='')

        def AuthCred(self):
            UName=self.usrnme.get()
            PWord=self.pswd.get()
            cur.execute((f"SELECT username FROM users WHERE username='{UName}' AND password='{PWord}';"))
            if not cur.fetchall(self):
                messagebox.showerror("Login Panel","Invalid credentials")
            else:
                self.root.destroy()
                main()

        def TogglePW(self):
            if self.pswd.cget('show')=='':
                self.pswd.config(show='*')

        def Digitalclock(self):
            try:
                text_input= time.strftime("%H:%M:%S")
                self.clock.config(text=text_input)
                self.clock.after(2, self.Digitalclock)
            except:
                pass






    class register():
        def __init__(self):
            self.root=Tk()
            self.root.title("Register Panel")
            self.root.geometry('355x315')
            self.root.resizable(height=False, width=False)
            self.root.configure(bg='#737171')
            self.root.iconbitmap('./form.ico')

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
            #Label on screen with randomly generated security code matching new user account, 4 digits
            Label(self.root,text="0 0 0 0",font=("",9),bg='grey',fg='white',width=10).place(x=130,y=230)

            Button(self.root,text="Create Account",height=1,width=13,bg="grey",fg="white",command=lambda: self.Check).place(x=21,y=270)
            #creates account by appending to database


            Button(self.root,text="Login",height=1,width=6,bg="grey",fg="white",command=lambda: [self.root.destroy(), main.login()]).place(x=125,y=270)

            ques_img=PhotoImage(file='./question_mark.png')
            ques=Button(self.root,text="",command=lambda: self.Help)
            ques.config(image=ques_img)
            ques.place(x=180,y=270)

            see1_img=PhotoImage(file='./view.png')
            see1=Button(self.root,text="",command=lambda:self.View1)
            see1.config(image=see1_img)
            see1.place(x=180,y=130)

            see2_img=PhotoImage(file='./view.png')
            see2=Button(self.root,text="",command=lambda: self.View2)
            see2.config(image=see2_img)
            see2.place(x=180,y=190)

            self.root.mainloop()

        def GetCode(self):
            print("The security code returns here")

        def Login(self):
            self.root.destroy()
            login()

        def Check(self):
            if len(self.pswd.get()) > 10 or len(self.cnfrm.get()) > 10 or len(self.usrnme.get()) > 10:
                messagebox.showerror("Register Panel","Entries exceed limit")
            elif self.pswd.get() != self.cnfrm.get():
                messagebox.showerror("Register Panel","Passwords do not match")
            else:
                GetCode()

        def Help(self):
            messagebox.showinfo("Register Help","Username, Password and Confirm Password entries must be less than 10 characters long")

        def View1(self):
            if self.pswd.cget('show')=='':
                self.pswd.config(show='*')
            else:
                self.pswd.config(show='')

        def View2(self):
            if self.cnfrm.cget('show')=='':
                self.cnfrm.config(show='*')
            else:
                self.cnfrm.config(show='')



main.login()