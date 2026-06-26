from google import genai
from dotenv import load_dotenv
from datetime import datetime
import os


def valid_date(dates):
    try:
        datetime.strptime(dates, "%m/%d/%Y")
        return False
    except ValueError:
        return True


def generate_trip_summary(location, start, end, exchange_data, deal=None):
    load_dotenv(dotenv_path=".env")
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
            f"The traveler has a flight deal: "
            f"{deal['departure_airport']} → "
            f"{deal['arrival_airport']} on "
            f"{deal['airline']} for ${deal['price']} "
            f"(average price ${deal['average_price']}, "
            f"saving ${deal['price_difference']}, "
            f"{deal['discount_percentage']}% off) "
            f"with {deal['stops']} stop(s). "
            f"Travel dates: {start} to {end}. "
            f"Flight URL: {deal['url']}"
        )
    else:
        flight_info = (
            f"No specific flight deal was selected. Include a brief note about"
            f" the approximate distance and flight duration to "
            f"{location}, and the likely destination airport there."
        )

    exchange_info = (
        f"Exchange rate: 1 {base} = {current_rate:.4f} {target} today. "
        f"The {months}-month average was {average_rate:.4f} {target}. "
        f"The current rate is {percent_difference:+.2f}% vs the average. "
    )

    prompt = (
        f"give a day by day itinerary of {location} for a tourist to go "
        f"during {start} until {end} that are popular during the season, make "
        f"sure the itinerary is clear and bulleted with dates and locations, "
        f"also provide a packing list below this itinerary including the "
        f"clothing to  wear, the type of outlet the location has, currency, "
        f"overall weather during the dates, and the primary language spoken."
        f"Flight information: {flight_info}\n\n"
        f"Exchange rate information: {exchange_info} "
        f"Comment briefly on whether now is a good or bad time to exchange "
        f"USD to {target} based on this trend."
    )

    interaction = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt

    )
    print(interaction.text)
