def cli(habit_manager, database):
    #this loop keeps this cli running until the program is exited
    while True :
        
        #this displays the menu of possible actions that can be taken by the user along with the corresponding  number to press in order to interact with the habit tracker
        print("""
        Welcome to your habit tracker! :D

        Action Menu: 
        1) Add new
        2) Mark completed
        3) Update
        4) List all
        5) View periodicity
        6) Show description
        7) View streak
        8) View longest streak
        9) Delete

        Press any other key followed by enter to exit.""")

        #user can type the number of the corresponding action that is desired
        action=input("\nTake action! ").strip()

        #adds a new habit to the habit manager
        #stores the new habit in the database 
        if action =="1" :
            habit = habit_manager.add_habit()
            database.store_habit({habit.name.lower(): habit})
        
        #here the habit is marked complete and the habit and database are updated with the new completion
        elif action == "2" :
            habit = habit_manager.completed_habit(database=database)

        #habit description and periodicity can be updated 
        elif action == "3":
            habit_manager.update_habit(database=database)

        #lists all of the habits stored in the habit tracker
        elif action =="4" :
            habit_manager.list_all_habits()
        
        #lists the habits by their periodicity, daily or weekly
        elif action=="5" :
            habit_manager.list_by_period()
        
        #displays the description of each habit
        elif action == "6":  
            habit_manager.show_description()

        #lists the habits with their streaks and the habits that do not have a streak 
        elif action=="7" :
            habit_manager.view_streak()

        #displays the habit with the longest streak
        elif action == "8" :
            habit_manager.longest_streak_all()

       
        #daletes habits from the habit manager and the database
        elif action == "9":
            habit_manager.delete_habit(database)
        
        #ends the loop
        else:
            break 