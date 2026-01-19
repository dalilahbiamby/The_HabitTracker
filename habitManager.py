from habit import Habit
from datetime import datetime

#The habit manager class, manages the habit objects with methods to create, update, track completions, delete, and display habit info. 
class HabitManager:
    
    #the initialising of an empty dictionary to sotore the habits
    def __init__(self):
        self.habits = {}

    #the method that allows the user to create habits, using parameters: name, description, and periodicty. 
    #also the existing habit objects from the preload class to be added
    def add_habit(self, habit=None):
        if habit is None:
            print("\nCreate a habit!")
            name = input("Name: ")

            #prompts ther user to choose another habit name if the one they entered alreaady exists
            while name.lower() in self.habits:
                name = input("A habit with this name already exists, pick another name:")
            
            description = input("Description: ")
            periodicity = input("Periodicity (daily or weekly): ").strip().lower()
            
            #prompts user to write an accepted periodicity of daily or weekly if they wrote something else.
            while periodicity not in ["daily", "weekly", " "]:
                periodicity = input(" Write 'daily' or 'weekly': ").strip().lower()  
            
            #habit instance
            habit = Habit(name, description, periodicity)
        
        #habits are stored with lowercase, this helps for later retrieval of habit, if the capitalisation of the name has been forgotten by the user
        self.habits[habit.name.lower()] = habit
        
        #print message when habit is successfully created
        print(f"\n{habit.name.title()} habit created :D")
        return habit

    #the method returns the habit which is marked completed by the user for the day/week
    def completed_habit(self, database=None):
        print("\nMark habit complete!")
        
        #user can input the habit name
        name = input("\nHabit name: ").strip().lower()

        #returns the marked habit
        habit = self.habits.get(name)

        #in case habit is mispelled or doesnt exist etc.
        if not habit:
            print("Habit not found")
            return None

        #allows the habit object ot save its completion data to the databse
        habit.mark_completed(database=database)
        return habit

    # method to delete a habit from the manager and datebase
    def delete_habit(self, database=None):
        print("\n Delete a habit.")
        
        #user inputs habit name
        name = input("Habit name: ").strip().lower()

        #deletes the habit if it exists 
        if name in self.habits:
            del self.habits[name]
        
            #print messages if the habit has been deleted succesfully or if it didnt exist to begin with
            print(f"\n{name.title()} habit deleted successfully")

            if database: 
                database.delete_habit(name)
        else:
            print(f"\n{name.title()} habit is already gone")

    #method that updates the habit description and periodicity ( both are optional). The name cannot be updated
    def update_habit(self, database=None):
        print("\n Make changes to a habit!")
        
        #user inputs habit name
        name = input("Habit name: ").strip().lower()
        habit = self.habits.get(name)
        
        #in case the habit does not exist
        if not habit:
            print("Habit not found")
            return

        #users can edit the description and or periodicity.
        print("\nEdit description and/or periodicity.")
        new_description = input("Description: ")
        new_periodicity = input("Periodicity (daily or weekly): ").strip().lower()

        #replaces the old description/periodicity with the newly set ones
        if new_description:
            habit.description = new_description
        if new_periodicity:
            habit.periodicity = new_periodicity

        #saves the habit update to the database
        if database:
            database.store_habit({habit.name.lower(): habit})

        #print message to confirm habit update success
        print(f"\n{habit.name.title()} habit updated!")  

    #to view the current streaks and view the habits that do not currently have a streak
    def view_streak(self):
        print("\nView habit streaks:\n")

        #creates two lists, one for the habits with streaks and one for the habits without streaks
        active_streaks =[]
        no_streaks=[]

        #loops thorugh all habits and if the returned habit's streak value is more than zero days, it is an active streak
        for habit in self.habits.values():
            streak = habit.get_streak()  

            #assign the correct unit to the streak value (either daily or weekly)
            if habit.periodicity == "daily":
                unit = "day(s)"
            else:
                unit = "week(s)"

            #seperates the currently active streaks from the habits with inactive streaks
            if streak > 0:
                active_streaks.append((habit.name, streak, unit))
            else:
                no_streaks.append(habit.name)

        #prints the active streaks and the non-active streaks
        print("Currently active streaks:")
        if active_streaks:
            for name, streak, unit in active_streaks:
                print(f"{name.title()}: {streak} {unit}")

        print("\nCurrently inactive streaks:")
        if no_streaks:
            for name in no_streaks:
                print(f"{name.title()}")             
    
    #Prints all the habits stored in the habit tracker
    def list_all_habits(self):
        print("\nA list of all your habits:")          

        for habit in self.habits.values():
            print(f"{habit.name.title()}")

    #prints all of the habits in the habit tracker by periodicity (daily habits or weekly habits)
    def list_by_period(self):
        print("\nViewing habit periodicty")

        #the daily and weekly habits are seperated and displayed in their respective lists
        print("\nDaily:")
        for habit in self.habits.values():
            if habit.periodicity == "daily":
                print(f"{habit.name.title()}")

        print("\nWeekly:")
        for habit in self.habits.values():
            if habit.periodicity == "weekly":
                print(f"{habit.name.title()}")
           

    #this method allows the user to view the habit with the longest streak
    def longest_streak_all(self):
        print("\nSearch your longest streak!")

        #calculates and prints habit with the longest streak and the streak number of days or weeks
        streaks = {name: habit.get_streak() for name, habit in self.habits.items()}
        longest_habit = max(streaks, key=streaks.get)
        longest_streak = streaks[longest_habit]
        print(f" Your longest streak is {longest_habit.title()}, for {longest_streak} days/weeks in a row!")

    #this method shows all habit names and their respective descriptions
    def show_description(self):
        print("\nView habit description\n")
        for habit in self.habits.values():
            print(str(habit)) 