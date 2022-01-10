# %%
from datetime import date,datetime,timedelta
import json
import csv
import time
import calendar
from itertools import groupby
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
import config

@dataclass
class Holiday:
    name: str
    date: datetime
    tag: str

    def __str__ (self):
        return self.name + " (" + self.date.strftime("%Y-%m-%d") + ")"

@dataclass
class HolidayList:
    holidays: list

    def addHoliday(self):
        
        print("Add a Holiday")
        print("=============\n")

        print("Holiday: ")

        time.sleep(1)
        name = input()
        while(True):
            print("Date (example: Jan 1 2021): ")

            time.sleep(1)
            Date = input()

            try:
                Date = datetime.strptime(Date,"%b %d %Y")
                break
            except:
                print("Error: invaild date format")
                continue

        print("Tag: ")

        time.sleep(1)
        tag = input()

        temp = Holiday(name,Date,tag)

        print("\nSuccess:")
        print(temp)
        print("has been added to the holiday list.\n")
        
        self.holidays.append(temp)

    def removeHoliday(self):
        
        print("Remove a Holiday")
        print("================\n")
        while(True):
            print("Holiday Name: ")

            time.sleep(1)
            name = input()
            
            temp = self.numHolidays()

            self.holidays = [x for x in self.holidays if x.name != name]

            if temp > self.numHolidays():
                print("\nSuccess:")
                print(name)
                print("has been removed from the holiday list.\n")
                break
            else:
                print("Error: holiday not found")
                continue

    def read_json(self,filelocation):
        
        try:
            with open(filelocation,"r") as file:
                load = json.load(file)
                
                for x in load["holidays"]:
                    self.holidays.append(Holiday(x["name"],(datetime.strptime(x["date"], "%b %d %Y")).date(),x["tag"]))
        except:
            print("404")

    def save_to_json(self,filename):

        temp_list = []

        with open("Data/" + filename + ".json", "w") as file:

            for x in self.holidays:
                
                temp_list.append(x.__dict__)
            
            temp_dict = {"holidays": temp_list}

            json.dump(temp_dict,file,indent = 4, default = str)

    def save_to_csv(self,filename):
        
        with open("Data/" + filename + ".csv","w",newline="",encoding="utf-8") as file:

            writer = csv.writer(file)
            writer.writerow(self.holidays[0].__dict__)
            for x in range(0,len(self.holidays)):
                writer.writerow(self.holidays[x].__dict__.values())

    def save(self,filelocation):

        print("Saving Holiday List")
        print("====================\n")

        print("Are you sure you want to save your changes? [y/n]:")

        time.sleep(1)
        y_n = input().lower()

        if y_n == "y":
            while(True):
                print("\nwould you like it saved to json or csv? [json/csv]:")

                time.sleep(1)
                json_csv = input().lower()

                if json_csv == "json":
                    self.save_to_json(filelocation)
                    break
                elif json_csv == "csv":
                    self.save_to_csv(filelocation)
                    break
                else: 
                    print("invalid input\n")
                    continue
        else:
            print("Canceled:\nHoliday list file save canceled.")

    def tag_search(self):
        
        print("Tag Search")
        print("==========\n")

        flag = True
        print("Tag?: ")
        
        time.sleep(1)
        tag = input()

        for x in self.holidays:
            if x.tag == tag:
                flag = False
                print(x)
        
        if flag:
            print("No Holidays Found")

    def date_search(self):

        print("Date Search")
        print("===========\n")

        flag = True
        print("Date? (example: 2020-01-14): ")

        time.sleep(1)
        date = input()

        for x in self.holidays:
            if x.date.strftime("%Y-%m-%d") == date:
                flag = False
                print("\n",x)
            
        if flag:
            print("No Holidays Found")
                
    def numHolidays(self):
        return len(self.holidays)

    def scrapeHolidays(self):

        todays_date = date.today()

        counter = todays_date.year - 2

        while counter < todays_date.year + 3:

            try:
                fetchedData = requests.get("https://www.timeanddate.com/holidays/us/"+ str(counter) +"?hol=9565233").text

                soup = BeautifulSoup(fetchedData, "lxml")

                data = soup.find_all("tr", class_= "showrow")

                for holiday in data:

                    name = holiday.find("a").text
                    tag = holiday.find_all("td")[2].get_text()
                    holiday_date = datetime.strptime(holiday.find("th").text + " " +str(counter), "%b %d %Y")

                    self.holidays.append(Holiday(name,holiday_date.date(),tag))
            except:
                print("can't reach website")   

            counter += 1
        
    def getweather(self):

        todays_date = date.today()
        
        print("Would you like to see this week's weather? [y/n]:\n")

        time.sleep(1)
        y_n = input().lower()

        if y_n == "y":
            url = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/daily"

            querystring = {"lat":"43.038902","lon":"-87.906474"}

            headers = {
                'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com",
                'x-rapidapi-key': config.api_key
                }

            response = requests.request("GET", url, headers=headers, params=querystring)

            temp_dict = response.json()

            weather_data = []

            for x in temp_dict["data"]:

                weather_data.append({"date": x["datetime"],"weather": x["weather"]["description"]})
            
            temp = self.getweek(todays_date.year,todays_date.isocalendar()[1] + 1)

            temp = list(filter(lambda x: x.date.day >= todays_date.day ,temp))
            if len(temp) > 0:
                for x in temp:
                    for y in weather_data:
                        if y["date"] == x.date.strftime("%Y-%m-%d"):
                            temp_str = x.__str__()
                            print(temp_str + " " + y["weather"])
                            
            else: print("no holidays left in the week")

        else: 
            temp = self.getweek(todays_date.year,todays_date.isocalendar()[1] + 1)

            for x in temp: print(x)

    def getweek(self,year,week):

        temp = [{x:y for x,y in row.__dict__.items()} for row in self.holidays]

        calendar_data = calendar.Calendar()
        weeks = (x for y in range(1, 13) for x in calendar_data.monthdatescalendar(year, y))
        weekdays = [x for x, _ in groupby(weeks)]
        
        week_holidays = list(filter(lambda x: x["date"] in weekdays[week-1],temp))

        week_holidays = sorted(week_holidays, key = lambda x: int(x["date"].strftime("%d")))

        temp2 = []

        for x in week_holidays:

            temp2.append(Holiday(x["name"],x["date"],x["tag"]))
        
        return temp2

    def view_holidays(self):

        todays_date = date.today()
        counter = todays_date.year - 2
        
        years = [str(counter),str(counter + 1),str(counter + 2),str(counter + 3),str(counter + 4)]
        x = [x for x in range(1,53)]
        
        print("View Holidays")
        print("=============\n")

        while(True):

            try:
                print("Which year?:")

                time.sleep(1)
                year = input()

                if year not in years:
                    raise
                else: break
            except:
                print("invaild input (only has current year +- 2)")
                continue

        while(True):

            try:
                print("Which week? #[1-52, Leave blank for the current week]:\n")

                time.sleep(1)
                week = input()

                if  week != "" and int(week) not in x:
                    raise
                else: break

            except:
                print("invaild input (1-52 or blank)")
                continue

        if week == "":
            self.getweather()
        else:
            temp = self.getweek(int(year),int(week))

            for x in temp:

                print(x)

    def exit_menu(self):

        print("Exit")
        print("====\n")

        print("Are you sure you want to exit? [y/n]:")
        print("if you have unsaved changes they will be lost.")

        time.sleep(1)
        y_n = input().lower()

        if y_n == "y":
            
            print("\nGoodbye")
            return True
        else: return False

def main():

    holiday_list = HolidayList([])
    holiday_list.read_json("Data/holidays.json")

    if len(holiday_list.holidays) < 8:
        holiday_list.scrapeHolidays()

    while(True):

        menuselection = 0
        
        print("\nHoliday Menu")
        print("================")
        print("1. Add a Holiday")
        print("2. Remove a Holiday")
        print("3. Save Holiday List")
        print("4. View Holidays")
        print("5. Tag Search")
        print("6. Date Search")
        print("7. Exit\n")

        time.sleep(1)
        menuselection = input()

        if menuselection == "1":
            holiday_list.addHoliday()
        elif menuselection == "2":
            holiday_list.removeHoliday()
        elif menuselection == "3":
            print("What would you like the file to be named?")

            time.sleep(1)
            filename = input()

            holiday_list.save(filename)
        elif menuselection == "4":
            holiday_list.view_holidays()
        elif menuselection == "5":
            holiday_list.tag_search()
        elif menuselection == "6":
            holiday_list.date_search()
        elif menuselection == "7":
            flag = holiday_list.exit_menu()
            if flag:
                break
        else: print("Not Vaild Input\n")

if __name__ == "__main__":
    main()



