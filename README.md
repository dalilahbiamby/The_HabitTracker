# The HabitTracker Installation and Run Manual

## 1. Introduction & Purpose 

The HabitTracker is a command-line based software application designed to help users create, manage, and analyse their personal habits over long periods of time. The primary purpose of this application is to support habit development by providing users with a one stop location when they can track their habits, their completions, and view analytics such as streak lengths and longest consecutively running habits. The application focuses on simplicity and clear feedback, so that users can easily monitor their daily and weekly habits.

## 2. Installation Prerequisites 
  
  ### 2.1 System Requirements 

  - Operating System: Windows, macOS, or Linux

  - Access to: Terminal/Command Prompt/Shell
    
  ### 2.2 Software Requirements 

  - A code editor (for example: VS Code)
      
  - Python 3.9 or higher (to run the application's code via the code editor)
    
    - Verify the Python version by running the following command in the terminal/command prompt/shell:
      
        - python -- version
          or
        - python3 -- version
          
    - If Python is not installed, download it using the following url:
      
        - https://www.python.org/downloads/
          
  - Git (for version control and cloning the repository)
       
    - Verify the Git installation by running the following command in the terminal/command prompt/shell:

        - git --version

    - If Git is not installed, find download guides using the following url:

        - https://github.com/git-guides/install-git
         
  ### 2.3 Programming Language & Tools Used

  - Python: for the application’s logic and object-oriented approach
    
  - SQLite: for data storage of the habits and their completion logs
    
  - Pytest: for testing the application’s core functionalities and analytics
    
  - Unittest.mock: for simulating user input during tests
    
  - GitHub: for version control and project management

## 3. Installation & Run Guide
  
  ### 3.1 Clone the Repository 

  - Using the terminal/command prompt/shell run the following command

      - git clone https://github.com/dalilahbiamby/The_HabitTracker.git
      
      - cd The_HabitTracker

  - Another option is to download the zip file and extract the code

  ### 3.2 Install Dependencies

  - install Pytest to run the functionality test; do this via the terminal/command prompt/shell using the following command

      - pip install pytest

  ### 3.3 Run the Application via the terminal/command prompt/shell

  - Navigate to The HabitTracker project folder using the terminal/command prompt/shell
  
  - Run the cd command with the following structure:

      - cd /Users/YourUserName/YourFolderWhereTheApplicationIsSaved/Habit_Tracker.py

  - Then run the following command to start The HabitTracker CLI:
  
      - python main.py
        or try 
      - python3 main.py
   
  - The application will be launched and will display an interactive action menu in the terminal/command prompt/shell

  - Press any key on the keyboard other than 1 through 9 to exit The HabitTracker
       
## 4. Application Features

- Users can perform the following actions through the menu:

  -  Add new habit
 
  -  Mark habit as completed
 
  -  Update habit description and/or periodicity
 
  -  List all (habits)
 
  -  View habits by periodicity
 
  -  Display habit descriptions
 
  -  View current habit streaks
 
  -  View longest habit streak
 
  -  Delete an exisiting habit
 
- Each action correcponds to a number between 1 and 9, which much be pressed to perform the action

- The application includes 5 preloaded habits with time-series completion data, which ends on February 10th 2026

## 5. Testing 

- Automated unit tests have been included to verify the core habit functionalities, they include:

    - Habit creation
 
    - Habit update
 
    - Habit deletion
 
    - Storing of habits
 
    - Habit correctly marked as completed
 
    - Daily streak calculation
 
    - Weekly streak calculation
 
    - Detecting broken streaks
 
    - All habits listed correctly
 
    - List by periodicity listed correctly
 
    - View streak calculated and listed correctly
 
    - Show description listed correctly
 
    - Longest streak calculated and listed correctly
 
- Run the tests in the terminal/command prompt/shell while in the application's folder with the following command:

    - pytest Testing.py -v
 
## 6. Database Storage 

- The habit data and the completion logs are stored in an SQLite database called:

    - habits.db
 
- The database can be reset with the following command:

    - rm habits.db
 
## 7. Troubleshooting

- If there is an issue with the databse not properly storing the habit data, not deleting the data between sessions, the streak calculation is inaccurate or any other unexpected behavior, reset the database with the following command rm habits.db then run the application again.

- If there is an issue accessing The HabitTracker project folder in the terminal with the cd command (cd /Users/YourUserName/YourFolderWhereTheApplicationIsSaved/Habit_Tracker.py) make sure that the main.py file is contained in the folder.

- If the command python main.py does not start the application, try the command python3 main.py
