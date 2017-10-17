import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi, cos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt
import random
import pandas as pd

from matplotlib.figure import Figure

import sys
import tkinter as Tk

from tkinter import *

from tkinter import messagebox

def _quit():
    root.quit()
    root.destroy()

root = Tk()
root.wm_title("Num methods project")
root.protocol('WM_DELETE_WINDOW', _quit)


#f = Figure(figsize=(5, 4), dpi=100)
#a = f.add_subplot(111)
t = arange(0.0, 3.0, 0.01)
s = sin(2*pi*t)

#a.plot(t, s)


f, axarr = plt.subplots(3, 3)
f.tight_layout()

p_w = axarr[0, 0]
p_w.set_title("P(w)")

x_t = axarr[0, 1]
x_t.set_title("X(t)")

S_t = axarr[0, 2]
S_t.set_title("S(t)")

z_t = axarr[1, 0]
z_t.set_title("Z(t)")

x_t_S_t = axarr[1, 1]
x_t_S_t.set_title("X(t) - S(t)")

y_t = axarr[1, 2]
y_t.set_title("Y(t)")

S_x = axarr[2, 0]
S_x.set_title("S(x)")

C1_b = axarr[2, 1]
C1_b.set_title("C1(b)")

C2_b = axarr[2, 2]
C2_b.set_title("C2(b)")


for i in range(3):
    for j in range(3):
        axarr[i,j].plot(t, sin(2*pi*t * (j * i + 1)))


# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

#toolbar = NavigationToolbar2TkAgg(canvas, root)
#toolbar.update()
canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)


def on_key_event(event):
    print('you pressed %s' % event.key)
    key_press_handler(event, canvas, toolbar)

canvas.mpl_connect('key_press_event', on_key_event)


def solve():
    for i in range(3):
        for j in range(3):
            axarr[i,j].clear()
            axarr[i, j].plot(t, cos(pi * t * (random.randint(1, 2) + 1)))
    canvas.draw()


global P_w_data, Z_t_data, S_t_data


def get_P_W_data():
    filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                               filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

    if ".csv" not in filename:
        data = None
        messagebox.showinfo("Error!", "Error in data selection!")
    else:
        data = pd.read_csv(filename)
        messagebox.showinfo("Succes", "Data was loaded succesfully!")
    P_w_data = data

def get_Z_t_data():
    filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                               filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

    if ".csv" not in filename:
        data = None
        messagebox.showinfo("Error!", "Error in data selection!")
    else:
        data = pd.read_csv(filename)
        messagebox.showinfo("Succes", "Data was loaded succesfully!")
    Z_t_data = data

def get_S_t_data():
    filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                               filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

    if ".csv" not in filename:
        data = None
        messagebox.showinfo("Error!", "Error in data selection!")
    else:
        data = pd.read_csv(filename)
        messagebox.showinfo("Succes", "Data was loaded succesfully!")
    S_t_data = data

def CreateNewWindow():
    top = Toplevel()
    top.title("Load Data page")

    csv_label = Label(top, text="CSV load")
    csv_label.grid(row = 0, column = 1, sticky = "w")
    button = Button(top, text='P(w)', command=get_P_W_data)
    #button.pack(side=LEFT)
    button.grid(row = 1, column = 0, sticky = "w")

    button = Button(top, text='Z(t)', command=get_Z_t_data)
    #button.pack(side=LEFT)
    button.grid(row=1, column=1, sticky="w")

    button = Button(top, text='S(t)', command=get_S_t_data)
    #button.pack(side=LEFT)
    button.grid(row=1, column=2, sticky="w")

    hand_P_w_label = Label(top, text="P(w) coefficients")
    hand_P_w_label.grid(row=2, column=2, sticky="w")

    a = Label(top, text="Enter a:")
    b = Label(top, text="Enter b:")

    a_value = ""
    b_value = ""

    a.grid(row=3, column=0, sticky="w")
    b.grid(row=4, column=0, sticky="w")

    a_entry = Entry(top, textvariable=a_value)
    b_entry = Entry(top, textvariable=b_value)

    a_entry.grid(row=3, column=2, padx=2, pady=5)
    b_entry.grid(row=4, column=2, padx=2, pady=5)

bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )


button = Button(bottomframe, text='Load data', command=CreateNewWindow)
button.pack(side = LEFT)

button = Button(bottomframe, text='Solve', command=solve)
button.pack(side = LEFT)


button = Button(bottomframe, text='Quit', command=_quit)
button.pack(side = LEFT)



mainloop()