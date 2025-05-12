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

    def combine_results(state: TravelState, flights: Optional[List[Dict]] = None, hotels: Optional[List[Dict]] = None) -> TravelState:
        updated_state = state.copy()
        if flights:
            updated_state.flights = flights
        if hotels:
            updated_state.hotels = hotels
        return updated_state

    graph = StateGraph(TravelState)

    graph.add_node("start", start_node)
    graph.add_node("find_flights", flight_agent)
    graph.add_node("find_hotels", hotel_agent)
    graph.add_node("combine_results", combine_results)
    graph.add_node("create_itinerary", itinerary_agent)

    graph.set_entry_point("start")        

    # Define the parallel branches
    parallel_branch = ParallelState(
        {
            "flights": flight_agent,
            "hotels": hotel_agent,
        }
    )
    
    graph.add_node("parallel_tasks", parallel_branch)
    graph.add_edge("start", "parallel_tasks")

    graph.add_edge("parallel_tasks", "combine_results")

    graph.add_edge("combine_results", "create_itinerary")
    graph.add_edge("create_itinerary", END)
    
    graph.set_finish_point("create_itinerary")
    
    return graph.compile()
