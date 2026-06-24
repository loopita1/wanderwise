import serpapi
import os
import json


def all_flight_deals(departure_id):
    key = "19e623d3d1663c0740835797df100dfadc565c1d61d6aea4e0533f1bbe402bcb"
    client = serpapi.Client(api_key=key)
    results = client.search({
    "engine": "google_flights_deals",
    "departure_id": departure_id,
    "currency": "USD"
    })

    return results.get("deals", [])

#def filtered_deals(deals):


