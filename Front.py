from tkinter import *
from tkinter import ttk
from tkmacosx import Button 
import Back as bk


def clear_main_frame():
    for widget in main_bar.winfo_children():
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
    global main_bar
    main_bar = Frame(t, bg="#111010")
    main_bar.pack(side=RIGHT, fill=BOTH, expand=True)
    
    welcome_lbl = Label(main_bar, text="Dashboard Area", font=("Arial", 24), bg="#111010", fg="gray")
    welcome_lbl.pack(expand=True)
    home_screen()

def home_screen():
    clear_main_frame()
    title = Label(main_bar, text="Welcome Home", font=("Arial", 32, "bold"), bg="#111010", fg="white")
    title.pack(pady=40, anchor=W, padx=40)
    
def sett_screen():
    clear_main_frame()
    title = Label(main_bar, text="System Settings", font=("Arial", 32, "bold"), bg="#111010", fg="white")
    title.pack(pady=40, anchor=W, padx=40)

    k=Frame(main_bar,bg='#1e1e1e')
    k.pack()

    choose_label=Label(k,text='Choose an Action To Perform',width=30)
    choose_label.pack(side=LEFT,padx=10,pady=10,anchor=N)

    n=StringVar()
    choice_box=ttk.Combobox(k,textvariable=n,width=50)
    choice_box['values']=("Sort files","Delete Duplicate Files")
    choice_box['state']='readonly'
    choice_box.pack(side=LEFT,padx=10,pady=10,anchor=N)

    apply_btn=Button(main_bar,text='APPLY',fg='white',bg="#0D1A46",command=bk.apply(choice_box))
    apply_btn.pack(side=TOP,padx=10,pady=10)


# Main Window Setup
def run():
    global t
    t = Tk()
    t["bg"] = "#111010"
    t.geometry("1515x1000+0+0")

    side_bar()
    Main_bar()

    t.mainloop()
run()
