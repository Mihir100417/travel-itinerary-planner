# graphs/travel_graph.py

from pydantic import BaseModel
from typing import List, Optional, Dict
from langgraph.graph import StateGraph, END

from agents.flight_agent import flight_agent
from agents.hotel_agent import hotel_agent
from agents.itinerary_agent import itinerary_agent
# from agents.budget_agent import budget_agent
# from agents.save_agent import save_agent

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
        # budget_estimate: Optional[float] = None

    def start_node(state: TravelState) -> TravelState:
        return state

    def combine_node(state: TravelState) -> TravelState:
        return state

    graph = StateGraph(TravelState)

    # Nodes
    graph.add_node("find_flights", flight_agent)
    graph.add_node("find_hotels", hotel_agent)
    graph.add_node("create_itinerary", itinerary_agent)
    # graph.add_node("calculate_budget", budget_agent)
    # graph.add_node("save_trip", save_agent)

    # Dummy branching node to initiate parallel tasks
    def start_node(state: TravelState) -> TravelState:
        return state

    graph.add_node("start", start_node)  
    graph.set_entry_point("start")        

    graph.set_entry_point("start")

    # Run flights and hotels in parallel
    graph.add_conditional_edges(
        "start",
        lambda state: {"find_flights", "find_hotels"}
    )

    graph.add_edge("find_flights", "combine")
    graph.add_edge("find_hotels", "combine")

    graph.add_node("combine", combine_node)

    graph.add_edge("combine", "create_itinerary")
    graph.add_edge("create_itinerary", END)
    # graph.set_finish_point("save_trip")

    graph.set_finish_point("create_itinerary")
    
    return graph.compile()
