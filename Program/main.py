from tkinter import *
import datetime as dt
import sqlite3,random,time
import pandas as pd
from tkinter import ttk,messagebox,filedialog

con=sqlite3.connect('C:/Users/ridwa/Documents/CS_Project/Program/dat/db.db')
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
score INTEGER,
user_id INTEGER,
FOREIGN KEY(user_id) REFERENCES users(user_id));""")

cur.execute("""CREATE TABLE IF NOT EXISTS
timetables(timetable_id INTEGER PRIMARY KEY AUTOINCREMENT,
path TEXT,
user_id INTEGER,
FOREIGN KEY(user_id) REFERENCES users(user_id));""")

cur.execute("""CREATE TABLE IF NOT EXISTS
notes(note_id INTEGER PRIMARY KEY AUTOINCREMENT,
note TEXT,
date TEXT,
path TEXT,
user_id INTEGER,
FOREIGN KEY(user_id) REFERENCES users(user_id));""")

con.commit()

class main():
    def __init__(self,username):
        self.root=Tk()
        self.root.title("Assignment Organiser")
        self.root.geometry('1400x700')
        self.root.resizable(height=False,width=False)
        self.root.configure(bg='#6B8282')
        self.root.iconbitmap('dat/notebook ICO.ico')

        Label(self.root,bg="#EB998E",height=70,width=10).place(x=0,y=0)
        Label(self.root,bg='black',height=1,width=100).place(x=0,y=665)
        Label(self.root,bg="#EB998E",height=4,width=300).place(x=0,y=0)
        Label(self.root,bg="#EB998E",height=4,width=100).place(x=0,y=670)
        
        logout_img=PhotoImage(file='dat/logout PNG.png')
        logoutb=Button(self.root,text="",command=self.Logout,image=logout_img)
        logoutb.place(x=12,y=10)

        timer_img=PhotoImage(file='dat/timer PNG.png')
        timerb=Button(self.root,text="",command=self.TimerSW,image=timer_img)
        timerb.place(x=12,y=70)

        cur.execute(f"SELECT user_id FROM users WHERE username='{username}';")
        UID=cur.fetchall()

        Label(self.root,text="Username :",font=("",9,'bold'),bg="#EB998E",fg='black').place(x=8,y=673)
        Label(self.root,text=username,font=("",9,'bold'),bg="#EB998E",fg='black').place(x=80,y=673)
        Label(self.root,text="UID :",font=("",9,'bold'),bg="#EB998E",fg='black').place(x=150,y=673)
        Label(self.root,text=UID,font=("",9,'bold'),bg="#EB998E",fg='black').place(x=180,y=673)

        Label(self.root,bg='black',width=1,height=4).place(x=1245,y=0)
        self.clock=Label(self.root,font=("helvetica",20,'bold'),bg="#EB998E",fg="black",width=9,height=2)
        self.clock.place(x=1250,y=-4)

        Label(self.root,text=f"{dt.datetime.now():%a %d %b %Y}",fg="black",bg="#EB998E",font=("",20,'bold'),width=12,
              height=1,relief=RAISED).place(x=1020,y=12)
        """
        Label(self.root,text=f"{dt.datetime.now():%B %d, %Y}",fg="white",bg="grey",font=("",11),width=12,
              height=1).place(x=220,y=50) ### Might change to
        """
        self.DigClockMain()
        self.root.mainloop()

    def DigClockMain(self):
        try:
            text_input=time.strftime("%H:%M:%S")
            self.clock.config(text=text_input)
            self.clock.after(2,self.DigClockMain)
        except:
            pass

    def Logout(self):
        logoutnow=messagebox.askokcancel("Assignment Organiser","You will be logging out")
        if logoutnow:
            self.root.destroy()
            main.login()

    def TimerSW(self):
        self.root=Tk()
        self.root.title("Stopwatch and Timer")
        self.root.geometry('300x500')
        self.root.resizable(height=False,width=False)
        self.root.configure(bg='#6B8282')
        self.root.iconbitmap('dat/timer ICO.ico')

        Button(self.root,text="Start",width=10,height=1,bg="grey",fg="white",command=self.Start_t) #Place
        Button(self.root,text="Stop",width=10,height=1,bg="grey",fg="white",command=self.Stop_t) #Place
        Button(self.root,text="Reset",width=10,height=1,bg="grey",fg="white",command=self.Reset_t) #Place

    def Start_t(self):
        #Starts the timer on screen
        print("") #null

    def Stop_t(self):
        #Stops the timer on screen
        print("") #null

    def Reset_t(self):
        #Resets the timer on screen
        print("") #null

    def Notes(self):
        self.root=Tk()
        self.root.title("Notes")
        self.root.geometry('600x400')
        self.root.resizable(height=False,width=False)
        self.root.configure(bg='#6B8282')
        self.root.iconbitmap('dat/notes.ico')

    class login():
        def __init__(self):
            self.root=Tk()
            self.root.title("Login Panel")
            self.root.geometry('355x220')
            self.root.resizable(height=False, width=False)
            self.root.configure(bg='#737171')
            self.root.iconbitmap('dat/lock ICO.ico')

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

            Label(self.root,text="Password:",bg="grey",fg="white").place(x=20,y=115)
            self.pswd=Entry(self.root,width=25,show='*')
            self.pswd.place(x=20,y=135)

            reset_img=PhotoImage(file='dat/reset PNG.png')
            resetb=Button(self.root,text="",command=self.ResetPassword,image=reset_img)
            resetb.place(x=180,y=110)

            Button(self.root,text="Register",width=10,height=1,bg="grey",fg="white",
                   command=self.Register).place(x=20,y=175)

            Button(self.root,text="Login",width=10,height=1,bg="grey",fg="white",
                    command=self.AuthCred).place(x=125,y=175)

            Label(self.root,text=f"{dt.datetime.now():%a %b%d %Y}",fg="white",bg="grey",font=("",11),width=12,
                height=1).place(x=220,y=50)

            see_img=PhotoImage(file='dat/view PNG.png')
            see=Button(self.root,text="",command=self.ViewEyeLogin,image=see_img)
            see.place(x=180,y=135)

            self.DigClockLogin()
            self.root.mainloop()

        def ResetPassword(self):
            self.root.destroy()
            main.reset()

        def Register(self):
            self.root.destroy()
            main.register()

        def ViewEyeLogin(self):
            if self.pswd.cget('show')=='':
                self.pswd.config(show='*')
            else:
                self.pswd.config(show='')

        def AuthCred(self):
            self.UN=self.usrnme.get()
            self.PW=self.pswd.get()
            cur.execute((f"SELECT username FROM users WHERE username='{self.UN}' AND password='{self.PW}';"))
            if not cur.fetchall():
                messagebox.showerror("Login Panel","Invalid credentials")
            else:
                self.root.destroy()
                main(self.UN)
            
        def DigClockLogin(self):
            try:
                text_input=time.strftime("%H:%M:%S")
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
            self.root.iconbitmap('dat/form ICO.ico')

            Label(self.root,bg="#b6c71c",height=220,width=1).place(x=220,y=0)#lime-yellow 1
            Label(self.root,bg="#f59911",height=220,width=1).place(x=245,y=0)#orange 1
            Label(self.root,bg="#cc4235",height=220,width=1).place(x=270,y=0)#red 1
            Label(self.root,bg="#f59911",height=220,width=1).place(x=295,y=0)#orange 2
            Label(self.root,bg="#b6c71c",height=220,width=1).place(x=320,y=0)#lime-yellow 2

            Label(self.root,text="Create New Account :",relief=RAISED,font=("helvetica",12),width=20,bg='grey',
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

            Label(self.root,text="",bg='grey',width=23).place(x=40,y=230)
            Label(self.root,text="Security Code:",bg='grey',fg='white').place(x=21,y=230)#security code

            Button(self.root,text="Create Account",height=1,width=13,bg="grey",fg="white",command=self.CheckCreds).place(x=21,y=270)
            Button(self.root,text="Login",height=1,width=6,bg="grey",fg="white",command=self.LoginButtonRegister).place(x=125,y=270)

            ques_img=PhotoImage(file='dat/question_mark PNG.png')
            ques=Button(self.root,text="",command=self.HelpRegister)
            ques.config(image=ques_img)
            ques.place(x=180,y=270)

            see1_img=PhotoImage(file='dat/view PNG.png')
            see1=Button(self.root,text="",command=self.ViewTopEye)
            see1.config(image=see1_img)
            see1.place(x=180,y=130)

            see2_img=PhotoImage(file='dat/view PNG.png')
            see2=Button(self.root,text="",command=self.ViewBottomEye)
            see2.config(image=see2_img)
            see2.place(x=180,y=190)

            self.root.mainloop()

        def LoginButtonRegister(self):
            self.root.destroy()
            main.login()

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
                        con.commit()
                        Label(self.root,text=UID,font=("",9),bg='grey',fg='white',width=10).place(x=130,y=230)
                        messagebox.showwarning("Register Panel","Please take note of your security code then proceed to login")
                        self.root.destroy()
                        main.login()

        def HelpRegister(self):
            messagebox.showinfo("Register Help","Username, Password and Confirm Password entries must be less than 10 chara"
                                "cters long. Take note of your security code upon creating an account.")

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

    class reset():
        def __init__(self):
            self.root=Tk()
            self.root.title("Reset Password Panel")
            self.root.geometry('355x315')
            self.root.resizable(height=False, width=False)
            self.root.configure(bg='#737171')
            self.root.iconbitmap('dat/reset ICO.ico')

            Label(self.root,bg="#b6c71c",height=220,width=1).place(x=220,y=0)#lime-yellow 1
            Label(self.root,bg="#f59911",height=220,width=1).place(x=245,y=0)#orange 1
            Label(self.root,bg="#cc4235",height=220,width=1).place(x=270,y=0)#red 1
            Label(self.root,bg="#f59911",height=220,width=1).place(x=295,y=0)#orange 2
            Label(self.root,bg="#b6c71c",height=220,width=1).place(x=320,y=0)#lime-yellow 2

            Label(self.root,text="Reset Password :",relief=RAISED,font=("helvetica",12),width=20,bg='grey',
                fg='white').place(x=21,y=15)

            Label(self.root,text="Username:",bg='grey',fg='white').place(x=21,y=50)#username
            self.usrnme=Entry(self.root,width=30)
            self.usrnme.place(x=21,y=70)

            Label(self.root,text="New Password:",bg='grey',fg='white').place(x=21,y=110)#password
            self.pswd=Entry(self.root,width=25,show='*')
            self.pswd.place(x=21,y=130)

            Label(self.root,text="Confirm New Password:",bg='grey',fg='white').place(x=21,y=170)#confirm password
            self.cnfrm=Entry(self.root,width=25,show='*')
            self.cnfrm.place(x=21,y=190)

            Label(self.root,text="Enter Security Code:",bg='grey',fg='white').place(x=21,y=230)#security code
            self.seccode=Entry(self.root,width=4)
            self.seccode.place(x=143,y=230)

            Button(self.root,text="Reset Password",height=1,width=13,bg="grey",fg="white",command=self.ResetPW).place(x=21,y=270)
            Button(self.root,text="Login",height=1,width=10,bg="grey",fg="white",command=self.Login).place(x=125,y=270)

            see1_img=PhotoImage(file='dat/view PNG.png')
            see1=Button(self.root,text="",command=self.ViewTopEye)
            see1.config(image=see1_img)
            see1.place(x=180,y=130)

            see2_img=PhotoImage(file='dat/view PNG.png')
            see2=Button(self.root,text="",command=self.ViewBottomEye)
            see2.config(image=see2_img)
            see2.place(x=180,y=190)

            ques_img=PhotoImage(file='dat/question_mark PNG.png')
            ques=Button(self.root,text="",command=self.HelpReset)
            ques.config(image=ques_img)
            ques.place(x=180,y=228)

            self.root.mainloop()

        def ResetPW(self):
            UName=self.usrnme.get()
            NewPW=self.pswd.get()
            ConfPW=self.cnfrm.get()
            SecCode=self.seccode.get()
            if ConfPW=="" or NewPW=="":
                messagebox.showerror("Register Panel","No entries given")
            elif len(NewPW)>10 or len(ConfPW)>10 or len(UName)>10:
                messagebox.showerror("Register Panel","Entries exceed limit")
            elif NewPW!=ConfPW:
                messagebox.showerror("Register Panel","Passwords do not match")
            else:
                cur.execute((f"SELECT security_code FROM users WHERE username='{UName}' AND security_code='{SecCode}';"))
                if not cur.fetchall():
                    messagebox.showerror("Reset Password Panel","Username and Security Code do not match.")
                else:
                    cur.execute(f"UPDATE users SET password='{NewPW}' WHERE security_code='{SecCode}';")
                    con.commit()
                    messagebox.showinfo("Reset Password Panel","Successfully updated password. Proceed to login panel.")
                    self.root.destroy()
                    main.login()
                    
        def Login(self):
            self.root.destroy()
            main.login()
            
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

        def HelpReset(self):
            messagebox.showinfo("Rest Password Panel","The Security Code is the linked number given upon creating an account.")

try:
    main.login()
except:
    pass
