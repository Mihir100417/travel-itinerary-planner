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

    query = f"Flights from {source} to {destination} departing on {start_date} and returning on {end_date} best options"
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
