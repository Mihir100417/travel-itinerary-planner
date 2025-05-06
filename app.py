# app.py

import streamlit as st
from graphs.travel_graph import build_travel_graph
import datetime
# from config import TAVILY_API_KEY, OPENAI_API_KEY, HUGGINGFACEHUB_API_TOKEN

trip_start = datetime.date.today() + datetime.timedelta (days=1) 
trip_end = trip_start + datetime.timedelta (days=5) 

st.title("✈️Travel Itinerary Planner🏖️")

destination = st.text_input("Destination City", "Goa")
start_date = st.date_input("Trip Start Date", value = trip_start)
end_date = st.date_input("Trip End Date", value = trip_end)
interests = st.multiselect("Your Interests", ["sightseeing", "food", "nature", "adventure", "history", "art", "temples", "beaches", "mountains", "forests"])

if st.button("Generate Itinerary"):
    if destination and start_date and end_date and interests:
        with st.spinner("Planning your dream trip..."):
            graph = build_travel_graph()
            initial_state = {
                "destination": destination,
                "start_date": str(start_date),
                "end_date": str(end_date),  
                "interests": interests
            }
            final_state = graph.invoke(initial_state)

            st.subheader("✈️ Flights (Top 5 Options)")
            for flight in final_state["flights"]:
                st.markdown(f"**{flight['title']}** - [View Details]({flight['link']})")

            st.subheader("🏨 Hotels (Top 5 Options)")
            for hotel in final_state["hotels"]:
                st.markdown(f"**{hotel['name']}** - [View Details]({hotel['link']})")

            st.subheader("🗺️ Suggested Itinerary")
            st.write(final_state["itinerary"])

            st.subheader("💰 Estimated Budget")
            st.success(f"Total Estimated Budget: **₹{final_state['budget_estimate']}**")

            # print("Final state keys:", final_state.keys())
    
            # if "saved_file" in final_state:
            #     with open(final_state["saved_file"], "rb") as f:
            #         st.download_button("Download Itinerary", f, file_name=final_state["saved_file"])
            # else:
            #     st.error("PDF was not generated. 'saved_file' key not found in final state.")
    else:
        st.error("Please complete all fields before generating!")
