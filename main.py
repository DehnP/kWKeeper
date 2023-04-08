import tkinter
import tkinter.messagebox
import customtkinter
import sqlite3
import datetime
from header import *
from readings import *
from analytics import *
from graphs import *

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class DatabaseManager:
    def __init__(self):
        self._create_db_connection()
        self._create_db_table()

    def _create_db_connection(self):
        self.conn = sqlite3.connect('readings.db')
        self.cursor = self.conn.cursor()

    def _create_db_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS readings
                            (reading REAL, date text)''')
        self.conn.commit()


class App(customtkinter.CTk, DatabaseManager):
    def __init__(self):
        customtkinter.CTk.__init__(self)
        DatabaseManager.__init__(self)
        self.standing_charge = 0.46
        self.price_per_unit = 0.34
        self.date_labels = []
        # configure window
        self.title("CTK Meter Reading Tracker")
        # create widgets
        self.create_widgets()
        self._display_readings()

    def create_widgets(self):
        create_header(self)
        create_readings(self)
        create_analytics(self)
        create_graphs(self)

    def _display_readings(self):
        self.date_labels = []
        self.listbox.delete(0, tkinter.END)
        self.cursor.execute("SELECT * FROM readings")
        readings = self.cursor.fetchall()
        # Sort the readings by date in the format 'ddmmyyyy'
        readings.sort(key=lambda x: datetime.datetime.strptime(x[1], '%d-%m-%Y'))
        for i in range(len(readings)):
            if i > 0:
                diff = readings[i][0] - readings[i-1][0]
                tkinter.Label(self.date_frame, text=readings[i][1], width=15, anchor='center').grid(row=i+1, column=0)
                tkinter.Label(self.reading_frame, text=readings[i][0], width=15, anchor='center').grid(row=i+1, column=1)
                tkinter.Label(self.diff_frame, text=diff, width=15, anchor='center').grid(row=i+1, column=2)
                # calculate the cost per day
                date1 = datetime.datetime.strptime(readings[i][1], '%d-%m-%Y')
                date2 = datetime.datetime.strptime(readings[i-1][1], '%d-%m-%Y')
                days = (date1 - date2).days
                tkinter.Label(self.cost_diff_frame, text=round(diff * self.price_per_unit + (self.standing_charge*days), 2), width=15, anchor='center').grid(row=i+1, column=3)
                cost_per_day = round((diff * self.price_per_unit / days) + self.standing_charge, 2)
                tkinter.Label(self.cost_per_day_frame, text=cost_per_day, width=15, anchor='center').grid(row=i+1, column=4)

            else:
                tkinter.Label(self.date_frame, text=readings[i][1], width=15, anchor='center').grid(row=i+1, column=0)
                tkinter.Label(self.reading_frame, text=readings[i][0], width=15, anchor='center').grid(row=i+1, column=1)
                tkinter.Label(self.diff_frame, text="N/A", width=15, anchor='center').grid(row=i+1, column=2)
                tkinter.Label(self.cost_diff_frame, text="N/A", width=15, anchor='center').grid(row=i+1, column=3)
                tkinter.Label(self.cost_per_day_frame, text="N/A", width=15, anchor='center').grid(row=i+1, column=4)
        
        self.listbox.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        for i in range(len(readings)):
            date_label = tkinter.Label(self.date_frame, text=readings[i][1], width=15, anchor='center')
            date_label.grid(row=i+1, column=0)
            self.date_labels.append((date_label, readings[i][1]))
            date_label.bind("<Button-3>", self._remove_entry)

    def _add_reading(self):
        date = datetime.datetime.now().strftime("%d-%m-%Y")
        dialog = customtkinter.CTkInputDialog(text="Enter Today's Reading:", title=date)
        reading = dialog.get_input()
        if reading.isdigit():
            reading = int(reading)
            self.cursor.execute('''INSERT INTO readings(reading, date)
                                VALUES(?,?)''', (reading, date))
            self.conn.commit()
            self._display_readings()

    def _add_legacy_reading(self):
        dialog = customtkinter.CTkInputDialog(text="Enter Reading:", title="Add Legacy Reading")
        reading = dialog.get_input()
        if reading.isdigit():
            reading = int(reading)
            dialog = customtkinter.CTkInputDialog(text="Enter Date:", title="Add Legacy Reading")
            date = dialog.get_input()
            try:
                datetime.datetime.strptime(date, '%d-%m-%Y')
                self.cursor.execute('''INSERT INTO readings(reading, date)
                                    VALUES(?,?)''', (reading, date))
                self.conn.commit()
                self._display_readings()
            except ValueError:
                tkinter.messagebox.showerror("Error", "Invalid date format. Please use the format 'dd-mm-yyyy'")

    def _remove_entry(self, event):
        confirm = tkinter.messagebox.askyesno("Confirmation", "Do you want to delete this entry?")
        if confirm:
            widget = event.widget
            date_to_delete = None
            for date_label, date in self.date_labels:
                if date_label == widget:
                    date_to_delete = date
                    break
            if date_to_delete:
                self.cursor.execute("DELETE FROM readings WHERE date=?", (date_to_delete,))
                self.conn.commit()
                self._display_readings()

    def _get_avg_daily_consumption(self):
        self.cursor.execute("SELECT * FROM readings")
        readings = self.cursor.fetchall()
        if len(readings) > 1:
            readings.sort(key=lambda x: datetime.datetime.strptime(x[1], '%d-%m-%Y'))
            total_days = (datetime.datetime.strptime(readings[-1][1], '%d-%m-%Y') - datetime.datetime.strptime(readings[0][1], '%d-%m-%Y')).days
            total_consumption = readings[-1][0] - readings[0][0]
            return round(total_consumption / total_days,2)
        else:
            return "N/A"

    def _get_avg_daily_cost(self, avg_daily_consump, price_per_unit):
        if avg_daily_consump != "N/A":
            return round(avg_daily_consump * price_per_unit + self.standing_charge,2)
        else:
            return "N/A"

    def _plot_readings_vs_time(self):
        import matplotlib.dates as mdates
        self.cursor.execute("SELECT * FROM readings")
        readings = self.cursor.fetchall()
        if len(readings) > 1:
            readings.sort(key=lambda x: datetime.datetime.strptime(x[1], '%d-%m-%Y'))
            dates = [datetime.datetime.strptime(reading[1], '%d-%m-%Y') for reading in readings]
            readings = [reading[0] for reading in readings]
            # zero the y-axis
            readings = [r - readings[0] for r in readings]
            self.fig.clf()
            self.axes = self.fig.add_subplot(111)
            self.axes.plot(dates, readings)
            self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%b - %y'))
            self.axes.xaxis.set_major_locator(mdates.MonthLocator(interval=2))     
            # add labels
            self.axes.set_ylabel("Reading (kWh)")
            self.axes.set_title("Readings vs Time")
            self.axes.grid(axis='y', linestyle='--', alpha=0.7)
            self.canvas.draw()
        else:
            tkinter.messagebox.showerror("Error", "Not enough data to plot graph")

    def _plot_daily_consumption_vs_time(self):
        import matplotlib.dates as mdates
        self.cursor.execute("SELECT * FROM readings")
        readings = self.cursor.fetchall()
        if len(readings) > 1:
            readings.sort(key=lambda x: datetime.datetime.strptime(x[1], '%d-%m-%Y'))
            dates = [datetime.datetime.strptime(reading[1], '%d-%m-%Y') for reading in readings]
            readings = [reading[0] for reading in readings]
            daily_consumption = [(readings[i+1] - readings[i]) / (dates[i+1] - dates[i]).days for i in range(len(readings)-1)]
            self.fig.clf()
            self.axes = self.fig.add_subplot(111)
            self.axes.plot(dates[1:], daily_consumption)
            self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%b - %y'))
            self.axes.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
            # add labels
            self.axes.set_ylabel("Daily Consumption (kWh)")
            self.axes.set_title("Daily Consumption vs Time")
            self.axes.grid(axis='y', linestyle='--', alpha=0.7)
            self.canvas.draw()
        else:
            tkinter.messagebox.showerror("Error", "Not enough data to plot graph")

    def _plot_daily_cost_vs_time(self):
        import matplotlib.dates as mdates
        self.cursor.execute("SELECT * FROM readings")
        readings = self.cursor.fetchall()
        if len(readings) > 1:
            readings.sort(key=lambda x: datetime.datetime.strptime(x[1], '%d-%m-%Y'))
            dates = [datetime.datetime.strptime(reading[1], '%d-%m-%Y') for reading in readings]
            readings = [reading[0] for reading in readings]
            daily_consumption = [(readings[i+1] - readings[i]) / (dates[i+1] - dates[i]).days for i in range(len(readings)-1)]
            daily_cost = [consumption * self.price_per_unit + self.standing_charge for consumption in daily_consumption]
            self.fig.clf()
            self.axes = self.fig.add_subplot(111)
            self.axes.plot(dates[1:], daily_cost)
            self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%b - %y'))
             # set tick interval to every other month
            self.axes.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
            # add labels
            self.axes.set_ylabel("Daily Cost (£)")
            self.axes.set_title("Daily Cost vs Time")
            self.axes.grid(axis='y', linestyle='--', alpha=0.7)
            self.canvas.draw()
        else:
            tkinter.messagebox.showerror("Error", "Not enough data to plot graph")


if __name__ == "__main__":
    app = App()
    app.mainloop()
