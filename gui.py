import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QDate
from datetime import datetime
from habittracker import Habit
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

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
        self.habit_list_widget = QListWidget()
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
            #muudab laiuse pikima teksti laiuseks
            longest_string = max(self.tracker.habits.keys(), key=len)
            label = QLabel(longest_string)
            label.adjustSize()
            habit_label.setFixedWidth(label.width() + 10)
            habit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(habit_label, row, 0)

            habit_data = self.tracker.habits[habit]
            completion_dates = habit_data.get('completion_dates', [])

            for day in range(1, days_in_month+1):
                completion_button = QPushButton()
                completion_button.setFixedSize(30, 30)
                completion_button.setCheckable(True)
                completion_button.setObjectName('completionButton')

                date = f'{datetime.now().year}-{datetime.now().month}-{day}'
                if date in completion_dates:
                    completion_button.setChecked(True)
                completion_button.clicked.connect(lambda _, h=habit, d=f'{day}': self.toggle_completion(h, d))
                self.grid_layout.addWidget(completion_button, row, day)
    
    def clear_calendar_grid(self): #kalendri clearimine
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
    
    def manage_tab_setup(self): #manage habits tabi setup
        self.manage_tab_layout = QHBoxLayout()
        self.manage_tab.setLayout(self.manage_tab_layout)

        #vasak paneel(harjumuste list, lisa/kustuta(hetkel ainult lisamise nupp))
        self.habit_list_layout = QVBoxLayout()
        self.habit_list_widget = QListWidget()
        self.habit_list_widget.setObjectName('habitList')
        self.habit_list_widget.setFixedWidth(200)
        self.load_habits_into_list()
        self.habit_list_widget.itemClicked.connect(self.display_habit_details)

        #add habit ja remove habit button
        self.add_habit_button = QPushButton('+')
        self.add_habit_button.clicked.connect(self.add_habit_dialogue)
        self.add_habit_button.setObjectName('addButton') #object name stylesheeti jaoks

        self.remove_habit_button = QPushButton('-')
        self.remove_habit_button.clicked.connect(self.remove_selected_habit)
        self.remove_habit_button.setObjectName('removeButton')
        
        habit_button_layout = QHBoxLayout()
        habit_button_layout.addWidget(self.add_habit_button)
        habit_button_layout.addWidget(self.remove_habit_button)

        #harjumuste list
        self.habit_list_layout.addWidget(QLabel('My Habits'))
        self.habit_list_layout.addWidget(self.habit_list_widget)
        self.habit_list_layout.addLayout(habit_button_layout)

        self.manage_tab_layout.addLayout(self.habit_list_layout)

        #parempoolne paneel(harjumuse detailid)
        self.details_tab_box = QGroupBox(f'Habit Details')
        self.details_tab_box.setStyleSheet('font-size: 18px;')
        self.details_layout = QVBoxLayout(self.details_tab_box)
        self.habit_name_label = QLabel(f'<b>Select a habit to view info</b>')
        self.frequency_label = QLabel('')
        self.description_label = QLabel('')

        self.details_layout.addWidget(self.habit_name_label)
        self.details_layout.addWidget(self.frequency_label)
        self.details_layout.addWidget(self.description_label)

        self.manage_tab_layout.addWidget(self.details_tab_box)
    
    def load_habits_into_list(self): #laeb harjumused listi
        self.habit_list_widget.clear()
        for habit in self.tracker.habits.keys():
            self.habit_list_widget.addItem(habit)
    
    def display_habit_details(self, item): #detailide all näitab harjumuse nime, sagedust ja progressi
        if not item:
            self.reset_habit_details()
            return
        
        habit_name = item.text()
        habit_data = self.tracker.habits.get(habit_name, {})
        self.habit_name_label.setText(f'<b>Habit:</b> {habit_name}')
        self.frequency_label.setText(f"<b>Frequency:</b> {habit_data.get('frequency', 'N/A')}")
        self.description_label.setText(f"<b>Description:</b> {habit_data.get('description', 'No description')}")

        completion_dates = habit_data.get('completion_dates', [])
        frequency = habit_data.get('frequency', 'Daily')
        self.habit_progress_graph(completion_dates, frequency)
    
    def reset_habit_details(self): #resetib detailide osa
        self.habit_name_label.setText('<b>Select a habit to view info</b>')
        self.frequency_label.setText('')
        self.description_label.setText('')

        if hasattr(self, 'canvas') and self.canvas:
            self.details_layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
    
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
    
    def add_habit_dialogue(self): #dialoogi kasti ilmumine kui harjumust lisada
        dialogue = AddHabitDialogue(self)
        if dialogue.exec():
            habit_name, frequency, description = dialogue.get_habit_info()
            if habit_name:
                self.tracker.add_habit(habit_name, frequency)
                if description:
                    self.tracker.habits[habit_name]['description'] = description
                self.tracker.save_data()
                self.load_habits_into_list()

                self.clear_calendar_grid()
                self.generate_calendar_grid()
    
    def remove_selected_habit(self): #harjumuse eemaldamise nupu funktsioon
        selected_item = self.habit_list_widget.currentItem()
        if selected_item:
            habit_name = selected_item.text()

            confirm = QMessageBox.question(self, 'Confirm', f"Are you sure you want to delete the habit '{habit_name}'?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                self.tracker.delete_habit(habit_name)
                self.tracker.save_data()
                self.load_habits_into_list()

                self.clear_calendar_grid()
                self.generate_calendar_grid()

                self.statusBar().showMessage(f"'{habit_name}' has been removed.", 5000) #näitab all ääres, et harjumus on eemaldatud

                if self.habit_list_widget.count() == 0:
                    self.reset_habit_details()
        else:
            QMessageBox.warning(self, 'No Habit Selected', 'Please select a habit to remove!')
        
    def habit_progress_graph(self, completion_dates, frequency='Daily'): #harjumuse progressi graafik
        if hasattr(self, 'canvas') and self.canvas:
            self.details_layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
        
        current_date = QDate.currentDate()
        days_in_month = current_date.daysInMonth()
        weeks_in_month = (days_in_month + current_date.dayOfWeek() - 1) // 7
        completed_days = len(set(datetime.strptime(date, '%Y-%m-%d').day for date in completion_dates))

        if frequency == 'Daily':
            completed = completed_days
            target = days_in_month
        elif frequency == 'Weekly':
            completed_weeks = len(set((datetime.strptime(date, '%Y-%m-%d').day - 1)//7 for date in completion_dates))
            completed = completed_weeks
            target = weeks_in_month
        else:
            completed = 0
            target = 1
        
        remaining = target - completed
        remaining = max(0, remaining) #et ei oleks mingit negatiivset

        sizes = [completed, remaining]
        labels = ['Completed', 'Remaining']
        colors = ['mediumorchid', 'lightgray']

        fig1, ax1 = plt.subplots(figsize=(3, 3))
        ax1.pie(
            sizes, labels=labels, autopct='%1.1f%%', startangle=90,
            colors=colors, textprops={'fontsize': 10}
        )
        ax1.set_title(f'Habit Progress This Month (Frequency: {frequency})', fontsize=12)

        self.canvas = FigureCanvas(fig1)
        self.details_layout.addWidget(self.canvas)
        self.canvas.draw()

        plt.close(fig1)
    
    def save_data(self):
        self.tracker.save_data()

class AddHabitDialogue(QDialog): #harjumuse dialoogi kast
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Add Habit')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.habit_name_input = QLineEdit(self)
        self.habit_name_input.setPlaceholderText('Enter habit name')
        layout.addWidget(QLabel('Habit Name:'))
        layout.addWidget(self.habit_name_input)

        self.frequency_combo = QComboBox(self)
        self.frequency_combo.addItems(['Daily', 'Weekly'])
        layout.addWidget(QLabel('Frequency:'))
        layout.addWidget(self.frequency_combo)

        self.description_input = QTextEdit(self)
        self.description_input.setPlaceholderText('Enter description (Optional)')
        layout.addWidget(QLabel('Description:'))
        layout.addWidget(self.description_input)

        button_layout = QHBoxLayout()
        add_button = QPushButton('Add', self)
        add_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton('Cancel', self)
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
    
    def get_habit_info(self): #dialoogi kasti jaoks harjumuse info kogumine
        habit_name = self.habit_name_input.text().strip()
        frequency = self.frequency_combo.currentText()
        description = self.description_input.toPlainText().strip()

        if not habit_name:
            return None, None, None
        
        return habit_name, frequency, description

def load_stylesheet(filepath): #stylesheeti faili laadimine
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f'Stylesheet file not found: {filepath}')
        return ''

def main():
    app = QApplication(sys.argv)

    stylesheet = load_stylesheet('styles.qss')
    app.setStyleSheet(stylesheet)

    window = HabitTrackerGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()