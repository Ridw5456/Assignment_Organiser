from tkinter import * # Initialising Tkinter
import datetime as dt
import sqlite3, random, time
import pandas as pd
from tkinter import ttk,messagebox,filedialog
# Added some Libs I would be using later on after some research
con=sqlite3.connect('C:/Users/ridwa/Documents/CS_Project/Program/dat/db.db') # Connecting to the database
cur=con.cursor() # Cursor is used to make changes to the database

cur.execute("""CREATE TABLE IF NOT EXISTS
users(user_id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT,
security_code TEXT);""")
# Creating the users table
cur.execute("""CREATE TABLE IF NOT EXISTS
sessions(session_id INTEGER PRIMARY KEY AUTOINCREMENT,
start_time TEXT,
end_time TEXT,
score INTEGER,
user_id INTEGER,
FOREIGN KEY(user_id) REFERENCES users(user_id));""")
# Creating the sessions table
cur.execute("""CREATE TABLE IF NOT EXISTS
timetables(timetable_id INTEGER PRIMARY KEY AUTOINCREMENT,
path TEXT,
user_id INTEGER,
FOREIGN KEY(user_id) REFERENCES users(user_id));""")
# Creating the timetables table
cur.execute("""CREATE TABLE IF NOT EXISTS
notes(note_id INTEGER PRIMARY KEY AUTOINCREMENT,
note TEXT,
date TEXT,
path TEXT,
user_id INTEGER,
FOREIGN KEY(user_id) REFERENCES users(user_id));""")
# Creating the notes table
con.commit() # Saves the changes made to the database

