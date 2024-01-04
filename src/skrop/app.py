"""
Schematische Kunst van het Regelmatig Opgewekt Poetsen
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT, BOTTOM, TOP, CENTER

import datetime
import csv

FIELDNAMES = ['task', 'frequency', 'begin']
FONTSIZE = 16

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
        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=5, flex=1))

        # Main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()

        # Week number
        self.this_week_number = get_week_number()
        self.week_scroller = toga.NumberInput(style=Pack(flex=1, padding=5, width=50, font_size=FONTSIZE), step=1, min=0, max=52)
        self.week_scroller.value = self.this_week_number
        self.week_scroller.on_change = self.week_scroller_handler
        this_week_button = toga.Button(
            "This week",
            on_press=self.this_week_handler,
            style=Pack(padding=5, flex=1, font_size=FONTSIZE)
        )
        week_box = toga.Box(style=Pack(direction=ROW, flex=1))
        week_label = toga.Label(
            "Tasks of week: ", style=Pack(padding=(15, 5, 5), flex=1, font_size=FONTSIZE)
        )
        week_box.add(week_label, self.week_scroller, this_week_button)

        # Today
        today = get_today()
        date_label = toga.Label(today, style=Pack(padding=(5, 5), flex=1, font_size=FONTSIZE))

        # Date box
        date_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        date_box.add(date_label)
        date_box.add(toga.Divider())
        date_box.add(week_box)

        self.main_box.add(date_box)

        self.open_data()
        self.initalize_tasks()

        task_box = toga.Box(style=Pack(direction=COLUMN, padding=5, flex=1))
        self.task_details.style = Pack(flex=1)
        task_box.add(toga.Divider(), self.task_details)
        self.main_box.add(task_box)

        overview_task_button = toga.Button(
            "See all tasks",
            on_press=self.overview_tasks_handler,
            style=Pack(padding=5, flex=1, font_size=FONTSIZE)
        )
        self.main_box.add(overview_task_button)

        # Task overview
        self.task_overview_box = toga.Box(style=Pack(direction=COLUMN, padding=5, flex=1))

        table_box = toga.Box(style=Pack(direction=COLUMN, padding=5, flex=1))

        self.table.style = Pack(flex=1)
        table_box.add(self.table)
        self.task_overview_box.add(table_box)
        add_task_box = toga.Box(style=Pack(direction=ROW, padding=5))

        task_label_box = toga.Box(style=Pack(direction=COLUMN, padding=5, flex=1))
        add_task_label = toga.Label("Task", style=Pack(padding=(5, 5), flex=1, font_size=FONTSIZE))
        self.task = toga.TextInput(style=Pack(flex=1), placeholder="Task details")
        task_label_box.add(add_task_label, self.task)
        add_task_box.add(task_label_box)

        freqency_label_box = toga.Box(style=Pack(direction=COLUMN, padding=5, flex=1))
        add_frequency_label = toga.Label("Frequency", style=Pack(padding=(5, 5), flex=1, font_size=FONTSIZE))
        self.frequency = toga.NumberInput(style=Pack(flex=1), step=1, min=1)
        freqency_label_box.add(add_frequency_label, self.frequency)
        add_task_box.add(freqency_label_box)
        
        begin_label_box = toga.Box(style=Pack(direction=COLUMN, padding=5, flex=1))
        add_begin_label = toga.Label("Begin week", style=Pack(padding=(5, 5), flex=1, font_size=FONTSIZE))
        self.begin = toga.NumberInput(style=Pack(flex=1), step=1, min=0)
        begin_label_box.add(add_begin_label, self.begin)
        add_task_box.add(begin_label_box)

        self.task_overview_box.add(add_task_box)
        
        add_task_button = toga.Button(
            "Add task",
            on_press=self.add_task,
            style=Pack(padding=5, font_size=FONTSIZE)
        )
        self.task_overview_box.add(add_task_button)

        back_home = toga.Command(
        self.back_to_homepage, text="Back home", tooltip="Go back to homepage", order=1, group=toga.Group.HELP)
        toga.App.app.commands.add(back_home)
        
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
                headings = FIELDNAMES
                self.data = []
                writer = csv.DictWriter(csvfile, fieldnames=headings)
                writer.writeheader()

        # create Toga table from csv data file  
        self.table = toga.Table(
            headings=FIELDNAMES,
            data = self.data,
            on_activate=self.confirm_delete_row,)  

    def initalize_tasks(self):
        self.task_details = toga.DetailedList(
            data=[], primary_action='Mark as done', on_primary_action=self.mark_task_done
        )
        self.determine_tasks()

    def determine_tasks(self):
        self.task_details.data.clear()
        for row in self.table.data:
            if self.check_task(row.begin, row.frequency):
                self.task_details.data.append({"subtitle": row.task})

    def mark_task_done(self):
        print(self.task_details.selection)
        self.task_details.selection.subtitle = "Done"
    
    def write_data(self):
        with open(self.paths.data / "tasks.csv", "w", newline='') as csvfile:
            fieldnames = FIELDNAMES
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.table.data:
                writer.writerow({'task': row.task,'frequency': row.frequency, 'begin': row.begin})
        self.determine_tasks()

    def add_task(self, widget):
        self.table.data.append((self.task.value,self.frequency.value,self.begin.value))
        
        # empty input fields after adding
        self.task.value = None
        self.frequency.value = None
        self.begin.value = None
        
        # save changes
        self.write_data()

    def confirm_delete_row(self, widget, row):
        self.main_window.confirm_dialog("Delete task?", f"Are you sure you want to delete: '{row.task}'?", on_result=self.delete_row)

    def delete_row(self, widget, result):
        # remove row if user confirmed
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

    def this_week_handler(self, widget):
        self.week_scroller.value = self.this_week_number

    def overview_tasks_handler(self, widget):
        self.main_window.content = self.task_overview_box

    def back_to_homepage(self, widget):
        self.main_window.content =  self.main_box

def main():
    return Skrop()
