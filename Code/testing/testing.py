"""
import tkinter as tk

window = tk.Tk()

label = tk.Label(
    text="This is a label",
    fg="#ff1c51",
    bg="#7c90d9",
    height=20,
    width=20)

button = tk.Button(
    text="Hello",
    height=10,
    width=10,
    fg="black",
    bg="white")

entry = tk.Entry(
    width=20)

button.pack()
label.pack()
entry.pack()
window.mainloop()

import tkinter as tk

root = tk.Tk()

margin = 0.23
projectedSales = tk.IntVar()
profit = tk.IntVar()

entry = tk.Entry(root, textvariable=projectedSales)

entry.pack()

def profit_calculator():
    profit.set(margin * projectedSales.get())

labelProSales = tk.Label(root, textvariable=projectedSales)
labelProSales.pack()

labelProfit = tk.Label(root, textvariable=profit)
labelProfit.pack()

button_calc = tk.Button(root, text="Calculate", command=profit_calculator)
button_calc.pack()

root.mainloop()
"""


username=StringVar()
password=StringVar()

def AuthCred():
    UName=username.get()
    PWord=password.get()
    print(UName)

Label(login_screen,text="Username:",bg="grey",fg="white").place(x=20,y=55)
usrnme_inp=Entry(login_screen,textvariable="username",width=30)
usrnme_inp.place(x=20,y=75)

Label(login_screen, text="Password:",bg="grey",fg="white").place(x=20,y=115)
pw_inp=Entry(login_screen,textvariable="password",width=30,show='*')
pw_inp.place(x=20,y=135)

usr_reg=Button(login_screen,text="Register",width=10,height=1,bg="grey",fg="white"
               ).place(x=20,y=175)

usr_log=Button(login_screen,text="Login",width=10,height=1,bg="grey",fg="white",
               command=AuthCred).place(x=125,y=175)
