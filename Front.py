from tkinter import *
from tkmacosx import Button  


def clear_main_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

# Side Bar Function
def side_bar():
    side_bar_frame = Frame(t, width=300, bg="#1B1B1B")
    side_bar_frame.pack(side=LEFT, fill=Y)
    side_bar_frame.pack_propagate(False)

    menu_label = Label(side_bar_frame, text="Menu", font=("Arial", 36, "bold"), bg="#1B1B1B", fg="white")
    menu_label.pack(pady=20, padx=10)

    home_btn = Button(
        side_bar_frame,
        text="HOME",
        relief=SUNKEN,
        background="#000000",
        activebackground="#222222",
        fg="white",
        font=("Arial", 12),
        borderless=1,
        command=home_screen
    )
    home_btn.pack(fill=X, pady=2)

    sett_btn = Button(
        side_bar_frame,
        text="SETTINGS",
        relief=SUNKEN,
        background="#000000",
        activebackground="#222222",
        fg="white",
        font=("Arial", 12),
        borderless=1,
        command=sett_screen
    )
    sett_btn.pack(fill=X, pady=2)


# Main Content Frame Function
def Main_bar():
    global main_frame
    main_frame = Frame(t, bg="#111010")
    main_frame.pack(side=RIGHT, fill=BOTH, expand=True)
    
    welcome_lbl = Label(main_frame, text="Dashboard Area", font=("Arial", 24), bg="#111010", fg="gray")
    welcome_lbl.pack(expand=True)
    home_screen()

def home_screen():
    clear_main_frame()
    title = Label(main_frame, text="Welcome Home", font=("Arial", 32, "bold"), bg="#111010", fg="white")
    title.pack(pady=40, anchor=W, padx=40)
    
def sett_screen():
    clear_main_frame()
    title = Label(main_frame, text="System Settings", font=("Arial", 32, "bold"), bg="#111010", fg="white")
    title.pack(pady=40, anchor=W, padx=40)
    


# Main Window Setup
t = Tk()
t["bg"] = "#111010"
t.geometry("1515x1000+0+0")

side_bar()
Main_bar()

t.mainloop()
