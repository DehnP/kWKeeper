from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import customtkinter

def create_graphs(App: customtkinter.CTk) -> None:
    # create a figure for graphing on tabview tab "Graphs"
    App.fig = Figure(figsize=(5, 4), dpi=100)
    App.ax = App.fig.add_subplot(111)
    App.canvas = FigureCanvasTkAgg(App.fig, master=App.tab_view.tab("Graphs"))
    App.canvas.draw()
    App.canvas.get_tk_widget().grid(row=0, column=0)
    
    # create a button to plot Readings vs time
    App.plot_button = customtkinter.CTkButton(App.tab_view.tab("Graphs"), text="Plot Readings vs Time", command=App._plot_readings_vs_time)
    App.plot_button.grid(row=1, column=0, pady=(20, 20))

    # create a button to plot daily consumption vs time
    App.plot_button = customtkinter.CTkButton(App.tab_view.tab("Graphs"), text="Plot Daily Consumption vs Time", command=App._plot_daily_consumption_vs_time)
    App.plot_button.grid(row=2, column=0, pady=(20, 20))

    # create a button to plot daily cost vs time
    App.plot_button = customtkinter.CTkButton(App.tab_view.tab("Graphs"), text="Plot Daily Cost vs Time", command=App._plot_daily_cost_vs_time)
    App.plot_button.grid(row=3, column=0, pady=(20, 20))
    