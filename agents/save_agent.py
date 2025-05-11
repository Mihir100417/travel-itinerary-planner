# agents/save_agent.py
# from config import TAVILY_API_KEY
import streamlit as st
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
from tavily import TavilyClient

client = TavilyClient(api_key=TAVILY_API_KEY)

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def save_agent(state):
    destination = state.destination
    itinerary = state.itinerary
    # budget_estimate = state.budget_estimate

    filename = f"{destination}_itinerary_planner.pdf"

    # Create PDF
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    text_obj = c.beginText(40, height - 50)
    text_obj.setFont("Helvetica", 12)

    text_obj.textLine(f"Destination: {destination}")
    # text_obj.textLine(f"Estimated Budget: ${budget_estimate}")
    text_obj.textLine("")

    text_obj.textLine("Travel Itinerary:")
    text_obj.textLine("-----------------")

    # Wrap long lines manually
    for line in itinerary.split('\n'):
        for chunk in [line[i:i+90] for i in range(0, len(line), 90)]:
            text_obj.textLine(chunk)

    c.drawText(text_obj)
    c.showPage()
    c.save()

    return {"saved_file": filename}
