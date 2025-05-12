# graphs/travel_graph.py

from pydantic import BaseModel
from typing import List, Optional, Dict
from langgraph.graph import StateGraph, END

from agents.flight_agent import flight_agent
from agents.hotel_agent import hotel_agent
from agents.itinerary_agent import itinerary_agent

def build_travel_graph():

    class TravelState(BaseModel):
        source: str
        destination: str
        start_date: str
        end_date: str
        interests: Optional[List[str]] = [] 
        flights: Optional[List[Dict]] = []
        hotels: Optional[List[Dict]] = []
        itinerary: Optional[List[Dict]] = []
    
    graph = StateGraph(TravelState)

    # Nodes
    graph.add_node("find_flights", flight_agent)
    graph.add_node("find_hotels", hotel_agent)
    graph.add_node("create_itinerary", itinerary_agent)
    
    # Edges
    graph.set_entry_point("find_flights")

    graph.add_edge("find_flights", "find_hotels")
    graph.add_edge("find_hotels", "create_itinerary")
    graph.add_edge("create_itinerary", END)

    graph.set_finish_point("create_itinerary")
    
    return graph.compile()
