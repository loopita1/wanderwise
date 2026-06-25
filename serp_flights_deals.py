import serpapi
import os
import json


def all_flight_deals(departure_id):
    key = os.getenv("SERP_API_KEY")

    if key is None:
        return("ERROR, API KEY NOT FOUND")

    client = serpapi.Client(api_key=key)

    results = dict(client.search({
    "engine": "google_flights_deals",
    "departure_id": departure_id,
    "currency": "USD"
    }))

    return results.get("deals", [])

def filtered_deals(deals):
    price = deals.get("price")
    average_price = deals.get("average_price")
    
    price_difference = None

    if price is not None and average_price is not None:
        price_difference = average_price - price
    
    return {
        "location" : deals.get("name"),
        "country" : deals.get("country"),
        "departure_airport" : deals.get("departure_airport_code"),
        "arrival_airport" : deals.get("arrival_airport_code"),
        "start_date" : deals.get("start_date"),
        "end_date" : deals.get("end_date"),
        "price" : price,
        "average_price" : average_price,
        "price_difference" : price_difference,
        "discount_percentage" : deals.get("discount_percentage"),
        "airline" : deals.get("airline"),
        "stops" : deals.get("stops"),
        "url" : deals.get("flight_link") or deals.get("serpapi_flight_link")
    }

def filter_top_deals(deals, different_countries = True, max_deals = 5, stops_filter=0):
    seen_countries = set()
    cleaned_deals = []

    for deal in deals:
        country = deal.get("country")
        stops = deal.get("stops")

        if country is None:
            continue
        if stops is None:
            continue


        if stops > stops_filter:
            continue
        
        if different_countries:
            if country in seen_countries:
                continue
        
        cleaned_deals.append(filtered_deals(deal))
        seen_countries.add(country)

        if len(cleaned_deals) == max_deals:
            break
    
    return cleaned_deals

        





