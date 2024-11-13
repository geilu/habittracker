from datetime import datetime

class Habit:
    def __init__(self, name):
        self.name = name
        self.dates_completed = set()
    
    def mark_complete(self, date=None):
        if date is None:
            date = datetime.today().strftime('%Y-%m-%d')
        self.dates_completed.add(date)
    
    def is_completed(self, date):
        return date in self.dates_completed
    
    def get_completion_dates(self):
        return sorted(self.dates_completed)
    
    def __str__(self):
        return f"Habit: {self.name}, completed on {len(self.dates_completed)} days."