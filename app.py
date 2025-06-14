# app.py

import streamlit as st
from graphs.travel_graph import build_travel_graph
import datetime
import pandas as pd

trip_start = datetime.date.today() + datetime.timedelta(days=1)
trip_end = trip_start + datetime.timedelta(days=5)

st.title("✈️ Travel Itinerary Planner 🏖️")

source = st.text_input("Source City", "Bengaluru")
destination = st.text_input("Destination City", "Goa")
start_date = st.date_input("Trip Start Date", value=trip_start)
end_date = st.date_input("Trip End Date", value=trip_end)

# Option 1: Predefined Interests
interests = st.multiselect("Your Interests", ["sightseeing", "food", "nature", "adventure", "history", "art", "temples", "beaches", "mountains", "forests"])

# Option 2: Free Form Interest Description
user_interest_description = st.text_area(
    "Or describe your interests in your own words (max ~50 words)",
    placeholder="I want to enjoy beaches or I want to try local food etc"
)

# Word count validation
if user_interest_description:
    word_count = len(user_interest_description.split())
    if word_count > 50:
        st.warning(f"Your description has {word_count} words. Please limit it to 50 words.")
else:
    word_count = 0


if st.button("Generate Itinerary"):
    if not source or not destination or not start_date or not end_date:
        st.error("Please complete all fields before generating!")
    elif start_date < datetime.date.today():
        st.error("Trip Start Date cannot be in the past.")
    elif end_date <= start_date:
        st.error("Trip End Date must be after the Start Date.")
    elif not interests and not user_interest_description:
        st.error("Please select interests or describe in your own words")
    elif word_count > 50:
        st.error("Please shorten the description to max 50 words")
    elif interests and user_interest_description:
        st.error("Please select interests from list or write your own but not both")
    else:
        with st.spinner("Planning your dream trip..."):
            graph = build_travel_graph()

            interests = ", ".join(interests) if interests else user_interest_description.strip()
         
            initial_state = {
                "source": source,
                "destination": destination,
                "start_date": str(start_date),
                "end_date": str(end_date),
                "interests": interests
            }
            final_state = graph.invoke(initial_state)

            st.subheader("✈️ Flights (Top 5 Roundtrip Options)")

            flights_df = pd.DataFrame(final_state["flights_data"])

            for idx, row in flights_df.iterrows():
                st.markdown(f"### ✈️ {row['carrier']} | ₹{row['price']}")
                
                # Outbound flight details
                st.markdown("**🛫 Outbound Flight**")
                col1, col2, col3, col4 = st.columns(4)
                col1.markdown(f"**Departure:** {row['departure']}")
                col2.markdown(f"**Arrival:** {row['arrival']}")
                col3.markdown(f"**Duration:** {row['duration']}")
                col4.markdown(f"**Stops:** {row['stops']}")

                # Return flight details
                st.markdown("**🛬 Return Flight**")
                col1, col2, col3, col4 = st.columns(4)
                col1.markdown(f"**Departure:** {row['Return_departure']}")
                col2.markdown(f"**Arrival:** {row['Return_arrival']}")
                col3.markdown(f"**Duration:** {row['Return_duration']}")
                col4.markdown(f"**Stops:** {row['Return_stops']}")

                st.markdown("---")

            st.subheader("🏨 Hotels (Top 5 Options)")
            for hotel in final_state["hotels"]:
                st.markdown(f"**{hotel['name']}** - [View Details]({hotel['link']})")

            st.subheader("🗺️ Suggested Itinerary")
            st.write(final_state["itinerary"])
