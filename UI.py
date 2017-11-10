import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi, cos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt
import random
import pandas as pd
from interpolation_module import save_interpolated_data, tabulate, tabulate_params, count_interpolant
from diff_solver_module import solve_diff
import numpy as np
from integral_module import count_integral

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
    global P_w_data
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


def get_input_func():
    top = Toplevel()
    top.title("Input functions parameters")

    hand_P_w_label = Label(top, text="P(w) coefficients")
    hand_P_w_label.grid(row=0, column=2, sticky="w")

    a = Label(top, text="Enter P's a:")
    b = Label(top, text="Enter P's b:")

    a_value = ""
    b_value = ""

    a.grid(row=1, column=0, sticky="w")
    b.grid(row=2, column=0, sticky="w")

    a_entry = Entry(top, textvariable=a_value)
    b_entry = Entry(top, textvariable=b_value)

    a_entry.grid(row=1, column=2, padx=2, pady=5)
    b_entry.grid(row=2, column=2, padx=2, pady=5)

    #---------

    hand_Z_t_label = Label(top, text="Z(t) coefficients")
    hand_Z_t_label.grid(row=3, column=2, sticky="w")

    a_Z = Label(top, text="Enter Z's a:")
    b_Z = Label(top, text="Enter Z's b:")

    a_value_Z = ""
    b_value_Z = ""

    a_Z.grid(row=4, column=0, sticky="w")
    b_Z.grid(row=5, column=0, sticky="w")

    a_entry_Z = Entry(top, textvariable=a_value)
    b_entry_Z = Entry(top, textvariable=b_value)

    a_entry_Z.grid(row=4, column=2, padx=2, pady=5)
    b_entry_Z.grid(row=5, column=2, padx=2, pady=5)

    #------------


    hand_S_t_label = Label(top, text="S(t) coefficients")
    hand_S_t_label.grid(row=6, column=2, sticky="w")

    a_S = Label(top, text="Enter S's a:")
    b_S = Label(top, text="Enter S's b:")

    a_value_S = ""
    b_value_S = ""

    a_S.grid(row=7, column=0, sticky="w")
    b_S.grid(row=8, column=0, sticky="w")

    a_entry_S = Entry(top, textvariable=a_value)
    b_entry_S = Entry(top, textvariable=b_value)

    a_entry_S.grid(row=7, column=2, padx=2, pady=5)
    b_entry_S.grid(row=8, column=2, padx=2, pady=5)

    def save_params():
        S_data = tabulate_params(a_value_S, b_value_S)
        Z_data = tabulate_params(a_value_Z, b_value_Z)
        P_data = tabulate_params(a_value, b_value)

        save_interpolated_data(S_data)
        save_interpolated_data(Z_data)
        save_interpolated_data(P_data)

    button = Button(top, text='Save', command=save_params)
    button.grid(row=9, column=2, sticky = "w")
    #button.pack(side = BOTTOM)


def tabulate_integral():
    top = Toplevel()
    top.title("Tabulate integral")
    button = Button(top, text='P(w)', command=get_P_W_data)
    button.grid(row=1, column=0, sticky="w")

    int_val = StringVar()

    int_val.set("Integral value")
    integral_value = Label(top, textvariable=int_val)
    integral_value.grid(row=2, column=1, sticky="w")

    def compute_integral():
        x, y = P_w_data['x'].values, P_w_data['y'].values
        int_val.set("Integral value: " + str(count_integral(y, x)))

    def count_interpolant_saver():
        count_interpolant(None)
        data = np.zeros((100))

        df = pd.DataFrame(data)
        df.to_csv("interpolant_data.csv")

    button = Button(top, text='Compute integral', command=compute_integral)
    button.grid(row=3, column=0, sticky="w")

    button = Button(top, text='Find coefficient', command=count_interpolant_saver)
    button.grid(row=4, column=0, sticky="w")


def cauchy_solver():
    top = Toplevel()
    top.title("Cauchy solver")

    param_label = Label(top, text="Parameter load")
    param_label.grid(row=0, column=1, sticky="w")

    x0 = Label(top, text="Enter X0:")
    y0 = Label(top, text="Enter Y0:")
    B_val = Label(top, text="Enter B:")
    T_val = Label(top, text="Enter T:")

    x0_value = ""
    y0_value = ""
    B_value = ""
    T_value = ""

    x0.grid(row=1, column=0, sticky="w")
    y0.grid(row=2, column=0, sticky="w")
    B_val.grid(row=3, column=0, sticky="w")
    T_val.grid(row=4, column=0, sticky="w")

    x0_entry = Entry(top, textvariable = x0_value)
    y0_entry = Entry(top, textvariable = y0_value)
    B_entry = Entry(top, textvariable=B_value)
    T_entry = Entry(top, textvariable=T_value)

    x0_entry.grid(row=1, column=2, padx=2, pady=5)
    y0_entry.grid(row=2, column=2, padx=2, pady=5)
    B_entry.grid(row=3, column=2, padx=2, pady=5)
    T_entry.grid(row=4, column=2, padx=2, pady=5)

    csv_label = Label(top, text="CSV load")
    csv_label.grid(row=5, column=1, sticky="w")
    button = Button(top, text='U(y)', command=get_P_W_data)
    # button.pack(side=LEFT)
    button.grid(row=6, column=0, sticky="w")

    button = Button(top, text='S(t)', command=get_Z_t_data)
    # button.pack(side=LEFT)
    button.grid(row=7, column=0, sticky="w")

    button = Button(top, text='z(t)', command=get_S_t_data)
    # button.pack(side=LEFT)
    button.grid(row=8, column=0, sticky="w")

    def solve_caushy_save():
        solve_diff(None)
        data = np.zeros((100))

        df = pd.DataFrame(data)
        df.to_csv("caushy_data.csv")

    button = Button(top, text='Solve!', command=solve_caushy_save)
    # button.pack(side=LEFT)
    button.grid(row=9, column=1, sticky="w")



def create_use_cases():
    top = Toplevel()
    top.title("Use cases")

    button = Button(top, text='Input functions', command=get_input_func)
    button.grid(row=0, column=0, sticky="w")


    button = Button(top, text='Tabulate integral', command=tabulate_integral)
    button.grid(row=1, column=0, sticky="w")


    button = Button(top, text='Cauchy solver', command=cauchy_solver)
    button.grid(row=2, column=0, sticky="w")


bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )


button = Button(bottomframe, text='Use cases', command = create_use_cases)
button.pack(side = LEFT)

button = Button(bottomframe, text='Load data', command = CreateNewWindow)
button.pack(side = LEFT)

button = Button(bottomframe, text='Solve', command = solve)
button.pack(side = LEFT)


button = Button(bottomframe, text='Quit', command=_quit)
button.pack(side = LEFT)



mainloop()