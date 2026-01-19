from datetime import datetime

class Habit:

    #initialisation of habits and defines their attributes
    def __init__(self,name, description, periodicity, creation_date=None, completion_log=None):
        self.name = name 
        self.description = description
        self.periodicity = periodicity
        self.creation_date = creation_date or datetime.now()
        self.completion_log = completion_log or []

    def __str__(self):
        return f"{self.name.title()} ({self.periodicity}): {self.description.capitalize()}"

    #this method marks the habits as completed for the day or week
    def mark_completed(self, database=None):
        today = datetime.now()
    
        #this allows the prevention of duplicate completions for the same day
        if today not in self.completion_log:
            self.completion_log.append(today)
            print(f"'{self.name}' habit completed!")
        else:
            print(f"'{self.name}' habit is already marked completed today!")

        #stores the completion in the database
        if database:

            #the completion is saved
            database.store_completion(self.name, [today])

    #this method calculates the habit's current streak
    def get_streak(self):

        #in case there are no completions then there will be no streak
        if not self.completion_log:
            return 0

        #stores the completion so that the most recent completion comes first 
        completions = sorted(self.completion_log, reverse=True)

        #the streak starts once there is one completion
        streak = 1
        #this stores the date of the most recent completion to compare with
        previous_date = completions[0].date()

        #daily streak 
        if self.periodicity == "daily":
            #checks whether there is a completion on the preceding day which allows for the calculation of the current streak 
            for completion in completions[1:]:
                current_date = completion.date()
                #the difference between completions can only be one day
                if (previous_date - current_date).days == 1:
                    streak += 1
                    previous_date = current_date
                #stops counting once a day has been missed
                else:
                    break

        #weekly streak
        elif self.periodicity == "weekly":
            #this checks whether there is a completion on the preceding week  
            for completion in completions[1:]:
                current_date = completion.date()
                #the range of days that constitute a week is from 6 to 8 days
                if 6 <= (previous_date - current_date).days <= 8:
                    streak += 1
                    previous_date = current_date
                #stops counting the streak once a week has been missed
                else:
                    break

        #return the calculated streak
        return streak

        
    #this method checks whether the habit's streak is currently broken, meaning that a day or week was missed
    def streak_break(self):
        
        #the streak is broken when there is no completion
        if not self.completion_log:  
            return True  

        #the most recent completion is retrieved
        today = datetime.now()
        previous_completion = self.completion_log[-1]

        #for daily habits if more than one day has gone by without completion, then the srteak is broken
        if self.periodicity == "daily":
            return (today.date() - previous_completion.date()).days > 1
        #for weekly habits, if more than one week has gone by without completion then the streak is broken
        elif self.periodicity == "weekly":
            return today.isocalendar()[1] - previous_completion.isocalendar()[1] > 1