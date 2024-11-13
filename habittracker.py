import json
from datetime import datetime

class Habit:
    def __init__(self, filename='data.json'):
        self.habits = {}
        self.filename = filename
    
    def add_habit(self, name, frequency='daily'):
        if name not in self.habits:
            self.habits[name] = {
                "frequency": frequency,
                "completion_dates": []
            }
            print(f"Habit '{name}' added with frequency '{frequency}'")
        else:
            print(f"Habit '{name}' already exists")
    
    def mark_habit(self, name):
        if name in self.habits:
            today = datetime.today().strftime('%Y-%m-%d')
            if today not in self.habits[name]['completion_dates']:
                self.habits[name]['completion_dates'].append(today)
                print(f"Habit '{name}' marked as completed for today")
            else:
                print(f"Habit '{name}' was already marked for today")
        else:
            print(f"Habit '{name}' does not exist")
    
    def list_habits(self):
        if not self.habits:
            print('No habits added yet')
        else:
            for habit, details in self.habits.items():
                print(f'\nHabit: {habit}')
                frequency = details.get('frequency')
                completion_dates = details.get('completion_dates')
                print(f"Habit: {habit} (Frequency: {frequency})")
                print(f"Completed on: {', '.join() if completion_dates else 'No completions yet'}")
    
    def save_data(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump({"habits": self.habits}, f, indent=4)
            print(f'Data saved to {self.filename}')
        except Exception as e:
            print(f'Error saving data: {e}')
    
    def load_data(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.habits = data.get('habits', {})
            print(f'Data loaded from {self.filename}')
        except FileNotFoundError:
            print(f'File not found, starting with empty habit list')
        except Exception as e:
            print(f'Error loading data: {e}')