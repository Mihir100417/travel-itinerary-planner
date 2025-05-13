# agents/flight_agent.py

# from config import TAVILY_API_KEY
import streamlit as st
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
from tavily import TavilyClient

client = TavilyClient(api_key=TAVILY_API_KEY)

def flight_agent(state):
    source = state.source
    destination = state.destination
    start_date = state.start_date
    end_date = state.end_date

    query = f"""
            You are a flight booking assistant helping a user plan their travel.
            
            Return a list of **top 5 available flights** for the following travel details:
            - **Source city**: {source}
            - **Destination city**: {destination}
            - **Departure date**: {start_date}
            - **Return date** : {end_date}
            
            For each flight, include:
            - Airline Name
            - Departure time and arrival time
            - Duration
            - Price in INR (estimate)
            - A dummy booking link (e.g., https://example.com/flight123)
            
            Output should be a JSON list of 5 objects with the following structure:
            [
              {{
                "title": "Airline XYZ 123",
                "departure_time": "10:30 AM",
                "arrival_time": "12:45 PM",
                "duration": "2h 15m",
                "price": " Rs.200",
                "link": "https://example.com/xyz123"
              }},
              ...
            ]
            Keep it realistic and useful.
            """
    response = client.search(query=query, search_depth="advanced")
    flights = response["results"]

    processed_flights = []
    for flight in flights:
        processed_flights.append({
            "title": flight["title"],
            "link": flight["url"],
            "price_estimate": flight.get("price", 500),
            "hops": flight.get("hops", 1)
        })

    processed_flights = sorted(processed_flights, key=lambda x: (x["price_estimate"], x["hops"]))
    
    return {"flights": processed_flights[:5]}
