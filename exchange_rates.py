import requests
from datetime import date,timedelta

API_URL = "https://api.frankfurter.dev/v2"


def get_date(months):
    return date.today() - timedelta(days = months * 30)


def exchange_rate_difference(base_currency, target_currency, months = 12):
    base_currency = base_currency.upper()
    target_currency = target_currency.upper()

    if base_currency == target_currency:
        return {
            "base" : base_currency,
            "target" : target_currency,
            "current_rate" : 1,
            "average_rate" : 1,
            "percent_difference" : 0,
            "months" : months
        }
    
    start_date = get_date(months)

    request = requests.get(f"{API_URL}/rate/{base_currency}/{target_currency}")
    latest_rates = request.json()

    current_rate = latest_rates['rate']

    historical_request = requests.get(f"{API_URL}/rates", params={
        "from" : start_date,
        "base" : base_currency,
        "quotes" : target_currency    })    

    historical_data = historical_request.json()
    rates = []

    for row in historical_data:
        if row.get("quote") == target_currency:
            rates.append(row['rate'])

    if len(rates) == 0:
        return "No historical data found"
    
    average_rate = sum(rates) / len(rates)
    percent_difference = ((current_rate - average_rate) / average_rate) * 100

    return {
        "base": base_currency,
        "target": target_currency,
        "current_rate": current_rate,
        "average_rate": average_rate,
        "percent_difference": percent_difference,
        "months": months       
    }


if __name__ == "__main__":
    result = exchange_rate_difference("USD", "JPY", 36)

    print("----------------------")
    print(f"{result['base']} to {result['target']}")
    print(f"Current Rate: {result['current_rate']:.4f}")
    print(f"{result['months']}-Month Average: {result['average_rate']:.4f}")
    print(f"Percent Difference: {result['percent_difference']:.2f}%")