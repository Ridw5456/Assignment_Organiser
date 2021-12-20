##########
#
# TO DO:
#   - STOPWATCH AND TIMER ON MAIN WINDOW
#
# EVALUATION:
#   - HIGH SCORE TRACKER FOR USERS TO SEE EACOTHERS HIGH SCORES, post online (?)
#   - DID NOT NEED TO USE TIMETABLE ID NEITHER SESSION ID, SAVED TO USER DIR INSTEAD
#   - THROUGH FILE MGR USERS CAN ACCESS AND EDIT EACHOTHERS TIMETABLES INTO EACHOTHERS DIR, NEEDS SECURITY
#   - NOT AS ENGAGING AS I ORIGINALLY THOUGHT IT WOULD BE, CHOICE OF COLOURS, AVAILABLE FEATURES ETC
#   - UI SEEMS TOO BASIC AND STILL SLIGHTLY UNAPPROACHABLE, CAN USE ANOTHER GUI LIB 
#   - HOW TO ADD ASIGNMENTS TO AN ARRAY LIKE DATA STRUCTURE (LINKED LIST) AND UPDATE THE WORK PRIORITY
#   - KEYBOARD SHORTCUTS IN TEXT BOX ENTRY TO MAKE TYPING EASIER (e.g. Ctrl+Backspace=delete last word)
#   - DARK THEME TO MAKE IT MORE APPEALING
#   - FORMATTING ISSUES WITH TEXT AND TIMETABLE
#   - OVERWRITE TIMETABLE EVEN WHEN FILE IS THE SAME
#   - HIGH SCORE DAMNENING FACTOR THE HIGH THE CURRENT TOTAL SCORE IS, MAKES IT HARDER TO SCORE HIGH CONSISTENTLY THEREFORE USER SCORES WILL NOT BE INCREDIBLY LARGE INTEGERS
#
##########

from sqlite3.dbapi2 import TimeFromTicks
from tkinter import *
import datetime as dt
import sqlite3,random,time,os,shutil,pathlib,threading,numpy
from PIL import ImageTk,Image
import pandas as pd
from tkinter import ttk,messagebox,filedialog
from tkcalendar import *

