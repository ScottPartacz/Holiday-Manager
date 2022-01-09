from datetime import date,datetime,timedelta
import json
import csv
import time
import calendar
from itertools import groupby
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass


# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
class Holiday:     
    
    def __str__ (self):
        # String output
        # Holiday output when printed.
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
   
    def addHoliday(holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday

    def removeHoliday(HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday

    def read_json(filelocation):
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.

    def save_to_json(filelocation):
        # Write out json file to selected file.
    
    def save_to_csv(filelocation):
        # Write out csv file to selected file.
    
    def save(filelocation):
        # pick which file format you want to save too.

    def scrapeHolidays():
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.     

    def tag_search(self):
        # search for all of the holidays with a certain tag
        # print out all of the holidays with the tag

    def date_search(self):
        # search for all of the holidays with a certain date
        # print out all of the holidays with the date

    def numHolidays():
        # Return the total number of holidays in innerHolidays
    
    def getWeather(weekNum):
        # ask the user if they want to see the weather along with the holidays
        # if no then just call getweek() with the current date
        # if yes you still call getweek() to get this weeks holidays
        # then sort the list to only upcoming holidays
        # call the weather api to get the weather for today and 16 day forecast
        # append the weather date to the list of holidays
        # print the updated list

    def gettWeek():
        # find the dates for the week requested
        # filter the holiday list to those dates
        # sort the list
        # print out the sorted list
        
    def view_holidays(self):
        # ask the user with year and week number they want to see
        # call getweek() unless they want the current week then call geteweather()
    
    def exit_menu(self):
        # ask the user if they want to exit
        # make sure to tell them unsaved changes will be lost
        # exit


def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 


if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