class main(): # Containing the login class in the main program class
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
                fg='white').place(x=21,y=15) # New account label

            Label(self.root,text="Username:",bg='grey',fg='white').place(x=21,y=50)#username
            self.usrnme=Entry(self.root,width=30) # Username entry
            self.usrnme.place(x=21,y=70)

            Label(self.root,text="Password:",bg='grey',fg='white').place(x=21,y=110) # Password
            self.pswd=Entry(self.root,width=25,show='*') # Password entry
            self.pswd.place(x=21,y=130)

            Label(self.root,text="Confirm Password:",bg='grey',fg='white').place(x=21,y=170)
            self.cnfrm=Entry(self.root,width=25,show='*') # Confirm password entry
            self.cnfrm.place(x=21,y=190)

            Label(self.root,text="",bg='grey',width=23).place(x=40,y=230)
            Label(self.root,text="Security Code:",bg='grey',fg='white').place(x=21,y=230) # Security code

            Button(self.root,text="Create Account",height=1,width=13,bg="grey",fg="white",command=self.CheckCreds).place(x=21,y=270) # Button to create an account
            Button(self.root,text="Login",height=1,width=6,bg="grey",fg="white",command=self.LoginButtonRegister).place(x=125,y=270) # Buttin to login

            ques_img=PhotoImage(file='dat/question_mark PNG.png')
            ques=Button(self.root,text="",command=self.HelpRegister) # Help button
            ques.config(image=ques_img)
            ques.place(x=180,y=270)

            see1_img=PhotoImage(file='dat/view PNG.png')
            see1=Button(self.root,text="",command=self.ViewTopEye) # View password
            see1.config(image=see1_img)
            see1.place(x=180,y=130)

            see2_img=PhotoImage(file='dat/view PNG.png')
            see2=Button(self.root,text="",command=self.ViewBottomEye) # View confirm password
            see2.config(image=see2_img)
            see2.place(x=180,y=190)

            self.root.mainloop()

        def LoginButtonRegister(self):
            self.root.destroy()
            main.login() # Return to login panel

        def CheckCreds(self): # Authenticate the input
            UName=self.usrnme.get() # Username
            PWord=self.pswd.get() # Password
            CFirm=self.cnfrm.get() # Confirm password
            cur.execute(f"SELECT username FROM users WHERE username='{UName}';") # Searches for username that matches the user input
            if UName=="" or PWord=="": # If the entries are blank
                messagebox.showerror("Register Panel","No entries given")
            elif len(PWord)>10 or len(CFirm)>10 or len(UName)>10: # If the input is longer than 10
                messagebox.showerror("Register Panel","Entries exceed limit")
            elif PWord!=CFirm: # If password and confirm password do not match
                messagebox.showerror("Register Panel","Passwords do not match")
            elif cur.fetchall(): # The username is already taken
                messagebox.showerror("Register Panel","This username is already taken")
            else: # It meets all the authentication requirements
                if 0<len(UName)<10 and 0<len(PWord)<10 and 0<len(CFirm)<10:
                    UID=random.randint(1000,9999) # Generates a random security code
                    cur.execute(f"SELECT security_code FROM users WHERE security_code='{UID}';")    
                    if not cur.fetchall(): # If the security code does not exist yet
                        cur.execute(f"INSERT INTO users(username,password,security_code) VALUES('{UName}','{PWord}','{UID}');") # Inserts credentials into database
                        con.commit() # Save to database
                        Label(self.root,text=UID,font=("",9),bg='grey',fg='white',width=10).place(x=130,y=230) # A label used to place the security code on screen
                        messagebox.showwarning("Register Panel","Please take note of your security code then proceed to login")
                        self.root.destroy()
                        main.login()
                    else:
                        CheckCreds()

        def HelpRegister(self): # The help window
            messagebox.showinfo("Register Help","Username, Password and Confirm Password entries must be less than 10 characters long. Take note of your security code.")

        def ViewTopEye(self):
            if self.pswd.cget('show')=='': # Hiding password
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
                fg='white').place(x=21,y=15) # Reads "Reset Password" on screen

            Label(self.root,text="Username:",bg='grey',fg='white').place(x=21,y=50) # Username
            self.usrnme=Entry(self.root,width=30)
            self.usrnme.place(x=21,y=70)

            Label(self.root,text="New Password:",bg='grey',fg='white').place(x=21,y=110) # Password
            self.pswd=Entry(self.root,width=25,show='*')
            self.pswd.place(x=21,y=130)

            Label(self.root,text="Confirm New Password:",bg='grey',fg='white').place(x=21,y=170) # Confirm password
            self.cnfrm=Entry(self.root,width=25,show='*')
            self.cnfrm.place(x=21,y=190)

            Label(self.root,text="Enter Security Code:",bg='grey',fg='white').place(x=21,y=230) # Security code
            self.seccode=Entry(self.root,width=4)
            self.seccode.place(x=143,y=230)

            Button(self.root,text="Reset Password",height=1,width=13,bg="grey",fg="white",command=self.ResetPW).place(x=21,y=270) # Reset Password button
            Button(self.root,text="Login",height=1,width=10,bg="grey",fg="white",command=self.Login).place(x=125,y=270)

            see1_img=PhotoImage(file='dat/view PNG.png')
            see1=Button(self.root,text="",command=self.ViewTopEye) # Show password button
            see1.config(image=see1_img)
            see1.place(x=180,y=130)

            see2_img=PhotoImage(file='dat/view PNG.png')
            see2=Button(self.root,text="",command=self.ViewBottomEye) # Show confirm password button
            see2.config(image=see2_img)
            see2.place(x=180,y=190)

            ques_img=PhotoImage(file='dat/question_mark PNG.png')
            ques=Button(self.root,text="",command=self.HelpReset) # Help button
            ques.config(image=ques_img)
            ques.place(x=180,y=228)

            self.root.mainloop()

        def ResetPW(self):
            UName=self.usrnme.get() # Gets the username input
            NewPW=self.pswd.get() # Gets the password input
            ConfPW=self.cnfrm.get() # Gets the confirm password input
            SecCode=self.seccode.get()# Gets the security code input
            if ConfPW=="" or NewPW=="": # If the confirm new password or new password entries are left blank
                messagebox.showerror("Register Panel","No entries given")
            elif len(NewPW)>10 or len(ConfPW)>10 or len(UName)>10: # If the username, password or confirm password entries exceed 10 characters
                messagebox.showerror("Register Panel","Entries exceed limit")
            elif NewPW!=ConfPW: # New password does not match confirm new password
                messagebox.showerror("Register Panel","Passwords do not match")
            else:
                cur.execute((f"SELECT security_code FROM users WHERE username='{UName}' AND security_code='{SecCode}';")) # SQL query
                if not cur.fetchall(): # If the username and security code do not match
                    messagebox.showerror("Reset Password Panel","Username and Security Code do not match.")
                else:
                    cur.execute(f"UPDATE users SET password='{NewPW}' WHERE security_code='{SecCode}';") # SQL query
                    con.commit()
                    messagebox.showinfo("Reset Password Panel","Successfully updated password. Proceed to login panel.")
                    self.root.destroy()
                    main.login()
                    
        def Login(self):
            self.root.destroy()
            main.login() # Proceed to login panel
            
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

        def HelpReset(self): # Help message box
            messagebox.showinfo("Rest Password Panel","The Security Code is the linked number given upon creating an account.")

try:
    main.login() # Upon starting the program it jumps to login
except:
    pass # Ignores flagged errors that would prevent the program from running
