# agents/itinerary_agent.py

from llm import llm
from datetime import datetime

def itinerary_agent(state):
    destination = state.destination
    start_date = state.start_date
    end_date = state.end_date
    interests = ", ".join(state.interests)

    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date,"%Y-%m-%d").date()
    time_difference = end_date - start_date

    nights = time_difference.days
    days = (time_difference.days) + 1


    prompt = f"""
    Create a {days}-day travel itinerary for a trip to {destination} from {start_date} to {end_date}.
    The user is interested in this: {interests}.
    Keep it structured day-wise with a small description for each day.
    Don't include budget and accomodation part anywhere.
    Don't keep any plan on last date post lunch.
    """
    
    # prompt_char_count = len(prompt)
    response = llm.invoke(prompt)
    # return {"itinerary": response[prompt_char_count:]}
    return {"itinerary": response.content.strip()}
