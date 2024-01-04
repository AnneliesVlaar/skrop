"""
Schematische Kunst van het Regelmatig Opgewekt Poetsen
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

import datetime
import csv

FIELDNAMES = ["task", "frequency", "begin"]
FONTSIZE = 16

def get_week_number():
    """Get current week number

    Returns:
        int: current week number
    """
    week_number = datetime.date.today().isocalendar()[1]
    return week_number


def get_today():
    """Get date of today in format date month (words) year

    Returns:
        string: date month (words) year
    """
    today = datetime.date.today()
    return today.strftime("%d %B %Y")


class Skrop(toga.App):
    def startup(self):
        """
        Construct and show the Skrop application.
        """

        self.create_main_window()
        self.create_week_box()
        self.create_today_box()
        self.create_date_box()

        self.open_data()
        self.initalize_tasks()
    
        self.create_task_box()
        self.create_overview_button()

        self.create_task_overview_box()

    def create_main_window(self):
        """Set main_box as main window
        """
        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=5, flex=1))
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()

    def create_today_box(self):
        """Create label with today's date
        """
        today = get_today()
        self.date_label = toga.Label(
            today, style=Pack(padding=(5, 5), flex=1, font_size=FONTSIZE)
        )

    def create_week_box(self):
        """Show the weeknumber and create button to go to current week
        """
        week_label = toga.Label(
            "Tasks of week: ",
            style=Pack(padding=(15, 5, 5), flex=1, font_size=FONTSIZE),
        )
        self.this_week_number = get_week_number()
        self.week_scroller = toga.NumberInput(
            style=Pack(flex=1, padding=5, width=50, font_size=FONTSIZE),
            step=1,
            min=0,
            max=52,
            value=self.this_week_number,
            on_change=self.week_scroller_handler
        )
        this_week_button = toga.Button(
            "This week",
            on_press=self.this_week_handler,
            style=Pack(padding=5, flex=1, font_size=FONTSIZE),
        )
        self.week_box = toga.Box(style=Pack(direction=ROW, flex=1))
        self.week_box.add(week_label, self.week_scroller, this_week_button)

    def create_date_box(self):
        """Layout today label and week box in main box
        """
        date_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        date_box.add(self.date_label)
        date_box.add(toga.Divider())
        date_box.add(self.week_box)

        self.main_box.add(date_box)

    def create_task_box(self):
        """Show the task of the week in detailed list
        """           
        task_box = toga.Box(style=Pack(direction=COLUMN, padding=5, flex=1))

        task_box.add(toga.Divider(), self.task_details)
        self.main_box.add(task_box)

    def create_overview_button(self):
        """Button to go to the whole list of takst
        """
        overview_task_button = toga.Button(
            "See all tasks",
            on_press=self.overview_tasks_handler,
            style=Pack(padding=5, flex=1, font_size=FONTSIZE),
        )
        self.main_box.add(overview_task_button)

    def create_task_overview_box(self):
        """Box to show all the tasks and add task functionallity
        """
        self.task_overview_box = toga.Box(
            style=Pack(direction=COLUMN, padding=5, flex=1)
        )
        self.task_overview_box.add(self.all_tasks)

        self.create_add_task_box()
        self.create_add_task_button()
        self.create_back_home_button()

    def create_add_task_box(self):
        """Layout labels above input to create add task functionallity.

        Labels and input for task, frequency and begin week are constructed. 
        """
        # task
        task_label_box = toga.Box(style=Pack(direction=COLUMN, padding=5, flex=1))
        add_task_label = toga.Label(
            "Task", style=Pack(padding=(5, 5), flex=1, font_size=FONTSIZE)
        )
        self.task = toga.TextInput(style=Pack(flex=1), placeholder="Task details")
        task_label_box.add(add_task_label, self.task)

        # frequency
        freqency_label_box = toga.Box(style=Pack(direction=COLUMN, padding=5, flex=1))
        add_frequency_label = toga.Label(
            "Frequency", style=Pack(padding=(5, 5), flex=1, font_size=FONTSIZE)
        )
        self.frequency = toga.NumberInput(style=Pack(flex=1), step=1, min=1)
        freqency_label_box.add(add_frequency_label, self.frequency)

        # begin
        begin_label_box = toga.Box(style=Pack(direction=COLUMN, padding=5, flex=1))
        add_begin_label = toga.Label(
            "Begin week", style=Pack(padding=(5, 5), flex=1, font_size=FONTSIZE)
        )
        self.begin = toga.NumberInput(style=Pack(flex=1), step=1, min=0)
        begin_label_box.add(add_begin_label, self.begin)

        # task, frequency, begin add to one box
        add_task_box = toga.Box(style=Pack(direction=ROW, padding=5))
        add_task_box.add(task_label_box, freqency_label_box, begin_label_box)
        self.task_overview_box.add(add_task_box)

    def create_add_task_button(self):
        """Add task button to box
        """
        add_task_button = toga.Button(
            "Add task",
            on_press=self.add_task,
            style=Pack(padding=5, font_size=FONTSIZE),
        )
        self.task_overview_box.add(add_task_button)

    def create_back_home_button(self):
        """Add button to show homepage to box
        """
        back_home_button = toga.Button(
            "Show this week tasks",
            on_press=self.back_to_homepage,
            style=Pack(padding=5, font_size=FONTSIZE),
        )

        self.task_overview_box.add(back_home_button)

    def open_data(self):
        """Open data with tasks from file

        File has name tasks.csv and contains heading see FIELDNAMES. 
        Content of the file is added as data to a table. 
        """
        try:
            self.paths.data.mkdir(exist_ok=True)
        except FileNotFoundError:
            print(f"Path: {self.paths.data} can't be created.")
        try:
            with open(self.paths.data / "tasks.csv", newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                headings = reader.fieldnames
                self.data = []
                for row in reader:
                    self.data.append(row)
        except FileNotFoundError:
            print(f"file not found at {self.paths.data}, creating new file...")
            # Create empty data file
            with open(self.paths.data / "tasks.csv", "w", newline="") as csvfile:
                headings = FIELDNAMES
                self.data = []
                writer = csv.DictWriter(csvfile, fieldnames=headings)
                writer.writeheader()

        # create Toga table from csv data file
        self.all_tasks = toga.Table(
            headings=FIELDNAMES,
            data=self.data,
            on_activate=self.confirm_delete_row,
            style=Pack(flex=1)
        )

    def initalize_tasks(self):
        """Create a DetailedList to show tasks of this week
        """
        self.task_details = toga.DetailedList(
            data=[],
            primary_action="Mark as done",
            on_primary_action=self.mark_task_done,
            style=Pack(flex=1)
        )
        self.determine_tasks()

    def determine_tasks(self):
        """Create a list of tasks that should be done in the week shown in the weekbox
        """
        self.task_details.data.clear()
        for row in self.all_tasks.data:
            if self.check_task(row.begin, row.frequency):
                self.task_details.data.append({"subtitle": row.task})

    def mark_task_done(self, widget, row):
        """Handler to add Done! to the title of the detailedlist

        Args:
            widget (): toga widget
            row (): current selection in the detailedlist 
        """
        row.title = "Done!"

    def write_data(self):
        """Save all tasks to csv file
        """
        with open(self.paths.data / "tasks.csv", "w", newline="") as csvfile:
            fieldnames = FIELDNAMES
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.all_tasks.data:
                writer.writerow(
                    {"task": row.task, "frequency": row.frequency, "begin": row.begin}
                )
        self.determine_tasks()

    def add_task(self, widget):
        """add task to all tasks table

        Args:
            widget (): toga widget
        """
        self.all_tasks.data.append(
            (self.task.value, self.frequency.value, self.begin.value)
        )

        # empty input fields after adding
        self.task.value = None
        self.frequency.value = None
        self.begin.value = None

        # save changes
        self.write_data()

    def confirm_delete_row(self, widget, row):
        """Show confirm dialog when row in all tasks table is tapped.

        Args:
            widget (): toga widget
            row (): current selected row in table
        """
        self.main_window.confirm_dialog(
            "Delete task?",
            f"Are you sure you want to delete: '{row.task}'?",
            on_result=self.delete_row,
        )

    def delete_row(self, widget, result):
        """Delete selected row in all tasks table when user confirmed

        Args:
            widget (): toga widget
            result (BOOL): True if user confirmed to delete task from table
        """
        if result:
            self.all_tasks.data.remove(self.all_tasks.selection)
            self.write_data()

    def check_task(self, begin, frequency):
        """Checks if task should be done in the stated week

        note: it not neccessarly checks against the current week,
        but against the week that is showed in the week box.

        Args:
            begin (int): week in which the task should start
            frequency (int): frequency (in weeks) with which the task should be repeated

        Returns:
            BOOL: True if task should be done in the stated week
        """
        is_week_task = False
        for moment in range(int(begin), 53, int(frequency)):
            if moment == self.week_scroller.value:
                is_week_task = True
        return is_week_task

    def week_scroller_handler(self, widget):
        """Updates task list when week value is changed

        Args:
            widget (): toga widget
        """
        self.determine_tasks()

    def this_week_handler(self, widget):
        """set week input value to current week number

        Args:
            widget (): toga widget
        """
        self.week_scroller.value = self.this_week_number

    def overview_tasks_handler(self, widget):
        """Show all tasks screen

        Args:
            widget (): toga widget
        """
        self.main_window.content = self.task_overview_box

    def back_to_homepage(self, widget):
        """Show start screen with task of the week

        Args:
            widget (): toga widget
        """
        self.main_window.content = self.main_box


def main():
    return Skrop()
