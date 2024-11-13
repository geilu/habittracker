import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QDate
from datetime import datetime
from habittracker import Habit

class HabitTrackerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tracker = Habit()
        self.tracker.load_data()
        self.current_month = datetime.now().strftime('%B')
        self.days_in_month = datetime.now().day

        self.setWindowTitle('Habit Tracker')
        self.setGeometry(100, 100, 1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        #tabs
        self.tabs = QTabWidget()
        self.habit_tab = QWidget()
        self.tabs.addTab(self.habit_tab, 'Habits')
        self.manage_tab = QWidget()
        self.tabs.addTab(self.manage_tab, 'Manage habits')
        self.main_layout.addWidget(self.tabs)

        self.habit_tab_layout = QHBoxLayout()
        self.habit_tab.setLayout(self.habit_tab_layout)
        self.habit_tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        #scroll area kus need kuupäevad jm on
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.habit_tab_layout.addWidget(self.scroll_area)

        #habit list ja grid
        self.grid_layout = QGridLayout()
        self.scroll_layout.addLayout(self.grid_layout)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.generate_calendar_grid()

        #save button
        self.save_button = QPushButton()
        self.save_button.clicked.connect(self.save_data)
    
    def generate_calendar_grid(self):
        self.grid_layout.setSpacing(5)
        current_date = QDate.currentDate()
        days_in_month = current_date.daysInMonth()
        month_name = current_date.toString('MMMM')

        month_label = QLabel(month_name)
        month_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        month_label.setStyleSheet('font-weight: bold; font-size: 16px;')
        self.grid_layout.addWidget(month_label, 0, 0, 1, days_in_month+1)

        for day in range(1, days_in_month+1):
            day_label = QLabel(str(day))
            day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(day_label, 1, day)

        for row, habit in enumerate(self.tracker.habits.keys(), start=2):
            habit_label = QLabel(habit)
            habit_label.setFixedWidth(100)
            habit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(habit_label, row, 0)

            for day in range(1, days_in_month+1):
                completion_button = QPushButton()
                completion_button.setFixedSize(30, 30)
                completion_button.setCheckable(True)

                date = f'{month_name} {day}'
                habit_completion_dates = self.tracker.habits.get(habit)
                if date in habit_completion_dates:
                    completion_button.setChecked(True)
                completion_button.clicked.connect(lambda _, h=habit, d=f'{day}': self.toggle_completion(h, d))
                self.grid_layout.addWidget(completion_button, row, day)
    
    def toggle_completion(self, habit_name, day):
        date = f'{self.current_month} {day}'

        if date in self.tracker.habits.get(habit_name, []):
            self.tracker.habits[habit_name].remove(date)
        else:
            self.tracker.habits.setdefault(habit_name, []).append(date)
        
        self.tracker.save_data()
    
    def save_data(self):
        self.tracker.save_data()

def main():
    app = QApplication(sys.argv)
    window = HabitTrackerGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()