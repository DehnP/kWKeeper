import tkinter
import customtkinter

def create_readings(App: customtkinter.CTk) -> None:
            # create listbox in tabview tab "Readings"
    App.listbox = tkinter.Listbox(App.tab_view.tab("Readings"), width=50, height=20)
    # Populate listbox

    App.date_frame = tkinter.Frame(App.listbox)
    App.date_frame.grid(row=0, column=0)
    tkinter.Label(App.date_frame, text="Date", width=15, anchor='center', font=("Arial", 12, "bold"),bg="lightgray").grid(row=0, column=0)
    App.date_frame.bind("<Button-3>", App._remove_entry) # bind right click to remove entry

    App.reading_frame = tkinter.Frame(App.listbox)
    App.reading_frame.grid(row=0, column=1)
    tkinter.Label(App.reading_frame, text="Reading (kWh)", width=15, anchor='center', font=("Arial", 12, "bold"),bg="gray").grid(row=0, column=1)


    App.diff_frame = tkinter.Frame(App.listbox)
    App.diff_frame.grid(row=0, column=2)
    tkinter.Label(App.diff_frame, text="Difference (kWh)", width=15, anchor='center', font=("Arial", 12, "bold"),bg="lightgray").grid(row=0, column=2)

    App.cost_diff_frame = tkinter.Frame(App.listbox)
    App.cost_diff_frame.grid(row=0,column=3)
    tkinter.Label(App.cost_diff_frame, text = "Cost (£)", width=15, anchor='center', font=("Arial",12,"bold"),bg="gray").grid(row=0,column=3)

    App.cost_per_day_frame = tkinter.Frame(App.listbox)
    App.cost_per_day_frame.grid(row=0,column=4)
    tkinter.Label(App.cost_per_day_frame, text = "Cost/day (£)", width=15, anchor='center', font=("Arial",12,"bold"),bg="lightgray").grid(row=0,column=4)