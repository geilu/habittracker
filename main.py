################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt
# Teema: Habit Tracker
#
#
# Autorid: Geilyn Tisler, Gris Reinesberg
#
# mõningane eeskuju: Toggl, füüsilised habit trackeri päevikud
#
# Lisakommentaar (nt käivitusjuhend):
#
##################################################
from habittracker import Habit

def main_menu():
    print('\n1. Add a new habit')
    print('2. Mark habit as complete')
    print('3. View habits')
    print('4. Exit')
    return input('Choose an option: ')

def add_habit(habits):
    name = input('Enter name of new habit: ')
    habit = Habit(name)
    habits.append(habit)
    print(f"Habit '{name}' added!")

def mark_habit_complete(habits):
    if not habits:
        print('No habits available to mark as complete')
        return
    
    for index, habit in enumerate(habits, start=1):
        print(f'{index}. {habit.name}')
    choice = int(input('Select a habit to mark complete: ')) - 1

    if 0 <= choice < len(habits):
        habits[choice].mark_complete()
        print(f"Marked '{habits[choice].name} as complete for today")
    else:
        print('Invalid choice!')

def view_habits(habits):
    if not habits:
        print('No habits to display.')
        return
    
    print('\nYour habits:')
    for habit in habits:
        print(f'- {habit.name} (Completed on: {habit.get_completion_dates()})')

def main():
    habits = []
    while True:
        choice = main_menu()

        if choice == '1':
            add_habit(habits)
        elif choice == '2':
            mark_habit_complete(habits)
        elif choice == '3':
            view_habits(habits)
        elif choice == '4':
            print('Goodbye!')
            break
        else:
            print('Invalid option. Please try again')

if __name__ == '__main__':
    main()