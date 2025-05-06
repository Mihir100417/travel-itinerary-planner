# agents/itinerary_agent.py

from llm import llm

def itinerary_agent(state):
    destination = state.destination
    start_date = state.start_date
    end_date = state.end_date
    interests = ", ".join(state.interests)

    prompt = f"""
    Create a 5-day travel itinerary for a trip to {destination} from {start_date} to {end_date}.
    Focus on interests like {interests}.
    Keep it structured day-wise with a small description.
    Don't include budget and accomodation part anywhere.
    """
    
    # prompt_char_count = len(prompt)
    response = llm.invoke(prompt)
    # return {"itinerary": response[prompt_char_count:]}
    return {"itinerary": response.content}
