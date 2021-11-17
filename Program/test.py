##########
#
# TO DO:
#   - STOPWATCH AND TIMER ON MAIN WINDOW
#   - SESSION TIME TO SECONDS BECOMES A SCORE, PERSONAL SCORES WINDOW BUTTON, PASTES ALL SESSION SCORES INTO EACH LINE
#   - SESSION ENDS, SESSION TIME = SESSION SCORE, ADD TO DB BASED ON UID
#
# EVALUATION:
#   - HIGH SCORE TRACKER FOR USERS TO SEE EACOTHERS HIGH SCORES, post online (?)
#   - DID NOT NEED TO USE TIMETABLE ID NEITHER SESSION ID, SAVED TO USER DIR INSTEAD
#   - THROUGH FILE MGR USERS CAN ACCESS AND EDIT EACHOTHERS TIMETABLES INTO EACHOTHERS DIR, NEEDS SECURITY
#   - NOT AS ENGAGING AS I ORIGINALLY THOUGHT IT WOULD BE, CHOICE OF COLOURS, AVAILABLE FEATURES ETC
#   - UI SEEMS TOO BASIC AND STILL SLIGHTLY UNAPPROACHABLE, CAN USE ANOTHER GUI LIB 
#   - HOW TO ADD ASIGNMENTS TO AN ARRAY LIKE DATA STRUCTURE (LINKED LIST) AND UPDATE THE WORK PRIORITY
#   - KEYBOARD SHORTCUTS IN TEXT BOX ENTRY, BINDING EVENTS TO MAKE TYPING EASIER (e.g. Ctrl+Backspace=delete last word)
#   - DARK THEME TO MAKE IT MORE APPEALING
#   - FORMATTING ISSUES WITH TEXT AND TIMETABLE
#
##########

from tkinter import *
import datetime as dt
import sqlite3,random,time,os,shutil,pathlib,threading
import pandas as pd
from tkinter import ttk,messagebox,filedialog
from tkcalendar import *

