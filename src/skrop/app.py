"""
Schematische Kunst van het Regelmatig Opgewekt Poetsen
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

import datetime
import csv

def get_week_number():
    week_number = datetime.date.today().isocalendar()[1]
    return week_number


def get_today():
    today = datetime.date.today()
    return today


def delete_detail(widget):
    print("hiep")


def Task_table():
    data = [
        {"task": "Wasmachine 90 graden", "frequency": 8, "begin": 0},
        {"task": "molton hoeslaken wassen (60 graden)", "frequency": 6, "begin": 3},
        {"task": "Matrassen draaien (z-as)", "frequency": 12, "begin": 3},
        {"task": "Matrassen keren (y-as)", "frequency": 12, "begin": 9},
    ]
    week = 27
    tasks = []
    for row in data:
        for moment in range(row["begin"], 53, row["frequency"]):
            if moment == week:
                tasks.append({"title": row["task"]})

    print(tasks)
    
    task_details = toga.DetailedList(
            data=tasks, 
            on_primary_action=delete_detail
        )
    return task_details


class Skrop(toga.App):
    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=5))

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        date_box = toga.Box(style=Pack(direction=COLUMN, padding=5))

        week_number = get_week_number()
        week_label = toga.Label(
            f"This is week: {week_number}.", style=Pack(padding=(5, 5))
        )
        today = get_today()
        date_label = toga.Label(f"Today is: {today}.", style=Pack(padding=(5, 5)))

        date_box.add(week_label)
        date_box.add(date_label)

        main_box.add(date_box)

        task_details = Task_table()
        
        # main_box.add(self.table)
        main_box.add(task_details)
    
        self.open_data()

    def open_data(self):
        try:
            self.paths.data.mkdir(exist_ok=True)
        except FileNotFoundError:
            print(f"Path: {self.paths.data} can't be created.")
        try:
            with open(self.paths.data / "tasks.csv", newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                headings = reader.fieldnames
                data = []
                for row in reader:
                    data.append(row)
        except FileNotFoundError:
            print(f"file not found at {self.paths.data}, creating new file...")
            # Create empty data file
            with open(self.paths.data / "tasks.csv", "w", newline='') as csvfile:
                headings = ['task', 'frequency', 'begin']
                data = []
                writer = csv.DictWriter(csvfile, fieldnames=headings)
                writer.writeheader()

        # create Toga table from csv data file  
        self.table = toga.Table(
            headings=headings,
            data = data,)
        for i in self.table.data:
            print(i)
    

    
    def write_data(self):
        with open(self.paths.data / "tasks.csv", "w", newline='') as csvfile:
            fieldnames = ['task', 'frequency', 'begin']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.table.data:
                writer.writerow({'task': row.task,'frequency': row.frequency, 'begin': row.begin})


def main():
    return Skrop()
