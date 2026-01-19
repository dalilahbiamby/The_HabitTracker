import sqlite3
from habit import Habit
from datetime import datetime, timedelta

#the database class that creates the sqlite database 
#allows for the creation of table, sotring methods to store and retrieve habit data
class Database:

    #initialises the database connection 
    def __init__(self, the_database="habits.db"):
        
        #makes the connection to the sqlite database file 
        self.conn =sqlite3.connect(the_database)

        #allows for a foreign key support in sqlite 
        self.conn.execute("PRAGMA foreign_keys=ON;")
        
        #creates tables 
        self.create_table()

    #the method to create tables in the database class
    def create_table(self):
        
        #creates the table that stores the habits 
        self.conn.execute(""" 
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                periodicity TEXT NOT NULL CHECK (periodicity IN ('daily', 'weekly')),
                created_at TEXT NOT NULL
                )
        """)

        #creates the table that stores the habit completion dates
        #the completions reference the habit by using habit_id
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY,
                habit_id INTEGER NOT NULL,
                completed_at TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits(id)
                )
        """)
        self.conn.commit()

    #the method that stores one or multiple habit objects in the database 
    def store_habit(self, habits):
        cursor = self.conn.cursor()

        #this inserts each habit object in the dictionary into the habit table
        for habit in habits.values():
            cursor.execute("""
                INSERT INTO habits (name, description, periodicity, created_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    description=excluded.description,
                    periodicity=excluded.periodicity
            """, (
                habit.name.lower(), 
                habit.description, 
                habit.periodicity, 
                habit.creation_date.isoformat()
                ))
        self.conn.commit()

    #this method fetches the stored habits in the databse and returns them as habit objects
    def fetch_habit(self):
        cursor = self.conn.cursor()

        #selects all of the habits that are stored into the database
        cursor.execute("SELECT name, description, periodicity,created_at FROM habits")
        rows = cursor.fetchall()
        habits = {}
        
        #converts the database rows back to habit objects
        for row in rows:
            name = row[0]
            description = row[1]
            periodicity= row[2]
            created_at= datetime.fromisoformat(row[3])
            habits[name]= Habit (name, description, periodicity, created_at)
        return habits
      
    #method that stores the completion timestamps for habits
    def store_completion(self, habit_name, completion_dates):
        cursor = self.conn.cursor()

        #converts all habit names that are searched to lower case
        habit_name =habit_name.lower()
        
        #searches and finds the habit's id which allows the completions to be referenced accurately
        cursor.execute("SELECT id FROM habits WHERE name = ?", (habit_name,))
        row = cursor.fetchone()
        if not row:
            print(f"'{habit_name}' not found :(")
            return
        habit_id = row[0]

        #stores the completion date while ignoring duplicates, in case the  completion is logged more than once on the same day
        for date in completion_dates:
            cursor.execute(
                "INSERT OR IGNORE INTO completions (habit_id, completed_at)  VALUES (?, ?)",
                (habit_id,   date.isoformat())
            )
        self.conn.commit()

    #this method fetches the completion  timstamps for habits
    def fetch_completion(self, habit_name, silent=False):
        cursor = self.conn.cursor()
        habit_name =habit_name.lower()
        
        #retrieves the habit's id to look up its completions
        cursor.execute ("SELECT id FROM habits WHERE name = ?", (habit_name,))
        row = cursor.fetchone()
        
        #message in case the habit cannot be found
        if not row:
            if not silent:  # Only print if silent=False
                print(f"'{habit_name}' habit not found :(")
            return []
        habit_id = row [0]
        
        #fetches the completion timestamps that are recorded for the respective habit
        cursor.execute("SELECT completed_at FROM completions WHERE habit_id = ?", (habit_id,))
        rows = cursor.fetchall()
        
        #the timestamp is converted back into a datetime object
        return [datetime.fromisoformat(date_str) for (date_str,) in rows]

    
    #this method deletes the habit along with its completion log
    def delete_habit(self, name):
        cursor=self.conn.cursor()
    
        #first the completion log for the habit that is to be deleted is deleted
        cursor.execute("DELETE FROM completions WHERE habit_id = (SELECT id FROM habits WHERE name = ?)", (name.lower(),))
    
        #then the actual habit is deleted
        cursor.execute("DELETE FROM habits WHERE name = ?", (name.lower(),))
    
        self.conn.commit()