c=os.getcwd()
con=sqlite3.connect(c+'/dat/db.db')
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
        #
        self.root=Tk()
        self.root.title("Assignment Organiser")
        self.root.geometry('1400x700')
        self.root.resizable(height=False,width=False)
        self.root.configure(bg='#6B8282')
        self.root.iconbitmap('dat/IMG/notebook ICO.ico')

        self.UN=username
        #
        Label(self.root,bg='black',height=1,width=62).place(x=0,y=665)
        Label(self.root,bg="#EB998E",height=4,width=55).place(x=0,y=0)
        Label(self.root,bg='black',width=2,height=2).place(x=430,y=665)
        Label(self.root,bg="#EB998E",height=2,width=62).place(x=0,y=670)
        #
        logout_img=PhotoImage(file='dat/IMG/logout PNG.png')
        logoutb=Button(self.root,text="",command=self.Logout,image=logout_img)
        logoutb.place(x=9,y=9)
        #
        cur.execute(f"SELECT user_id FROM users WHERE username='{username}';")
        UID=cur.fetchall()
        Label(self.root,text="Username :",font=("",9,'bold'),bg="#EB998E",fg='black').place(x=8,y=673)
        Label(self.root,text=self.UN,font=("",9,'bold'),bg="#EB998E",fg='black').place(x=80,y=673)
        Label(self.root,text="UID :",font=("",9,'bold'),bg="#EB998E",fg='black').place(x=150,y=673)
        Label(self.root,text=UID,font=("",9,'bold'),bg="#EB998E",fg='black').place(x=180,y=673)
        Label(self.root,text="Session Time :",font=("",9,'bold'),bg="#EB998E",fg='black').place(x=235,y=673)
        self.start=time.time()
        self.sessiontime=Label(self.root,text="",font=("",12,'bold'),bg="#EB998E",fg='black',relief=RAISED)
        self.sessiontime.place(x=330,y=673)
        #
        Label(self.root,bg='black',width=1,height=4).place(x=310,y=0)
        Label(self.root,bg='black',width=1,height=4).place(x=430,y=0)
        self.clock=Label(self.root,font=("helvetica",20,'bold'),bg="#EB998E",fg="black",width=7,height=2)
        self.clock.place(x=314,y=-4)

        self.date=Label(self.root,fg="black",bg="#EB998E",font=("",20,'bold'),width=13,
                   height=1,relief=RAISED)
        self.date.place(x=70,y=12)
        #
        style=ttk.Style()
        style.theme_use('clam')
        CalFrame=ttk.Frame(self.root) # The frame sits in window (main)
        CalFrame.place(height=200,width=300,rely=0,relx=.786) # Height and placement
        t=dt.date.today() # Get today date
        self.cal=Calendar(CalFrame,selectmode='day',year=t.year,month=t.month,day=t.day)
        self.cal.pack(fill='both',expand=True) # Fill entire container
        #
        Label(self.root,bg='black',width=1,height=50).place(x=1090,y=0)
        
        Button(self.root,text="Open Note",command=self.OpenNote,width=10,bg='#229954',fg='white').place(x=1117,y=210)
        Button(self.root,text="Save Note",command=self.SaveNote,width=10,bg='#229954',fg='white').place(x=1213,y=210)
        self.cfrmsave=Label(self.root,text="",bg='#6B8282',fg='green',font=('arial',10,'bold'))
        self.cfrmsave.place(x=1320,y=211) # Label to confirm saving edits to the txt file
        Button(self.root,text="Session Tracker",command=self.SessionTracker,width=24).place(x=1117,y=248)
        self.noten=Label(self.root,text="",bg='#6B8282',fg='white',font=("",12,'bold'))
        self.noten.place(x=1117,y=284)
        Label(self.root,bg='black',width=50).place(x=1100,y=318)
        Label(self.root,bg='#6B8282',width=50).place(x=1103,y=322)
        #
        self.windtext=Text(self.root,font=('Helvetica',10),height=100,width=93)
        self.windtext.place(y=0,x=444)

        self.TblFrame=LabelFrame(self.root) # Timetable frame
        self.TblFrame.place(height=520,width=444,rely=.0937,relx=0) # Place frame

        self.FileFrame=LabelFrame(self.root,text="Timetable") # File frame
        self.FileFrame.place(height=80,width=444,rely=.835,relx=0) # Place frame

        Button(self.FileFrame,text="Open",command=self.FileOpen).place(rely=.5,relx=.05)
        Button(self.FileFrame,text="Load",command=self.FileDat).place(rely=.5,relx=.2)
        Button(self.FileFrame,text="Clear",command=self.Purge).place(rely=.5,relx=.35)

        self.Lab1=Label(self.FileFrame,text="No File Selected") # "No File Selected" label
        self.Lab1.place(rely=0,relx=0) # Place label in frame

        self.Tree=ttk.Treeview(self.TblFrame) # Creatine a tree for the spreadsheet file
        self.Tree.place(relheight=1,relwidth=1) # Place the tree, tree spans entire frame

        self.ScrollY=Scrollbar(self.TblFrame,orient="vertical",command=self.Tree.yview) # Vertical scrollbar
        self.ScrollX=Scrollbar(self.TblFrame,orient="horizontal",command=self.Tree.xview) # Horizontal scrollbar
        self.Tree.configure(xscrollcommand=self.ScrollX.set,yscrollcommand=self.ScrollY.set) # Config Scroll X,Y
        self.ScrollX.pack(side="bottom",fill="x") # Scroller X on x-axis bottom
        self.ScrollY.pack(side="right",fill="y") # Scroller Y on y-axis right
        #
        self.SessionClock()
        self.DigClockMain()
        self.CalMain()
        self.root.mainloop()

    def OpenNote(self):
        cwd=os.getcwd() # Gets CWD
        self.OpenNote=filedialog.askopenfilename(initialdir=(cwd+'/dat/usr/'+self.UN+'/Notes'),title="Select A File",
                                                 filetype=(("txt files","*.txt"),("All Files","*.*")))
        self.ON=pathlib.Path(self.OpenNote)
        try:
            self.noten['text']=(self.ON.name) # Change label to name of the file selected
            opcontent=open(self.ON,'r') # Open the file in ON in read mode
            rtxt=opcontent.read() # Read the file data
            self.windtext.delete('1.0','end') # Deletes the content of the old txt data on the widget
            self.windtext.insert(END,rtxt) # Inserts the new data into the widget
            opcontent.close() # Close connection to the file

        except ValueError: # The files arent spreadsheets (.csv/.xlsx)
            messagebox.showerror("","Invalid file type")
            return None
        except FileNotFoundError: # The file can no longer be found in the directory
            messagebox.showerror("","File does not exist or has been moved")
            return None

        UN=self.UN # The username
        cwd1=pathlib.Path(cwd+'/dat/usr/'+UN+'/Notes') # New CWD to user folder
        os.chdir(cwd1)
        if os.path.exists(self.ON.name):
            pass
        else:
            shutil.copy(self.ON,cwd1) # Copy the file to the user area
        os.chdir(cwd)

    def SaveNote(self):
        opcontent=open(self.ON,'w') # Open in write mode
        opcontent.write(self.windtext.get('1.0','end')) # Overwrites the contents
        # of whats on the Text widget to the text file selected
        x=threading.Thread(target=self.Count) # Thread Count
        x.start() # Start Thread

    def SessionTracker(self):
        print("")

    def Count(self):
        self.cfrmsave['text']="Saved!" # Change label to read "Saved!"
        self.cfrmsave['bg']="white" # Change background to white
        time.sleep(3) # Sleep
        self.cfrmsave['text']="" # Revert text
        self.cfrmsave['bg']="#6B8282" # Revert background

    def SessionClock(self):
        secs=int(time.time()-self.start) # Change in time from start to current
        mins=secs//60 # Floor division of seconds to minutes
        secs=secs%60 # Mod seconds
        hrs=mins//60 # Floor division of minutes to hours
        mins=mins%60 # Mod minutes
        self.sessiontime.config(text="{0}:{1}:{2}".format(int(hrs),int(mins),int(secs))) # Insert into label
        self.sessiontime.after(100,self.SessionClock) # Refresh time

    def FileOpen(self):
        cwd=os.getcwd()
        self.OpenFile=filedialog.askopenfilename(initialdir=(cwd+'/dat/usr/'+self.UN+'/Timetables'),title="Select A File",
                                              filetype=(("xlsx files","*.xlsx"),("All Files","*.*")))
        self.Lab1['text']=self.OpenFile
        return None

    def FileDat(self):
        Path=self.Lab1['text']
        try:
            File=r'{}'.format(Path)
            if File[-4]=='.csv':
                self.df=pd.read_csv(File)
            else:
                self.df=pd.read_excel(File)
                
        except ValueError:
            messagebox.showerror("","Invalid file type")
            return None
        except FileNotFoundError:
            messagebox.showerror("","File does not exist or has been moved")
            return None

        UN=self.UN
        OF=pathlib.Path(self.OpenFile)
        cwd=os.getcwd()
        cwd1=pathlib.Path(cwd+'/dat/usr/'+UN+'/Timetables')
        os.chdir(cwd1)
        if os.path.exists(OF.name):
            pass
        else:
            shutil.copy(OF,cwd1)
        
        os.chdir(cwd)
        self.Purge()
        self.Tree['column']=list(self.df.columns)
        self.Tree['show']='headings'
        for column in self.Tree['columns']:
            self.Tree.heading(column,text=column)

        dfRows=self.df.to_numpy().tolist()
        for row in dfRows:
            self.Tree.insert("","end",values=row)
        self.Tree.pack()

    def Purge(self):
        self.Tree.delete(*self.Tree.get_children())
        self.Lab1['text']=""
        return None 
            
    def DigClockMain(self):
        try:
            text_input=time.strftime("%H:%M:%S")
            self.clock.config(text=text_input)
            self.clock.after(100,self.DigClockMain)
        except:
            pass

    def CalMain(self):
        try:
            text_inp=f"{dt.datetime.now():%a %d %b %Y}"
            self.date.config(text=text_inp)
            self.date.after(100,self.CalMain)
        except:
            pass

    def Logout(self):
        logoutnow=messagebox.askokcancel("Assignment Organiser","You will be logging out")
        if logoutnow:
            self.root.destroy()
            main.login()

    def Notes(self):
        self.root=Tk()
        self.root.title("Notes")
        self.root.geometry('600x400')
        self.root.resizable(height=False,width=False)
        self.root.configure(bg='#6B8282')
        self.root.iconbitmap('dat/IMG/notes.ico')

    class login():
        def __init__(self):
            self.root=Tk()
            self.root.title("Login Panel")
            self.root.geometry('355x220')
            self.root.resizable(height=False, width=False)
            self.root.configure(bg='#737171')
            self.root.iconbitmap('dat/IMG/lock ICO.ico')

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

            reset_img=PhotoImage(file='dat/IMG/reset PNG.png')
            resetb=Button(self.root,text="",command=self.ResetPassword,image=reset_img)
            resetb.place(x=180,y=110)

            Button(self.root,text="Register",width=10,height=1,bg="grey",fg="white",
                   command=self.Register).place(x=20,y=175)

            Button(self.root,text="Login",width=10,height=1,bg="grey",fg="white",
                    command=self.AuthCred).place(x=125,y=175)

            Label(self.root,text=f"{dt.datetime.now():%a %b%d %Y}",fg="white",bg="grey",font=("",11),width=12,
                height=1).place(x=220,y=50)

            see_img=PhotoImage(file='dat/IMG/view PNG.png')
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
                self.clock.after(100,self.DigClockLogin)
            except:
                pass

    class register():
        def __init__(self):
            self.root=Tk()
            self.root.title("Register Panel")
            self.root.geometry('355x315')
            self.root.resizable(height=False, width=False)
            self.root.configure(bg='#737171')
            self.root.iconbitmap('dat/IMG/form ICO.ico')

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

            ques_img=PhotoImage(file='dat/IMG/question_mark PNG.png')
            ques=Button(self.root,text="",command=self.HelpRegister)
            ques.config(image=ques_img)
            ques.place(x=180,y=270)

            see1_img=PhotoImage(file='dat/IMG/view PNG.png')
            see1=Button(self.root,text="",command=self.ViewTopEye)
            see1.config(image=see1_img)
            see1.place(x=180,y=130)

            see2_img=PhotoImage(file='dat/IMG/view PNG.png')
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
                        cwd=os.getcwd() # Gets current working directory
                        os.chdir(cwd+'/dat/usr') # Change the current working directory to user folder
                        os.mkdir(UName) # Make a new directory by the username
                        os.chdir(cwd+'/dat/usr/'+UName)
                        os.mkdir("Timetables")
                        os.mkdir("Notes")
                        os.chdir(cwd) # Change back to the original directory
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
            self.root.iconbitmap('dat/IMG/reset ICO.ico')

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

            see1_img=PhotoImage(file='dat/IMG/view PNG.png')
            see1=Button(self.root,text="",command=self.ViewTopEye)
            see1.config(image=see1_img)
            see1.place(x=180,y=130)

            see2_img=PhotoImage(file='dat/IMG/view PNG.png')
            see2=Button(self.root,text="",command=self.ViewBottomEye)
            see2.config(image=see2_img)
            see2.place(x=180,y=190)

            ques_img=PhotoImage(file='dat/IMG/question_mark PNG.png')
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
