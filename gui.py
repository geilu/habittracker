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

        #tabid
        self.tabs = QTabWidget()
        self.habit_tab = QWidget()
        self.manage_tab = QWidget()

        self.tabs.addTab(self.habit_tab, 'Habits')
        self.tabs.addTab(self.manage_tab, 'Manage habits')
        self.main_layout.addWidget(self.tabs)

        self.habit_tab_setup()
        self.manage_tab_setup()

    def habit_tab_setup(self): #habiti checkimise tabi setup
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
    
    def generate_calendar_grid(self): #kalendrigridi tegemise funktsioon
        self.grid_layout.setSpacing(5)
        current_date = QDate.currentDate()
        days_in_month = current_date.daysInMonth()
        month_name = current_date.toString('MMMM')

        month_label = QLabel(month_name) #ülesse kirja praegune kuu
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

            habit_data = self.tracker.habits[habit]
            completion_dates = habit_data.get('completion_dates', [])

            for day in range(1, days_in_month+1):
                completion_button = QPushButton()
                completion_button.setFixedSize(30, 30)
                completion_button.setCheckable(True)

                date = f'{datetime.now().year}-{datetime.now().month}-{day}'
                if date in completion_dates:
                    completion_button.setChecked(True)
                completion_button.clicked.connect(lambda _, h=habit, d=f'{day}': self.toggle_completion(h, d))
                self.grid_layout.addWidget(completion_button, row, day)
    
    def manage_tab_setup(self): #manage habits tabi setup
        self.manage_tab_layout = QHBoxLayout()
        self.manage_tab.setLayout(self.manage_tab_layout)

        #vasak paneel(harjumuste list, lisa/kustuta(hetkel ainult lisamise nupp))
        self.habit_list_layout = QVBoxLayout()
        self.habit_list_widget = QListWidget()
        self.habit_list_widget.setFixedWidth(200)
        self.load_habits_into_list()
        self.habit_list_widget.itemClicked.connect(self.display_habit_details)

        #add habit button
        self.add_habit_button = QPushButton('+')
        self.add_habit_button.clicked.connect(self.tracker.add_habit)
        
        habit_button_layout = QHBoxLayout()
        habit_button_layout.addWidget(self.add_habit_button)      

        self.habit_list_layout.addWidget(QLabel('My Habits'))
        self.habit_list_layout.addWidget(self.habit_list_widget)
        self.habit_list_layout.addLayout(habit_button_layout)

        self.manage_tab_layout.addLayout(self.habit_list_layout)

        #parempoolne paneel(harjumuse detailid)
        self.details_tab_box = QGroupBox("Habit Details")
        self.details_tab_box.setStyleSheet("font-size: 14px;")
        self.details_layout = QVBoxLayout(self.details_tab_box)
        self.habit_name_label = QLabel('Habit Name')
        self.frequency_label = QLabel('Frequency:')
        self.progress_label = QLabel('Progress:')
        self.description_label = QLabel('Description:')

        self.details_layout.addWidget(self.habit_name_label)
        self.details_layout.addWidget(self.frequency_label)
        self.details_layout.addWidget(self.progress_label)
        self.details_layout.addWidget(self.description_label)

        self.manage_tab_layout.addWidget(self.details_tab_box)
    
    def load_habits_into_list(self):
        self.habit_list_widget.clear()
        for habit in self.tracker.habits.keys():
            self.habit_list_widget.addItem(habit)
    
    def display_habit_details(self, item):
        habit_name = item.text()
        habit_data = self.tracker.habits.get(habit_name, {})
        self.habit_name_label.setText(f'Habit: {habit_name}')
        self.frequency_label.setText(f"Frequency: {habit_data.get('frequency', 'N/A')}")
        self.progress_label.setText(f"Progress: {habit_data.get('progress', 'No data')}")
        self.description_label.setText(f"Description: {habit_data.get('description', 'No description')}")
    
    def toggle_completion(self, habit_name, day): #checkida mis päevadel harjumus täidetud on
        date = f'{datetime.now().year}-{datetime.now().month}-{day}'

        if habit_name in self.tracker.habits:
            completion_dates = self.tracker.habits[habit_name].setdefault('completion_dates', [])

            if date in completion_dates:
                completion_dates.remove(date)
            else:
                completion_dates.append(date)
        
            self.tracker.save_data()
        else:
            print(f"Habit '{habit_name}' does not exist")
    
    def save_data(self):
        self.tracker.save_data()

def main():
    app = QApplication(sys.argv)
    window = HabitTrackerGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()