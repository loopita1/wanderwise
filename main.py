from serp_flights_deals import all_flight_deals, filter_top_deals
from exchange_rates import exchange_rate_difference
from gen import generate_trip_summary, validDate
import datetime


 
COUNTRY_CURRENCY = {
    "japan": "JPY", "france": "EUR", "germany": "EUR", "italy": "EUR",
    "spain": "EUR", "mexico": "MXN", "canada": "CAD", "uk": "GBP",
    "united kingdom": "GBP", "australia": "AUD", "brazil": "BRL",
    "india": "INR", "thailand": "THB", "indonesia": "IDR",
    "south korea": "KRW", "china": "CNY", "colombia": "COP",
    "argentina": "ARS", "peru": "PEN", "chile": "CLP", "portugal": "EUR",
    "netherlands": "EUR", "greece": "EUR", "turkey": "TRY", "egypt": "EGP",
    "vietnam": "VND", "philippines": "PHP", "malaysia": "MYR",
}

def get_currency(country):
  return COUNTRY_CURRENCY.get(country.lower(), "USD")


def main():
  print("Welcome to WanderWise, your personal travel assistant! ")

  departure_id = input("\nWhat is your departure airport code? (e.g. JFK, LAX, DFW): ").strip().upper()

  see_deals = input("Would you like to see current flight deals from your airport? (Y/N): ").strip().lower()
