from google import genai
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv(dontenv_path=".env")

def validDate(dates):
        try:
            datetime.strptime(dates, "%m/%d/%Y")
            return False
        except ValueError:
            return True



def generate_trip_summary(location, start, end, exchange_data, deal=None):
  api_key = os.getenv("GEMINI_API_KEY")
  client = genai.Client(api_key=api_key)
  base = exchange_data.get("base")
  target = exchange_data.get("target")
  current_rate = exchange_data.get("current_rate")
  average_rate = exchange_data.get("average_rate")
  percent_difference = exchange_data.get("percent_difference")
  months = exchange_data.get("months")


  if deal:
    flight_info = (
      f"The traveler has a flight deal: {deal['departure_airport']} → {deal['arrival_airport']} "
      f"on {deal['airline']} for ${deal['price']} (average price ${deal['average_price']}, "
      f"saving ${deal['price_difference']}, {deal['discount_percentage']}% off) with {deal['stops']} stop(s). "
      f"Travel dates: {start} to {end}. Flight URL: {deal['url']}"
        )
  else:
    flight_info = (
      f"No specific flight deal was selected. Include a brief note about the approximate"
      f"distance and flight duration to {location}, and the likely destination airport there."

    )
  
  exchange_info = (
    f"Exchange rate: 1 {base} = {current_rate:.4f} {target} today. "
    f"The {months}-month average was {average_rate:.4f} {target}. "
    f"The current rate is {percent_difference:+.2f}% vs the average. "
  )

  prompt = (
    f"give a day by day itinerary of {location} for a tourist to go during {start} until {end} "
    f"that are popular during the season, make sure the itinerary is clear and bulleted with dates and locations, "
    f"also provide a packing list below this itinerary including the clothing to wear, the type of outlet the "
    f"location has, currency, overall weather during the dates, and the primary language spoken. "
    f"\n\nFlight information: {flight_info}"
    f"\n\nExchange rate information: {exchange_info} Comment briefly on whether now is a good or bad time "
    f"to exchange USD to {target} based on this trend."
  )

  interaction = client.models.generate_content(
    model ="gemini-2.5-flash-lite",
    contents=prompt

  )
  print(interaction.text)






