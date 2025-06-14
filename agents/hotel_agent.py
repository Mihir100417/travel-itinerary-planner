# agents/hotel_agent.py

# from config import TAVILY_API_KEY
import streamlit as st
from tavily import TavilyClient

TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
client = TavilyClient(api_key=TAVILY_API_KEY)

def hotel_agent(state):
    destination = state.destination
    start_date = state.start_date
    end_date = state.end_date

    query = f"Top hotels in {destination} for stay from {start_date} to {end_date} affordable and good reviews"
    response = client.search(query=query, search_depth="advanced")
    hotels = response["results"]

    processed_hotels = []
    for hotel in hotels:
        processed_hotels.append({
            "name": hotel["title"],
            "link": hotel["url"],
            "price_estimate": hotel.get("price", 100),
        })

    processed_hotels = sorted(processed_hotels, key=lambda x: x["price_estimate"])
    
    return {"hotels": processed_hotels[:5]}
