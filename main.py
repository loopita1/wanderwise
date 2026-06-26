from serp_flights_deals import all_flight_deals, filter_top_deals
from exchange_rates import exchange_rate_difference
from gen import generate_trip_summary, valid_date
from db import init_db, save_trip, print_trip_history
from datetime import datetime


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
    init_db()

    print("Welcome to WanderWise, your personal travel assistant!")

    show_history = input("\nWould you like to see your past trips before we start? (Y/N): ").strip().lower()
    if show_history == "y":
        print_trip_history()

    departure_id = input("What is your departure airport code? (e.g. JFK, LAX, IAH): ").strip().upper()

    see_deals = input("Would you like to see current flight deals from your airport? (Y/N): ").strip().lower()
    while see_deals not in ("y", "n"):
        see_deals = input("Please enter Y or N: ").strip().lower()

    selected_deal = None
    location = None
    start = None
    end = None

    if see_deals == "y":
        max_input = input("How many deals would you like to see?: ").strip()
        max_deals = int(max_input) if max_input.isdigit() else 5

        stops_input = input("Max number of stops? : ").strip()
        stops_filter = int(stops_input) if stops_input.isdigit() else 1

        diff_countries_input = input("Only show one deal per country (Y/N): ").strip().lower()
        different_countries = diff_countries_input != "n"

        print("\nFetching flight deals...\n")
        raw_deals = all_flight_deals(departure_id)
        deals = filter_top_deals(raw_deals, different_countries, max_deals, stops_filter)

        if not deals:
            print("No deals found. Let's plan manually instead.\n")
            see_deals = "n"
        else:
            print("Here are the available deals:\n")
            for i, deal in enumerate(deals):
                print(f"[{i}] {deal['location']}, {deal['country']} — ${deal['price']} "
                      f"(avg ${deal['average_price']}) | {deal['airline']} | Stops: {deal['stops']}")

            while True:
                pick = input("\nEnter the index number of the deal you want: ").strip()
                if pick.isdigit() and int(pick) < len(deals):
                    selected_deal = deals[int(pick)]
                    break
                print(f"Please enter a number between 0 and {len(deals) - 1}.")

            location = f"{selected_deal['location']}, {selected_deal['country']}"
            start = datetime.strptime(selected_deal["start_date"], "%Y-%m-%d").strftime("%m/%d/%Y")
            end = datetime.strptime(selected_deal["end_date"], "%Y-%m-%d").strftime("%m/%d/%Y")

    if see_deals == "n":
        location = input("\nPlease put your desired city and country, separating them with a comma (Ex: Madrid, Spain): ").strip()

        start = input("Please enter your intended arrival date for travel in the format MM/DD/YYYY: ").strip()
        while valid_date(start):
            start = input("Please enter your intended arrival date for travel in the format MM/DD/YYYY: ").strip()
        start_date = datetime.strptime(start, "%m/%d/%Y")

        end = input("Please enter your intended departure date for travel in the format MM/DD/YYYY: ").strip()
        end_date = datetime.strptime(end, "%m/%d/%Y")
        while valid_date(end) or end_date <= start_date:
            end = input("Please enter your intended departure date for travel in the format MM/DD/YYYY: ").strip()
            if not valid_date(end):
                end_date = datetime.strptime(end, "%m/%d/%Y")

    country = selected_deal["country"] if selected_deal else location.split(",")[-1].strip()
    save_trip(location, start, end, deal=selected_deal)

    target_currency = get_currency(country)
    print(f"\nFetching exchange rate (USD -> {target_currency})...\n")
    exchange_data = exchange_rate_difference("USD", target_currency)

    print("Generating your trip summary...\n")
    generate_trip_summary(location, start, end, exchange_data, deal=selected_deal)


if __name__ == "__main__":
    main()