import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from advisor_solver import solve

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


f, axarr = plt.subplots(2, 3, )
f.tight_layout()

p_w = axarr[0, 0]
p_w.set_title("P(w)")

x_t = axarr[0, 1]
x_t.set_title("X(t) with Y(t)")

S_t = axarr[0, 2]
S_t.set_title("S(t)")

z_t = axarr[1, 0]
z_t.set_title("Z(t)")

x_t_S_t = axarr[1, 1]
x_t_S_t.set_title("X(t) - S(t)")

S_x = axarr[1, 2]
S_x.set_title("S(x)")

for i in range(2):
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


def solve_button():
    top = Toplevel()
    top.title("Load parameters")

    param_label = Label(top, text="Parameter load")
    param_label.grid(row=0, column=1, sticky="w")

    x0 = Label(top, text="Enter X0:")
    y0 = Label(top, text="Enter Y0:")
    pw_val = Label(top, text="Enter P(w):")
    z_val = Label(top, text="Enter z(t):")
    s_val = Label(top, text="Enter S(t):")
    T_val = Label(top, text="Enter T:")
    beta_from_val = Label(top, text="Enter B from:")
    beta_to_val = Label(top, text="Enter B to:")

    x0_value = ""
    y0_value = ""
    pw_value = ""
    z_value = ""
    s_value = ""
    T_value = ""
    beta_from_value = ""
    beta_to_value = "Single"

    x0.grid(row=1, column=0, sticky="w")
    y0.grid(row=2, column=0, sticky="w")
    pw_val.grid(row=3, column=0, sticky="w")
    z_val.grid(row=4, column=0, sticky="w")
    s_val.grid(row=5, column=0, sticky="w")
    T_val.grid(row=6, column=0, sticky="w")
    beta_from_val.grid(row=7, column=0, sticky="w")
    beta_to_val.grid(row=8, column=0, sticky="w")

    x0_entry = Entry(top, textvariable=x0_value)
    y0_entry = Entry(top, textvariable=y0_value)
    pw_entry = Entry(top, textvariable=pw_value)
    z_entry = Entry(top, textvariable=z_value)
    s_entry = Entry(top, textvariable=s_value)
    T_entry = Entry(top, textvariable=T_value)
    beta_from_entry = Entry(top, textvariable=beta_from_value)
    beta_to_entry = Entry(top, textvariable=beta_to_value)
    beta_to_entry.delete(0, END)
    beta_to_entry.insert(END, beta_to_value)

    x0_entry.grid(row=1, column=2, padx=2, pady=5)
    y0_entry.grid(row=2, column=2, padx=2, pady=5)
    pw_entry.grid(row=3, column=2, padx=2, pady=5)
    z_entry.grid(row=4, column=2, padx=2, pady=5)
    s_entry.grid(row=5, column=2, padx=2, pady=5)
    T_entry.grid(row=6, column=2, padx=2, pady=5)
    beta_from_entry.grid(row=7, column=2, padx=2, pady=5)
    beta_to_entry.grid(row=8, column=2, padx=2, pady=5)

    c1_val = StringVar()
    c2_val = StringVar()
    beta_val = StringVar()
    c1 = Label(top, textvariable=c1_val)
    c1.grid(row=9, column=1, sticky="w")
    c2 = Label(top, textvariable=c2_val)
    c2.grid(row=10, column=1, sticky="w")

    beta = Label(top, textvariable=beta_val)
    beta.grid(row=11, column=1, sticky="w")

    def solve_plot():
        A = 1
        B = 10
        beta_n = 10

        try:
            x0 = float(x0_entry.get())
            y0 = float(y0_entry.get())
            T = float(T_entry.get())
            beta_from = float(beta_from_entry.get())
            if beta_to_entry.get() != 'Single':
                beta_to = float(beta_to_entry.get())
            else:
                beta_to = None
            pw = pw_entry.get()
            S = s_entry.get()
            Z = z_entry.get()
            if beta_to:
                mode = True
            else:
                mode = False

            beta_opt, sol_x, sol_y, c1_opt, c2_opt = solve(x0, y0, T, A, B, pw,
                                                           S, Z, beta_from, beta_n, mode,
                                                           beta_to)
        except:
            messagebox.showinfo("Error", "Check input parameters!")
            return

        for i in range(2):
            for j in range(3):
                axarr[i, j].clear()

        p_w = axarr[0, 0]
        p_w.set_title("P(w)")
        x = np.linspace(0, T, 100)
        y = []
        for elem in x:
            w = elem
            y.append(eval(pw))
        p_w.plot(x, np.array(y))

        x_t = axarr[0, 1]
        x_t.set_title("X(t) with Y(T)")
        x_t_pred = sol_x.predict(x)
        x_t.plot(x, x_t_pred, label='X(T)')
        y_t_pred = sol_y.predict(x)
        x_t.plot(x, y_t_pred, label='Y(T)')
        x_t.legend()

        S_t = axarr[0, 2]
        S_t.set_title("S(t)")
        y = []
        for elem in x:
            t = elem
            y.append(eval(S))
        S_t_pred = np.array(y)
        S_t.plot(x, S_t_pred)

        z_t = axarr[1, 0]
        z_t.set_title("Z(t)")
        y = []
        for elem in x:
            t = elem
            y.append(eval(Z))
        z_t.plot(x, np.array(y))

        x_t_S_t = axarr[1, 1]
        x_t_S_t.set_title("X(t) - S(t)")
        x_t_S_t.plot(x, x_t_pred - S_t_pred)

        S_x = axarr[1, 2]
        S_x.set_title("S(x)")
        y = []
        for elem in x_t_pred:
            t = elem
            y.append(eval(S))
        S_x.plot(x_t_pred, np.array(y))

        canvas.draw()

        c1_val.set('C1: ' + str(c1_opt))
        c2_val.set('C1: ' + str(c2_opt))
        beta_val.set('Beta: ' + str(beta_opt))

    button = Button(top, text='Solve!', command=solve_plot)
    # button.pack(side=LEFT)
    button.grid(row=12, column=1, sticky="w")



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

# button = Button(bottomframe, text='Use cases', command = create_use_cases)
# button.pack(side = LEFT)

# button = Button(bottomframe, text='Load data', command = CreateNewWindow)
# button.pack(side = LEFT)

button = Button(bottomframe, text='Load parameters', command=solve_button)
button.pack(side = LEFT)


button = Button(bottomframe, text='Quit', command=_quit)
button.pack(side = LEFT)



mainloop()