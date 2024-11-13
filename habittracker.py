import json
from datetime import datetime

class Habit:
    def __init__(self):
        self.habits = {}
    
    def add_habit(self, name):
        if name not in self.habits:
            self.habits[name] = []
            print(f"Habit '{name}' added")
        else:
            print(f"Habit '{name}' already exists")
    
    def mark_habit(self, name):
        if name in self.habits:
            today = datetime.today().strftime('%Y-%m-%d')
            if today not in self.habits[name]:
                self.habits[name].append(today)
                print(f"Habit '{name}' marked as completed for today")
            else:
                print(f"Habit '{name}' was already marked for today")
        else:
            print(f"Habit '{name}' does not exist")
    
    def list_habits(self):
        if not self.habits:
            print('No habits added yet')
        else:
            for habit, dates in self.habits.items():
                print(f'\nHabit: {habit}')
                print(f"Completed on: {', '.join(dates) if dates else 'No completions yet'}")
    
    def save_data(self, filename='data.json'):
        try:
            with open(filename, 'w') as f:
                json.dump(self.habits, f, indent=4)
            print(f'Data saved to {filename}')
        except Exception as e:
            print(f'Error saving data: {e}')
    
    def load_data(self, filename='data.json'):
        try:
            with open(filename, 'r') as f:
                self.habits = json.load(f)
            print(f'Data loaded from {filename}')
        except FileNotFoundError:
            print(f'File not found, starting with empty habit list')
        except Exception as e:
            print(f'Error loading data: {e}')