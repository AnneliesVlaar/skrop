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
    return today.strftime('%d %B %Y')


def delete_detail(widget):
    print("Deleted task from task table")


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

        self.week_number = get_week_number()
        week_label = toga.Label(
            f"This is week: {self.week_number}.", style=Pack(padding=(5, 5))
        )
        today = get_today()
        date_label = toga.Label(f"Today is: {today}.", style=Pack(padding=(5, 5)))

        date_box.add(week_label)
        date_box.add(toga.Divider())
        date_box.add(date_label)

        main_box.add(date_box)

        self.open_data()
        self.determine_tasks()

        main_box.add(toga.Divider())
        task_label = toga.Label("Task of this week:", style=Pack(padding=(5, 5)))
        main_box.add(task_label)
        main_box.add(self.task_details)

        main_box.add(toga.Divider())
        overview_label = toga.Label("Overview tasks:", style=Pack(padding=(5, 5)))
        main_box.add(overview_label)
        main_box.add(self.table)

        add_task_box = toga.Box(style=Pack(direction=ROW, padding=5))
        self.task = toga.TextInput(style=Pack(flex=1), placeholder="Task details")
        add_task_box.add(self.task)
        self.frequency = toga.NumberInput(style=Pack(flex=1), step=1, min=1)
        add_task_box.add(self.frequency)
        self.begin = toga.NumberInput(style=Pack(flex=1), step=1, min=0)
        add_task_box.add(self.begin)

        main_box.add(add_task_box)
        
        add_task_button = toga.Button(
            "Add task",
            on_press=self.add_task,
            style=Pack(padding=5)
        )
        main_box.add(add_task_button)

    def open_data(self):
        try:
            self.paths.data.mkdir(exist_ok=True)
        except FileNotFoundError:
            print(f"Path: {self.paths.data} can't be created.")
        try:
            with open(self.paths.data / "tasks.csv", newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                headings = reader.fieldnames
                self.data = []
                for row in reader:
                    self.data.append(row)
        except FileNotFoundError:
            print(f"file not found at {self.paths.data}, creating new file...")
            # Create empty data file
            with open(self.paths.data / "tasks.csv", "w", newline='') as csvfile:
                headings = ['task', 'frequency', 'begin']
                self.data = []
                writer = csv.DictWriter(csvfile, fieldnames=headings)
                writer.writeheader()

        # create Toga table from csv data file  
        self.table = toga.Table(
            headings=headings,
            data = self.data,)  

    def determine_tasks(self):
        tasks = []
        for row in self.data:
            for moment in range(int(row["begin"]), 53, int(row["frequency"])):
                if moment == self.week_number:
                    tasks.append({"title": row["task"]})
        
        self.task_details = toga.DetailedList(
                data=tasks, 
                on_primary_action=delete_detail
            )
        print(self.task_details.data.append())
    
    def write_data(self):
        with open(self.paths.data / "tasks.csv", "w", newline='') as csvfile:
            fieldnames = ['task', 'frequency', 'begin']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.table.data:
                writer.writerow({'task': row.task,'frequency': row.frequency, 'begin': row.begin})
        self.determine_tasks()

    def add_task(self, widget):
        self.table.data.append((self.task.value,self.frequency.value,self.begin.value))
        self.write_data()




def main():
    return Skrop()
