"""
Schematische Kunst van het Regelmatig Opgewekt Poetsen
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

import datetime

def get_week_number():
    week_number = datetime.date.today().isocalendar()[1]
    return f"This is week: {week_number}."

def get_today():
    today = datetime.date.today()
    return f"Today is: {today}."


class Skrop(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box()

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        date_box = toga.Box(style=Pack(direction=COLUMN, padding=5))

        week_label = toga.Label(get_week_number(), style=Pack(padding=(0, 5)))
        date_label = toga.Label(get_today(), style=Pack(padding=(0, 5)))

        date_box.add(week_label)
        date_box.add(date_label)

        main_box.add(date_box)

def main():
    return Skrop()
