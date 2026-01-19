from datetime import datetime, timedelta
from habit import Habit

#preloaded habits that are included with the habit tracker
#they include, a name, description, periodicity (daily or weekly), and completions 
included_habits = {
    "Meditate": {
        "description": "morning meditation for 15 minutes",
        "periodicity": "daily",
        "completions": [
            "2025-12-15","2025-12-16","2025-12-17","2025-12-18","2025-12-19","2025-12-20",
            "2025-12-21","2025-12-22","2025-12-23","2025-12-24","2025-12-25","2025-12-26",
            "2025-12-27","2025-12-28","2025-12-29","2025-12-30","2025-12-31","2026-01-01",
            "2026-01-02","2026-01-03","2026-01-04","2026-01-05","2026-01-06","2026-01-07",
            "2026-01-08","2026-01-09","2026-01-10","2026-01-11","2026-01-12","2026-01-13",
            "2026-01-14","2026-01-15","2026-01-16","2026-01-17","2026-01-18","2026-01-19",
            "2026-01-20","2026-01-21","2026-01-22","2026-01-23","2026-01-25","2026-01-26",
            "2026-01-27","2026-01-28","2026-01-29","2026-01-30","2026-01-31","2026-02-01",
            "2026-02-02","2026-02-03","2026-02-04","2026-02-05","2026-02-06","2026-02-07",
            "2026-02-08","2026-02-09","2026-02-10"
        ]
    },

    "Exercise": {
        "description": "Exercise for at least 30 minutes",
        "periodicity": "daily",
        "completions": [
            "2025-12-15","2025-12-16","2025-12-17","2025-12-19","2025-12-20","2025-12-21",
            "2025-12-22","2025-12-24","2025-12-25","2025-12-26","2025-12-27","2025-12-28",
            "2025-12-29","2025-12-30","2025-12-31","2026-01-01","2026-01-02","2026-01-03",
            "2026-01-04","2026-01-05","2026-01-06","2026-01-07","2026-01-08","2026-01-09",
            "2026-01-10","2026-01-11","2026-01-12","2026-01-13","2026-01-14","2026-01-16",
            "2026-01-17","2026-01-19","2026-01-20","2026-01-21","2026-01-23","2026-01-24",
            "2026-01-26","2026-01-27","2026-01-28","2026-01-30","2026-01-31","2026-02-02",
            "2026-02-03","2026-02-05","2026-02-06","2026-02-07","2026-02-09","2026-02-10"
        ]
    },

    "Practice German": {
        "description": "Practice German for 15 minutes",
        "periodicity": "daily",
        "completions": [
            "2025-12-15","2025-12-16","2025-12-18","2025-12-19","2025-12-20","2025-12-21",
            "2025-12-24","2025-12-26","2025-12-27","2025-12-28","2025-12-29","2025-12-30",
            "2025-12-31","2026-01-01","2026-01-02","2026-01-04","2026-01-05","2026-01-06",
            "2026-01-07","2026-01-08","2026-01-09","2026-01-10","2026-01-11","2026-01-12",
            "2026-01-13","2026-01-14","2026-01-15","2026-01-17","2026-01-18","2026-01-21",
            "2026-01-22","2026-01-23","2026-01-26","2026-01-27","2026-01-29","2026-02-01",
            "2026-02-02","2026-02-04","2026-02-05","2026-02-06","2026-02-09"
        ]
    },

    "Meal Prep": {
        "description": "Plan and prepare weekday meals",
        "periodicity": "weekly",
        "completions": [
            "2025-12-23","2025-12-30","2026-01-06","2026-01-20","2026-02-03", "2026-02-10"
        ]
    },

    "Clean Apartment": {
        "description": "Deep clean the apartment",
        "periodicity": "weekly",
        "completions": [
            "2025-12-18","2025-12-25","2026-01-01","2026-01-08","2026-01-15","2026-01-22",
            "2026-01-29","2026-02-05"
        ]
    }
}



#this method converts the iso-format strings into datetime objects
def parse_dates(date_list):
    return [datetime.fromisoformat(date) for date in date_list]

#loads the included habits into the database and into the habit manager
def preload_habits(habit_manager, database):
    existing = database.fetch_habit()

    for name, info in included_habits.items():
        habit_name = name.strip().lower()
        
        #checks if the habit is already in the database
        if habit_name in existing:
            habit=existing[habit_name]
                 
            #this loads the existing completion log stored in the database
            habit.completion_log  = database.fetch_completion(habit_name, silent=True)
            habit_manager.habits[habit_name] = habit
            continue

        #this converts the stored completion strings into datetime objects
        completion_log=parse_dates(info["completions"])
        
        #creates the habit object
        habit = Habit(
            name=habit_name,
            description=info["description"],
            periodicity=info["periodicity"],
            creation_date=datetime.now(),
            completion_log=completion_log
        )

        #thistores the habit into the database
        database.store_habit({habit_name: habit})
        database.store_completion(habit_name,completion_log)

        #saves the habit into the habit manager
        habit_manager.habits[habit_name] =  habit