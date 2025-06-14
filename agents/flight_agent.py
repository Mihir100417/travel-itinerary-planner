# agents/flight_agent.py

# from config import TAVILY_API_KEY
# from tavily import TavilyClient

# client = TavilyClient(api_key=TAVILY_API_KEY)

# def flight_agent(state):
#     source = state.source
#     destination = state.destination
#     start_date = state.start_date
#     end_date = state.end_date

#     query = f"Flights from {source} to {destination} departing on {start_date} and returning on {end_date} best options"
#     response = client.search(query=query, search_depth="advanced")
#     flights = response["results"]

#     processed_flights = []
#     for flight in flights:
#         processed_flights.append({
#             "title": flight["title"],
#             "link": flight["url"],
#             "price_estimate": flight.get("price", 500),
#             "hops": flight.get("hops", 1)
#         })

#     processed_flights = sorted(processed_flights, key=lambda x: (x["price_estimate"], x["hops"]))
    
#     return {"flights": processed_flights[:5]}

# from config import AMADEUS_CLIENT_ID, AMADEUS_CLIENT_SECRET
import streamlit as st
from amadeus import Client, ResponseError
import re
import pandas as pd

AMADEUS_CLIENT_ID = st.secrets["AMADEUS_CLIENT_ID"]
AMADEUS_CLIENT_SECRET = st.secrets["AMADEUS_CLIENT_SECRET"]

amadeus = Client(
    client_id = AMADEUS_CLIENT_ID,
    client_secret = AMADEUS_CLIENT_SECRET
)
    
def get_iata_code(city_name):
    try:
        response = amadeus.reference_data.locations.get(
            keyword=city_name,
            subType='CITY'
        )
        return response.data[0]['iataCode']
    except Exception:
        raise ValueError(f"Could not find IATA code for city: {city_name}")

def get_airline_name(code):
    try:
        res = amadeus.reference_data.airlines.get(airlineCodes=code)
        return res.data[0]['businessName'] if res.data else code
    except:
        return code

def parse_duration(iso_duration):
    """Converts 'PT2H15M' to '2h 15m' for readability."""
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?", iso_duration)
    if not match:
        return ""
    hours = match.group(1) or "0"
    minutes = match.group(2) or "0"
    return f"{hours}h {minutes}m"

def search_roundtrip_flights(origin_city, destination_city, departure_date, return_date):
    try:
        origin = get_iata_code(origin_city)
        destination = get_iata_code(destination_city)

        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=departure_date,
            returnDate=return_date,
            adults=1,
            currencyCode='INR',
            max=10
        )

        results = []

        for offer in response.data:
            itineraries = offer['itineraries']

            # Outbound segment
            outbound = itineraries[0]['segments']
            out_first = outbound[0]
            out_last = outbound[-1]
            out_stops = len(outbound) - 1
            out_duration = parse_duration(itineraries[0]['duration'])

            # Inbound segment
            inbound = itineraries[1]['segments'] if len(itineraries) > 1 else []
            in_first = inbound[0] if inbound else {}
            in_last = inbound[-1] if inbound else {}
            in_stops = len(inbound) - 1 if inbound else None
            in_duration = parse_duration(itineraries[1]['duration']) if len(itineraries) > 1 else None

            results.append({
                'carrier': out_first['carrierCode'],
                'price': float(offer['price']['total']),
                'departure': out_first['departure']['at'],
                'arrival': out_last['arrival']['at'],
                'duration': out_duration,
                'stops': out_stops,
                'Return_departure': in_first.get('departure', {}).get('at'),
                'Return_arrival': in_last.get('arrival', {}).get('at'),
                'Return_duration': in_duration,
                'Return_stops': in_stops,
            })

        sorted_results = sorted(results, key=lambda x: (x['price'], x['stops'] + (x['Return_stops'] or 0)))

        return sorted_results

    except ResponseError as error:
        print(error)
        return []

def postprocessing(output_list):
    df = pd.DataFrame(output_list)
    df['carrier'] = df['carrier'].apply(get_airline_name)
    df['departure'] = pd.to_datetime(df['departure'])
    df['Return_departure'] = pd.to_datetime(df['Return_departure'])
    df = df.sort_values(by = ['departure','Return_departure'], ascending= [True, False], ignore_index=True)
    df['departure'] = pd.to_datetime(df['departure']).dt.strftime('%Y-%m-%d %I:%M %p')
    df['arrival'] = pd.to_datetime(df['arrival']).dt.strftime('%Y-%m-%d %I:%M %p')
    df['Return_departure'] = pd.to_datetime(df['Return_departure']).dt.strftime('%Y-%m-%d %I:%M %p')
    df['Return_arrival'] = pd.to_datetime(df['Return_arrival']).dt.strftime('%Y-%m-%d %I:%M %p')
    return(df)

def flight_agent(state):
    origin_city = state.source
    destination_city = state.destination
    departure_date = state.start_date
    return_date = state.end_date

    flights = search_roundtrip_flights(origin_city, destination_city, departure_date, return_date)
    flights_data = postprocessing(flights)

    return {"flights_data": flights_data.to_dict(orient="records")}
