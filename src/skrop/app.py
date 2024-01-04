"""
Schematische Kunst van het Regelmatig Opgewekt Poetsen
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT, BOTTOM, TOP, CENTER

import datetime
import csv

def get_week_number():
    week_number = datetime.date.today().isocalendar()[1]
    return week_number

def get_today():
    today = datetime.date.today()
    return today.strftime('%d %B %Y')

class Skrop(toga.App):
    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=5))

        # Main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        # Week number
        self.this_week_number = get_week_number()
        self.week_scroller = toga.NumberInput(style=Pack(flex=1), step=1, min=0, max=52)
        self.week_scroller.value = self.this_week_number
        self.week_scroller.on_change = self.week_scroller_handler
        week_box = toga.Box(style=Pack(direction=ROW, padding=5))
        week_label = toga.Label(
            "This is week: ", style=Pack(padding=(5, 5))
        )
        week_box.add(week_label, self.week_scroller)

        # Today
        today = get_today()
        date_label = toga.Label(f"Today is: {today}.", style=Pack(padding=(5, 5)))

        # Date box
        date_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        date_box.add(week_box)
        date_box.add(toga.Divider())
        date_box.add(date_label)

        main_box.add(date_box)

        self.open_data()
        self.initalize_tasks()

        task_box = toga.Box(style=Pack(direction=COLUMN, padding=5, flex=2))
        task_box.add(toga.Divider())
        task_label = toga.Label("Task of this week:", style=Pack(padding=(5, 5)))
        task_box.add(task_label)
        self.task_details.style = Pack(height=250)
        task_box.add(self.task_details)
        main_box.add(task_box)

        table_box = toga.Box(style=Pack(direction=COLUMN, padding=5, flex=1, alignment=BOTTOM))
        table_box.add(toga.Divider())
        overview_label = toga.Label("Overview tasks:", style=Pack(padding=(5, 5)))
        table_box.add(overview_label)
        self.table.style = Pack(height=150)
        table_box.add(self.table)
        main_box.add(table_box)

        add_task_box = toga.Box(style=Pack(direction=ROW, padding=5, alignment=BOTTOM))
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
            data = self.data,
            on_activate=self.confirm_delete_row,)  

    def initalize_tasks(self):
        self.task_details = toga.DetailedList( 
            data=[], on_primary_action=self.delete_tasks
        )
        self.determine_tasks()

    def determine_tasks(self):
        self.task_details.data.clear()
        for row in self.table.data:
            if self.check_task(row.begin, row.frequency):
                self.task_details.data.append({"title": row.task})

    def delete_tasks(self):
        self.task_details.data.remove(self.task_details.selection)
    
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

    def confirm_delete_row(self, widget, row):
        self.main_window.confirm_dialog("Delete task?", f"Are you sure you want to delete: '{row.task}'?", on_result=self.delete_row)

    def delete_row(self, widget, result):
        if result:
            self.table.data.remove(self.table.selection)
            self.write_data()

    def check_task(self, begin, frequency):
        is_week_task = False
        for moment in range(int(begin), 53, int(frequency)):
            if moment == self.week_scroller.value:
                is_week_task = True
        return is_week_task
    
    def week_scroller_handler(self, widget):
        self.determine_tasks()

def main():
    return Skrop()