c=os.getcwd()
con=sqlite3.connect(c+'\dat\db.db')
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
secs INTEGER,
date TEXT,
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
        self.UN=username
        self.startsecs=round(time.time())
        self.starttime=dt.datetime.now().strftime('%H:%M:%S')
        Label(self.root,bg='black',height=1,width=62).place(x=0,y=665)
        Label(self.root,bg="#EB998E",height=4,width=55).place(x=0,y=0)
        Label(self.root,bg='black',width=2,height=2).place(x=430,y=665)
        Label(self.root,bg="#EB998E",height=2,width=62).place(x=0,y=670)
        logout_img=ImageTk.PhotoImage(file='dat/logout PNG.png')
        logoutb=Button(self.root,text="",command=self.Logout,image=logout_img)
        logoutb.place(x=9,y=9)
        self.root.bind('<Escape>',self.Logout)
        cur.execute(f"SELECT user_id FROM users WHERE username='{username}';")
        self.UID=cur.fetchall()
        Label(self.root,text="Username :",font=("",9,'bold'),bg="#EB998E",fg='black').place(x=8,y=673)
        Label(self.root,text=self.UN,font=("",9,'bold'),bg="#EB998E",fg='black').place(x=80,y=673)
        Label(self.root,text="UID :",font=("",9,'bold'),bg="#EB998E",fg='black').place(x=150,y=673)
        Label(self.root,text=self.UID,font=("",9,'bold'),bg="#EB998E",fg='black').place(x=180,y=673)
        Label(self.root,text="Session Time :",font=("",9,'bold'),bg="#EB998E",fg='black').place(x=235,y=673)
        self.sessiontime=Label(self.root,text="",font=("",12,'bold'),bg="#EB998E",fg='black',relief=RAISED)
        self.sessiontime.place(x=330,y=673)
        Label(self.root,bg='black',width=1,height=4).place(x=310,y=0)
        Label(self.root,bg='black',width=1,height=4).place(x=430,y=0)
        self.clock=Label(self.root,font=("helvetica",20,'bold'),bg="#EB998E",fg="black",width=7,height=2)
        self.clock.place(x=314,y=-4)
        self.date=Label(self.root,fg="black",bg="#EB998E",font=("",20,'bold'),width=13,
                   height=1,relief=RAISED)
        self.date.place(x=70,y=12)
        style=ttk.Style()
        style.theme_use('clam')
        CalFrame=ttk.Frame(self.root) # The frame sits in window (main)
        CalFrame.place(height=200,width=300,rely=0,relx=.786) # Height and placement
        t=dt.date.today() # Get today date
        self.cal=Calendar(CalFrame,selectmode='day',year=t.year,month=t.month,day=t.day,firstweekday="monday",
                          background='#EB998E',foreground='black',date_pattern='dd/mm/yyyy')
        self.cal.pack(fill='both',expand=True) # Fill entire container
        Label(self.root,bg='black',width=1,height=50).place(x=1090,y=0)
        Button(self.root,text="Open Note",command=self.OpenNote,width=10,bg='#229954',fg='white').place(x=1117,y=210)
        Button(self.root,text="Save Note",command=self.SaveNote,width=10,bg='#229954',fg='white').place(x=1213,y=210)
        self.cfrmsave=Label(self.root,text="",bg='#6B8282',fg='green',font=('arial',10,'bold'),width=9)
        self.cfrmsave.place(x=1308,y=211) # Label to confirm saving edits to the txt file
        Button(self.root,text="Get Date",command=self.GetDate,width=10).place(x=1308,y=248)
        self.dispdate=Label(self.root,text="",bg='#6B8282',fg='black',font=('arial',10,'bold'),width=9)
        self.dispdate.place(x=1308,y=285)
        Button(self.root,text="Session Tracker",command=self.SessionTracker,width=24).place(x=1117,y=248)
        self.noten=Label(self.root,text="",bg='#6B8282',fg='white',font=("",12,'bold'),relief=RAISED)
        self.noten.place(x=1117,y=284)
        Label(self.root,bg='black',width=50).place(x=1100,y=318)
        Label(self.root,bg='#6B8282',width=50).place(x=1103,y=322)
        self.TblFrame=LabelFrame(self.root)
        self.TblFrame.place(height=520,width=444,rely=.0937,relx=0)
        self.FileFrame=LabelFrame(self.root,text="Timetable")
        self.FileFrame.place(height=80,width=444,rely=.835,relx=0)
        Button(self.FileFrame,text="Open",command=self.FileOpen).place(rely=.5,relx=.05)
        Button(self.FileFrame,text="Load",command=self.FileDat).place(rely=.5,relx=.2)
        Button(self.FileFrame,text="Clear",command=self.Purge).place(rely=.5,relx=.35)
        self.Lab1=Label(self.FileFrame,text="No File Selected")
        self.Lab1.place(rely=0,relx=0)
        self.Tree=ttk.Treeview(self.TblFrame)
        self.Tree.place(relheight=1,relwidth=1)
        self.ScrollYTbl=Scrollbar(self.TblFrame,orient="vertical",command=self.Tree.yview)
        self.ScrollXTbl=Scrollbar(self.TblFrame,orient="horizontal",command=self.Tree.xview)
        self.Tree.configure(xscrollcommand=self.ScrollXTbl.set,yscrollcommand=self.ScrollYTbl.set)
        self.ScrollXTbl.pack(side="bottom",fill="x")
        self.ScrollYTbl.pack(side="right",fill="y")
        self.TextFrame=LabelFrame(self.root)
        self.TextFrame.place(height=700,width=654,rely=0,relx=.317)
        self.ScrollYTxt=Scrollbar(self.TextFrame,orient="vertical")
        self.ScrollYTxt.pack(side=RIGHT,fill=Y)
        self.windtext=Text(self.TextFrame,font=('Helvetica',10),yscrollcommand=self.ScrollYTxt.set)
        self.windtext.pack(fill='both',expand=True)
        self.windtext.insert(END,'\n')
        #
        self.hour=StringVar()
        self.minute=StringVar()
        self.second=StringVar()
        self.hour.set("")
        self.minute.set("")
        self.second.set("")
        
        self.hrin=Entry(self.root,width=2,font=("Arial",18),textvariable=self.hour).place(x=1117,y=340)
        self.minin=Entry(self.root,width=2,font=("Arial",18),textvariable=self.minute).place(x=1200,y=340)
        self.secin=Entry(self.root,width=2,font=("Arial",18),textvariable=self.second).place(x=1300,y=340)
        
        self.startb=Button(self.root,text="Start",command=self.Start).place(x=1117,y=400)
        self.stopb=Button(self.root,text="Stop",command=self.Stop).place(x=1200,y=400)
        self.resetb=Button(self.root,text="Reset",command=self.Reset).place(x=1300,y=400)
        #
        self.logo=False
        self.quit=False
        self.root.protocol("WM_DELETE_WINDOW",self.Quit)
        self.SW=None
        self.clear=False
        self.tick=-1
        self.suspended = False
        
        entries = ['1117,Hour: ', '1200,Minute: ', '1300,Seconds: ']
        for i in entries:
            i, j = i.split(",")
            exec(f'Label(self.root,text="{j}",bg="grey",fg="white").place(x={i},y=320)')
        
        
        self.SessionClock()
        self.DigClockMain()
        self.CalMain()
        self.root.mainloop()
         
    def Start(self):
        if int(self.hour.get()) == 0 and int(self.minute.get()) == 0 and int(self.second.get()) == 0:
            messagebox.showinfo("Stopwatch", "Time not set.")
        elif int(self.hour.get()) < 0 or int(self.minute.get()) < 0 or int(self.second.get()) < 0:
            messagebox.showinfo("Stopwatch", "One or more values are less than zero.")
        else:
            self.suspended = False
            self.thread1=threading.Thread(target=self.Tick)
            self.thread1.start()
        
    def Tick(self):
        try:
            temp=int(self.hour.get())*3600+int(self.minute.get())*60+int(self.second.get())
        except:
            print("Invalid input.")
        while self.suspended == False and temp >-1:
            mins,secs=divmod(temp,60)
            hours=0
            if mins>60:
                hours,mins=divmod(mins,60)
            self.hour.set("{0:2d}".format(hours))
            self.minute.set("{0:2d}".format(mins))
            self.second.set("{0:2d}".format(secs))
            self.root.update()
            time.sleep(1)
            if (temp==0):
                messagebox.showinfo("Stopwatch","Time ended.")
            temp-=1
        
    def Stop(self):
        self.suspended = True
        
    def Reset(self):
        if self.suspended == True:
            self.hour.set(0)
            self.minute.set(0)
            self.second.set(0)
        else:
            messagebox.showinfo("Stopwatch","Stop timer before resetting.")
    
    def Logout(self,*args):
        ans=messagebox.askyesno("Logout","Do you want to log out?")
        if ans:
            self.logo=True # Logout status
            self.CalcTime()

    def Quit(self):
        dest=messagebox.askyesno("Quit","Quit window?")
        if dest:
            self.quit=True # Quit status
            self.CalcTime()

    def CalcTime(self):
        endsecs=round(time.time()) # Time on closing program
        tot=endsecs-self.startsecs # Total session time
        endtime=dt.datetime.now().strftime('%H:%M:%S') # End time
        date=f"{dt.datetime.now():%a %d %b %Y}" # The date
        if tot<10: # If session time is less than 10 seconds
            pass
        else:
            cur.execute(f"INSERT INTO sessions(start_time,end_time,secs,date,user_id) VALUES('{self.starttime}','{endtime}','{tot}','{date}','{self.UID}');")
            con.commit()
        if self.logo==True: # Logout status is true
            self.root.destroy()
            main.login()
        if self.quit==True: # Quit status is true
            self.root.destroy()

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
        
    def GetDate(self):
        self.dispdate.config(text=self.cal.get_date(),bg='white')

    def Count(self):
        self.cfrmsave['text']="Saved!" # Change label to read "Saved!"
        self.cfrmsave['bg']="white" # Change background to white
        time.sleep(3) # Sleep
        self.cfrmsave['text']="" # Revert text
        self.cfrmsave['bg']="#6B8282" # Revert background
        

    def SessionClock(self):
        secs=int(time.time()-self.startsecs) # Change in time from start to current
        mins,secs=divmod(secs,60)
        hrs,mins=divmod(mins,60)
        self.sessiontime.config(text="{0}:{1}:{2}".format(int(hrs),int(mins),int(secs))) # Insert into label
        self.sessiontime.after(100,self.SessionClock) # Refresh time

    def FileOpen(self):
        cwd=os.getcwd()
        self.OpenFile=filedialog.askopenfilename(initialdir=(cwd+'/dat/usr/'+self.UN+'/Timetables'),title="Select A File",
                                              filetype=(("All Files","*.xlsx,*xlsm,*xls,*xltx,*xlsb,*xltm"),("All Files","*.*")))
        self.OF=pathlib.Path(self.OpenFile)
        self.Lab1['text']=self.OF.name
        return None

    def FileDat(self):
        Path=self.OpenFile
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
        cwd=os.getcwd()
        cwd1=pathlib.Path(cwd+'/dat/usr/'+UN+'/Timetables')
        os.chdir(cwd1)
        if os.path.exists(self.OF.name):
            pass
        else:
            shutil.copy(self.OF,cwd1)
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
        
    def SessionTracker(self):
        if self.SW is None:
            self.SW=Toplevel(self.root)
            self.SW.protocol('WM_DELETE_WINDOW',self.rmwin)
            self.SW.title("Session Tracker")
            self.SW.geometry('250x230')
            self.SW.resizable(height=False,width=False)
            self.SW.configure(bg='grey')
            self.SW.iconbitmap('dat/chart ICO.ico')
            cur.execute(f"SELECT secs FROM sessions WHERE user_id='{self.UID}';")
            secs=[]
            for i in cur.fetchall():
                secs.append(i[0])
            
            total_score=0
            for i in secs:
                i*=.05
                total_score+=i
            high=max(secs)
            time_spent=str(high)
            highest_score=high*0.05
            total_time=0
            for i in secs:
                total_time+=i    
            cur.execute(f"SELECT session_id FROM sessions WHERE user_id='{self.UID}';")
            session_count=len(cur.fetchall())
            avg_time=total_time/session_count
            highest_score=str(round(highest_score,2))
            total_score=str(round(total_score,2))
            avg_time=str(round(avg_time))
            Label(self.SW,bg='black',height=20).place(x=115,y=0)
            Label(self.SW,text="Highest score :").place(x=15,y=15)
            Label(self.SW,text=(highest_score+" points")).place(x=135,y=15)
            Label(self.SW,text=">>Time spent :").place(x=15,y=50)
            Label(self.SW,text=(time_spent+" seconds")).place(x=135,y=50)            
            Label(self.SW,text="Total score :").place(x=15,y=85)
            Label(self.SW,text=(total_score+" points")).place(x=135,y=85)          
            Label(self.SW,text="Total time :").place(x=15,y=120)
            Label(self.SW,text=(str(total_time)+" seconds")).place(x=135,y=120)         
            Label(self.SW,text="Average time :").place(x=15,y=155)
            Label(self.SW,text=(avg_time+" seconds")).place(x=135,y=155)
            Label(self.SW,text="Session count :").place(x=15,y=190)
            Label(self.SW,text=(str(session_count)+" sesions")).place(x=135,y=190)           
            self.SW.mainloop()
    
    def rmwin(self):
        self.SW.destroy()
        self.SW=None

    class login():
        def __init__(self):
            self.root=Tk()
            self.root.title("Login Panel")
            self.root.geometry('355x220')
            self.root.resizable(height=False,width=False)
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
            img_reset=ImageTk.PhotoImage(file='dat/reset PNG.png')
            resetb=Button(self.root,text="",command=self.ResetPassword,image=img_reset)
            resetb.place(x=180,y=110)
            Button(self.root,text="Register",width=10,height=1,bg="grey",fg="white",
                   command=self.Register).place(x=20,y=175)
            self.loginb=Button(self.root,text="Login",width=10,height=1,bg="grey",fg="white",
                    command=self.AuthCred).place(x=125,y=175)
            self.root.bind('<Return>',self.AuthCred)
            Label(self.root,text=f"{dt.datetime.now():%a %b%d %Y}",fg="white",bg="grey",font=("",11),width=12,
                height=1).place(x=220,y=50)
            see_img=ImageTk.PhotoImage(file='dat/view PNG.png')
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

        def AuthCred(self,*args):
            self.UN=self.usrnme.get()
            self.PW=self.pswd.get()
            cur.execute(f"SELECT username FROM users WHERE username='{self.UN}' AND password='{self.PW}';")
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
            ques_img=ImageTk.PhotoImage(file='dat/question_mark PNG.png')
            ques=Button(self.root,text="",command=self.HelpRegister)
            ques.config(image=ques_img)
            ques.place(x=180,y=270)
            see1_img=ImageTk.PhotoImage(file='dat/view PNG.png')
            see1=Button(self.root,text="",command=self.ViewTopEye)
            see1.config(image=see1_img)
            see1.place(x=180,y=130)
            see2_img=ImageTk.PhotoImage(file='dat/view PNG.png')
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
                    cwd=os.getcwd() # Gets current working directory
                    os.chdir(cwd+'/dat/usr') # Change the current working directory to user folder
                    if os.path.exists(UName):
                        a=messagebox.showerror("Register Panel","Error occured creating user dir: User dir already exists.")
                        if a:
                            self.root.destroy()  
                    else: 
                        os.mkdir(UName) # Make a new directory by the username
                        os.chdir(cwd+'/dat/usr/'+UName)
                        os.mkdir("Timetables")
                        os.mkdir("Notes")
                        os.chdir(cwd) # Change back to the original directory
                        UID=random.randint(1000,9999)
                        cur.execute(f"SELECT security_code FROM users WHERE security_code='{UID}';")    
                        if not cur.fetchall():
                            cur.execute(f"INSERT INTO users(username,password,security_code) VALUES('{UName}','{PWord}','{UID}');")
                            con.commit()
                            Label(self.root,text=UID,font=("",9),bg='grey',fg='white',width=10).place(x=130,y=230)
                            messagebox.showwarning("Register Panel","Please take note of your security code then proceed to login.")
                            self.root.destroy()
                            main.login()
                        else:
                            messagebox.showinfo("Register Panel","An error has occured. Please try again.")

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
            see1_img=ImageTk.PhotoImage(file='dat/view PNG.png')
            see1=Button(self.root,text="",command=self.ViewTopEye)
            see1.config(image=see1_img)
            see1.place(x=180,y=130)
            see2_img=ImageTk.PhotoImage(file='dat/view PNG.png')
            see2=Button(self.root,text="",command=self.ViewBottomEye)
            see2.config(image=see2_img)
            see2.place(x=180,y=190)
            ques_img=ImageTk.PhotoImage(file='dat/question_mark PNG.png')
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

main.login()
