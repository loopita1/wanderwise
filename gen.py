from google import genai
from dotenv import load_dotenv
from datetime import datetime
import os

def validDate(dates):
        try:
            datetime.strptime(dates, "%m/%d/%Y")
            return False
        except ValueError:
            return True

if __name__ == "__main__":
    print("Welcome to WanderWise, your personal travel assistant!")
    answer = input("Do you already have a place and date in mind? (Y/N)\n")
    load_dotenv(dotenv_path=".env")

    api_key = os.getenv("GEMINI_API_KEY")

    while answer.lower() != "y" and answer.lower() != "n":
        answer = input("Do you already have a place and date in mind?")
    if answer.lower() == "n":
        
        interaction = client.interactions.create(
            model="gemini-2.5-flash-lite",
            input=f"give a list of the 5 interesting facts for tourists to know for each country in {top3}"
        )
        print(interaction.output_text)
    else:
        location = input("Please put your desired city and country of origin, separating them with a comma (Ex: Madrid, Spain)\n")

        # check for valid start and end dates
        start = input("Please enter your intended arrival date for travel in the format MM/DD/YY\n")    
        while validDate(start):
            start = input("Please enter your intended arrival date for travel in the format MM/DD/YY\n")    
        start_date = datetime.strptime(start, "%m/%d/%Y")

        end = input("Please enter your intended departure date for travel in the format MM/DD/YY\n")
        end_date = datetime.strptime(end, "%m/%d/%Y")
        while validDate(end) or end_date <= start_date:
            end = input("Please enter your intended departure date for travel in the format MM/DD/YY\n") 
        client = genai.Client(api_key=api_key)

        # get and print gen ai response
        interaction = client.interactions.create(
            model="gemini-2.5-flash-lite",
            input=f"give a day by day itinerary of {location} for a tourist to go during {start} until {end} that are popular during the season, make sure the itinerary is clear a bulleted with dates and locations, also provide a packing list below this itinerary including the clothing to wear, the type of outlet the location has, currency, overall weather during the dates, and the primary language spoken"
        )
        print(interaction.output_text)
