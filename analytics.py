import tkinter
import customtkinter

def create_analytics(App: customtkinter.CTk) -> None:
    # create a frame in tabview tab "Analytics"
    App.analytics_frame = tkinter.Frame(App.tab_view.tab("Analytics"))
    App.analytics_frame.grid(row=0, column=0)

    # create an average daily consumption label
    tkinter.Label(App.analytics_frame, text="Average Daily Consumption (kWh)", width=50, anchor='center', font=("Arial", 12, "bold"),bg="lightgray").grid(row=0, column=0)
    avg_daily_consump = App._get_avg_daily_consumption()
    App.avg_daily_consumption = tkinter.Label(App.analytics_frame, text=avg_daily_consump, width=50, anchor='center', font=("Arial", 12, "bold"))
    App.avg_daily_consumption.grid(row=1, column=0)

    # create an average daily cost label
    tkinter.Label(App.analytics_frame, text="Average Daily Cost (£)", width=50, anchor='center', font=("Arial", 12, "bold"),bg="lightgray").grid(row=2, column=0)
    avg_daily_cost = App._get_avg_daily_cost(avg_daily_consump, 0.34)
    App.avg_daily_cost = tkinter.Label(App.analytics_frame, text=avg_daily_cost, width=50, anchor='center', font=("Arial", 12, "bold"))
    App.avg_daily_cost.grid(row=3, column=0)

    # create an average weekly cost label
    tkinter.Label(App.analytics_frame, text="Average Weekly Cost (£)", width=50, anchor='center', font=("Arial", 12, "bold"),bg="lightgray").grid(row=4, column=0)
    avg_weekly_cost = round(avg_daily_cost * 7,2)
    App.avg_weekly_cost = tkinter.Label(App.analytics_frame, text=avg_weekly_cost, width=50, anchor='center', font=("Arial", 12, "bold"))
    App.avg_weekly_cost.grid(row=5, column=0)

    # create an average monthly cost label
    tkinter.Label(App.analytics_frame, text="Average Monthly(30d) Cost (£)", width=50, anchor='center', font=("Arial", 12, "bold"),bg="lightgray").grid(row=6, column=0)
    avg_monthly_cost = round(avg_daily_cost * 30,2)
    App.avg_monthly_cost = tkinter.Label(App.analytics_frame, text=avg_monthly_cost, width=50, anchor='center', font=("Arial", 12, "bold"))
    App.avg_monthly_cost.grid(row=7, column=0)