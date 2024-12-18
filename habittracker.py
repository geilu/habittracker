import json
from datetime import datetime, timedelta

class Habit:
    def __init__(self):
        self.habits = {}
    
    def add_habit(self, name, frequency='Daily'):
        if name not in self.habits:
            self.habits[name] = {
                'frequency': frequency,
                'completion_dates': [],
                'description': ''
            }
            print(f"Habit '{name}' added")
        else:
            print(f"Habit '{name}' already exists")

    def delete_habit(self, name):
        if name in self.habits:
            del self.habits[name]
            print(f"Habit '{name}' has been deleted.")
        else:
            print(f"Habit '{name}' does not exist.")
    
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
            for name, data in self.habits.items():
                print(f'\nHabit: {name}')
                print(f"Frequency: {data['frequency']}")
                if data['completion_dates']:
                    completion_dates = [datetime.strptime(date, '%Y-%m-%d') for date in data['completion_dates']]
                    completion_dates.sort()

                    sorted_dates = [date.strftime('%Y-%m-%d') for date in completion_dates]
                    print(f"Completed on: {', '.join(sorted_dates)}")
                else:
                    print('Completed on: No completions yet')
                print(f"Description: {data['description']}")

    
    def save_data(self, filename='data.json'):
        try:
            with open(filename, 'w') as f:
                json.dump(self.habits, f, indent=4, sort_keys=False)
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

    def calculate_streak(self, name):

        if name not in self.habits:
            print(f"Habit '{name}' does not exist")
            return 0
        completion_dates = [datetime.strptime(date, '%Y-%m-%d') for date in self.habits[name]['completion_dates']]
        if not completion_dates:
            print(f"No completions yet for habit '{name}'")
            return 0
        completion_dates.sort()

        streak = 0
        max_streak = 0

        if self.habits[name]['frequency'] == 'Weekly':
            unique_weeks = sorted({date - timedelta(days=date.weekday()) for date in completion_dates})
            for i in range(1, len(unique_weeks)):
                if i == 0 or (unique_weeks[i] - unique_weeks[i-1]).days == 7:
                    streak += 1
                else:
                    max_streak = max(max_streak, streak)
                    streak = 1
            max_streak = max(max_streak, streak)
            print(f"Current streak for habit '{name}': {max_streak} week(s)")
                    
        else:
            streak = 1
            max_streak = 1
            for i in range(1, len(completion_dates)):
                days_diff = (completion_dates[i] - completion_dates[i-1]).days
                if days_diff == 1:
                    streak += 1
                else:
                    max_streak = max(streak, max_streak)
                    streak = 1
            max_streak = max(streak, max_streak)
            print(f"Current streak for habit '{name}': {max_streak} day(s)")

        return max_streak