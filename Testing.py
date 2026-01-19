import pytest
from habit import Habit
from habitManager import HabitManager
from unittest.mock import patch
from datetime import datetime, timedelta
from io import StringIO
import sys

#creates an instance of a habit manager for the tests
@pytest.fixture
def habit_manager():
    return HabitManager()

#creates a daily habit solely used for testing
@pytest.fixture
def daily_habit():
    return Habit("Intermittent Fasting", "fast for 14 to 16 hours", "daily")

#creates a weekly habit solely used for testing
@pytest.fixture
def weekly_habit():
    return Habit("Plan Week", "organise the upcoming week on Sunday", "weekly")

#this creates a 3 day streak for testing 
def test_daily_streak(daily_habit):
    today =datetime.now()
    daily_habit.completion_log = [
        today - timedelta(days=2),
        today - timedelta(days=1),
        today
        ]

    #makes sure that the streak count is right
    assert daily_habit.get_streak() == 3
    #and here it makes sure that the streak in not broken
    assert not daily_habit.streak_break()

#this creates a 3 week streak
def test_weekly_streak(weekly_habit):
    today= datetime.now()
    weekly_habit.completion_log = [
        today - timedelta(days=14),
        today - timedelta(days=7),
        today ]
    
    #makes sure that the streak count in correct 
    assert weekly_habit.get_streak() == 3
    #and that it is not broken 
    assert not weekly_habit.streak_break()

#the daily habit is added to the habit manager 
def test_add_habit_store(habit_manager, daily_habit):
    habit_manager.add_habit(daily_habit)
   
    #verifies that the habit is stored in lowercase
    assert "intermittent fasting" in habit_manager.habits
    #and that it has the correct name
    habit_key="intermittent fasting"
    assert habit_manager.habits[habit_key].name == "Intermittent Fasting"

#simulates user input for the creation of a habit 
def test_add_habit_create(habit_manager):
    with patch("builtins.input",side_effect=["Stretch", "stretch for 15 minutes","daily"]):
        habit = habit_manager.add_habit()
   
    #checks that the habit creation was accurately done
    assert habit.name == "Stretch"
    assert habit.periodicity == "daily"
    assert "stretch" in habit_manager.habits

#this completes the habit 
def test_completed_habit(habit_manager, daily_habit):
    habit_manager.add_habit(daily_habit)
    
    #simulates the act of a user choosing which habit is to be marked as complete
    with patch("builtins.input", return_value="Intermittent Fasting" ):
        habit = habit_manager.completed_habit()

    #checks that the completion was in fact logged
    assert len(habit.completion_log) == 1

#a test to edit an existing habit
def test_update_habit(habit_manager, daily_habit):
    habit_manager.add_habit(daily_habit)

   #this simulates the user input for testing; the habit name, description, and periodicity 
    with patch(
        "builtins.input",
        side_effect=[
            "Intermittent Fasting",  
            "Fast for 18 hours",     
            "daily"                  
        ]
    ):
        habit_manager.update_habit()
    
    #gets the updated habit from the manager
    habit = habit_manager.habits["intermittent fasting"]
    
    #verifies that the habit's decription and periodicity is updated
    assert habit.description == "Fast for 18 hours"
    assert habit.periodicity == "daily"


#this test deletes existing habits
def test_delete_habit(habit_manager, daily_habit):
    habit_manager.add_habit(daily_habit)

    #simulates a user selecting a habit
    with patch("builtins.input", return_value="Intermittent Fasting"):
        habit_manager.delete_habit()

    #makes sure that the habit has been deleted 
    assert "intermittent fasting" not in habit_manager.habits

#this test can detect when a streak is broken
def test_streak_break( daily_habit):
    today = datetime.now()
    #forces in a gap between completions to break a streak
    daily_habit.completion_log= [today - timedelta(days=4)]
   
    #checks that the streak is considered broken
    assert daily_habit.streak_break()

#a helper function that takes what is printed by a function for testing
def take_output(func, *args,**kwargs):  
    previous_output =sys.stdout
    sys.stdout = StringIO()
   
    #catches the print output
    try:
        func(*args,**kwargs)
        return sys.stdout.getvalue()
    #restores the normal printing    
    finally:
        sys.stdout= previous_output

#views the streak output
def test_view_streak(habit_manager):
    fasting = Habit("Intermittent Fasting", "fast for 16-14 hours", "daily")
    planning = Habit("Plan Week", "organise the upcoming week on Sunday", "weekly")
    today = datetime.now()
    
    #simulates a 4 day streak
    fasting.completion_log = [
        today- timedelta(days=3),
        today- timedelta(days=2), 
        today - timedelta(days=1), 
        today  ]  
    
    #adds the habit to the habit manager
    habit_manager.add_habit(fasting)
    habit_manager.add_habit(planning)
    
    #checks that the correct output is displayed
    output= take_output(habit_manager.view_streak)
    assert "Intermittent Fasting: 4 day(s)" in output

#a test to list all habits in the habit tracker
def test_list_all_habits(habit_manager, daily_habit, weekly_habit):
   
    #adds both the daily and the weekly habit to the habit manager
    habit_manager.add_habit(daily_habit)
    habit_manager.add_habit(weekly_habit)
    
    output = take_output(habit_manager.list_all_habits)
    
    #checks that both habit names are included
    assert "Intermittent Fasting" in output
    assert "Plan Week" in output


#a test to view the periodicity of a habit
def test_list_by_period(habit_manager, daily_habit, weekly_habit):
    
    #adds both the daily and the weekly habit to the habit manager
    habit_manager.add_habit(daily_habit)
    habit_manager.add_habit(weekly_habit)
    
    #simulates a user selecting the daily habit
    with patch("builtins.input", return_value="Intermittent Fasting"):
        output = take_output(habit_manager.list_by_period)
    
    #checks that the periodicity of the habit is outputted
    assert "daily" in output.lower()


#A method that shows the description of a habit
def test_show_description(habit_manager, daily_habit, weekly_habit):
    habit_manager.add_habit(daily_habit)
    habit_manager.add_habit(weekly_habit)
    
    #simulates a user selecting the weekly habit
    with patch("builtins.input", return_value="Plan Week"):
        output = take_output(habit_manager.show_description)
    
    #checks that the habit description is outputted
    assert "Organise the upcoming week on sunday" in output

#tests finding the longest streak
def test_longest_streak_all(habit_manager):
    fasting =Habit("Intermittent Fasting", "fast for 16-14 hours", "daily")
    planning =Habit("Plan Week", "organise the upcoming week on Sunday", "weekly")
    today=datetime.now()
    
    #simulates the daily habit streak of five days
    fasting.completion_log = [
        today - timedelta(days=4),
        today - timedelta (days=3) ,
        today -timedelta(days=2),
        today - timedelta(days=1),
        today]
    
    #simulates the weekly habit for three days 
    planning.completion_log = [
        today- timedelta(weeks=2),
        today-timedelta(weeks=1),
        today]  
   
    #adds the habit to the habit manager
    habit_manager.add_habit(fasting)
    habit_manager.add_habit(planning)
    
    #checks that the output is correct
    output=take_output(habit_manager.longest_streak_all)
    assert "Intermittent Fasting" in output
    assert "5"in output