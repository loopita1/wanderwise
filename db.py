import sqlite3
from datetime import datetime

DB_PATH = "wanderwise.db"


def init_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS trip_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            location    TEXT NOT NULL,
            start_date  TEXT NOT NULL,
            end_date    TEXT NOT NULL,
            price       REAL,
            airline     TEXT,
            saved_at    TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()
 
 
def save_trip(location, start_date, end_date, deal=None):
    con = sqlite3.connect(DB_PATH)
    con.execute(
        "INSERT INTO trip_history (location, start_date, end_date, price, airline, saved_at) VALUES (?, ?, ?, ?, ?, ?)",
        (
            location,
            start_date,
            end_date,
            deal.get("price") if deal else None,
            deal.get("airline") if deal else None,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        )
    )
    con.commit()
    con.close()
 
 
def print_trip_history():
    con = sqlite3.connect(DB_PATH)
    rows = con.execute("SELECT location, start_date, end_date, price, airline, saved_at FROM trip_history ORDER BY saved_at DESC").fetchall()
    con.close()
 
    if not rows:
        print("No trip history yet.\n")
        return
 
    print("\n--- Your Past Trips ---")
    for location, start, end, price, airline, saved_at in rows:
        price_str = f"${price}" if price else "manual search"
        airline_str = f" via {airline}" if airline else ""
        print(f"  {location} | {start} -> {end} | {price_str}{airline_str} | saved {saved_at}")
    print()