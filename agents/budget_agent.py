# agents/budget_agent.py
from datetime import datetime
# from config import TAVILY_API_KEY
import streamlit as st
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
from tavily import TavilyClient

client = TavilyClient(api_key=TAVILY_API_KEY)

def budget_agent(state):
    flights = state.flights
    hotels = state.hotels

    avg_flight_price = sum([f.get("price_estimate", 500) for f in flights]) / len(flights)
    avg_hotel_price = sum([h.get("price_estimate", 100) for h in hotels]) / len(hotels)

    # Calculating the average expenses
    start_date = state.start_date
    end_date = state.end_date

    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date,"%Y-%m-%d").date()
    time_difference = end_date - start_date

    nights = time_difference.days
    days = time_difference.days + 1
    daily_expenses = 3000
    budget_estimate = avg_flight_price + (avg_hotel_price * nights) + (daily_expenses * days)

    return{"budget_estimate" : round(budget_estimate,2)}
