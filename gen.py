from google import genai
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

api_key = os.getenv("GEMINI_API_KEY")

location = input("Please put your desired city and country of origin, separating them with a comma (Ex: Madrid, Spain)\n")
start = input("Please enter your intended arrival date for travel in the format MM/DD/YY\n")
end = input("Please enter your intended departure date for travel in the format MM/DD/YY\n")

client = genai.Client(api_key=api_key)


interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=f"give a day by day itinerary of {location} for a tourist to go during {start} until {end} that are popular during the season, make sure the itinerary is clear a bulleted with dates and locations, also provide a packing list below this itinerary including the clothing to wear, the type of outlet the location has, currency, overall weather during the dates, and the primary language spoken"
)
print(interaction.output_text)

# stream = client.interactions.create(
#     model="gemini-3.5-flash",
#     input=f"give a day by day itinerary of {location} for a tourist to go during {start} until {end} that are popular during the season, make sure the itinerary is clear a bulleted with dates and locations, also provide a packing list below this itinerary including the clothing to wear, the type of outlet the location has, currency, overall weather during the dates, and the primary language spoken",
#     stream=True
# )

# for event in stream:
#     print(event)


