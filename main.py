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
# Lisakommentaar (nt käivitusjuhend): hetkel CLI saab kui runid main.py ja GUI saab kui runid gui.py
#
##################################################
from habittracker import Habit

def main():
    tracker = Habit()
    tracker.load_data()

    while True:
        print('\n---Habit Tracker---')
        print('1. Add habit')
        print('2. Mark habit complete')
        print('3. View habits')
        print('4. Save data')
        print('5. Quit')

        choice = input('Choose an option(1-5): ')

        if choice == '1':
            habit_name = input('Enter name of habit: ')
            tracker.add_habit(habit_name)
        elif choice == '2':
            habit_name = input('Enter name of habit to mark as complete: ')
            tracker.mark_habit(habit_name)
        elif choice == '3':
            tracker.list_habits()
        elif choice == '4':
            tracker.save_data()
        elif choice == '5':
            print('Goodbye!')
            break
        else:
            print('Invalid choice, please try again')

if __name__ == '__main__':
    main()