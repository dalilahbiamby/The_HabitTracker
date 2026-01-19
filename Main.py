from database import Database
from habitManager import HabitManager
from cli import cli
from Preload import preload_habits

# initialises the habit manager and the database
if __name__ == "__main__":
    database = Database()
    habit_manager = HabitManager()

    #loads all of the pre-exisiting habits into the database
    loaded_habits = database.fetch_habit()
    habit_manager.habits = {name.lower(): habit for name, habit in loaded_habits.items()}
    
    if not database.fetch_habit():
        preload_habits(habit_manager, database)

    #loads the completion logs for all of the habits
    for name, habit in habit_manager.habits.items():
        habit.completion_log = database.fetch_completion(name, silent=True)

    #runs the cli
    cli(habit_manager, database)