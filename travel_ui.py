import streamlit as st
import pandas as pd
from final_model import model

# ---------- Distance Map ----------
distance_map = {
    ("Delhi", "Mumbai"): 1400,
    ("Delhi", "Jaipur"): 280,
    ("Delhi", "Lucknow"): 555,
    ("Delhi", "Bhopal"): 740,
    ("Delhi", "Raipur"): 1100,
    ("Delhi", "Goa"): 1870,
    ("Delhi", "Bengaluru"): 2150,
    ("Delhi", "Kolkata"): 1530,
    ("Delhi", "Chennai"): 2180,
    ("Delhi", "Hyderabad"): 1560,

    ("Mumbai", "Jaipur"): 1140,
    ("Mumbai", "Lucknow"): 1360,
    ("Mumbai", "Bhopal"): 780,
    ("Mumbai", "Raipur"): 1115,
    ("Mumbai", "Goa"): 590
}

# ---------- Maps ----------
city_map = {
    "Delhi": 0,
    "Mumbai": 1,
    "Jaipur": 2,
    "Lucknow": 3,
    "Bhopal": 4,
    "Raipur": 5,
    "Goa": 6,
    "Bengaluru": 7,
    "Kolkata": 8,
    "Chennai": 9,
    "Hyderabad": 10
}

airline_map = {
    "IndiGo": 0,
    "Air India": 1,
    "Jet Airways": 2,
    "SpiceJet": 3,
    "Vistara": 4
}

hotel_map = {
    "Budget": 0,
    "Standard": 1,
    "Premium": 2
}

season_map = {
    "Winter": 0,
    "Summer": 1,
    "Monsoon": 2
}

user_map = {
    "General": 0,
    "Student": 1
}

tourist_places = {
    "Delhi": ["India Gate", "Qutub Minar", "Humayun's Tomb"],
    "Mumbai": ["Gateway of India", "Marine Drive", "Elephanta Caves"],
    "Jaipur": ["Hawa Mahal", "Amber Fort", "City Palace"],
    "Lucknow": ["Bara Imambara", "Rumi Darwaza", "Ambedkar Park"],
    "Bhopal": ["Upper Lake", "Van Vihar", "Sanchi Stupa"],
    "Raipur": ["Nandan Van Zoo", "Mahant Ghasidas Museum", "Purkhouti Muktangan"],
    "Goa": ["Baga Beach", "Fort Aguada", "Dudhsagar Falls"]
}

# ---------- UI ----------
st.set_page_config(page_title="Smart Travel Planner", layout="centered")

st.title("Smart Travel Planner")
st.caption("Hybrid travel budget prediction with smart destination suggestions")

# ---------- Travel Mode ----------
travel_mode = st.selectbox("Travel Mode", ["Flight", "Train", "Bus"])

# ---------- Airline ----------
if travel_mode == "Flight":
    airline = st.selectbox("Airline", list(airline_map.keys()))
else:
    airline = "IndiGo"

# ---------- Cities ----------
source = st.selectbox("Source City", list(city_map.keys()))
destination = st.selectbox("Destination City", list(city_map.keys()))

# ---------- Distance ----------
distance = distance_map.get((source, destination)) or distance_map.get((destination, source))

if distance:
    st.write(f"Estimated Distance: {distance} km")
else:
    distance = 500
    st.write("Estimated Distance: 500 km")

# ---------- Auto Duration ----------
if travel_mode == "Flight":
    duration = int(distance / 8)

elif travel_mode == "Train":
    duration = int(distance / 1)

else:
    duration = int(distance / 0.7)

st.write(f"Estimated Travel Duration: {duration} minutes")

# ---------- Flight Inputs ----------
if travel_mode == "Flight":
    stops = st.selectbox("Total Stops", [0, 1, 2, 3])
    dep_hour = st.slider("Departure Hour", 0, 23, 10)
    arrival_hour = st.slider("Arrival Hour", 0, 23, 14)
else:
    stops = 0
    dep_hour = 10
    arrival_hour = 14

# ---------- Trip Inputs ----------
journey_day = st.slider("Journey Day", 1, 31, 15)
journey_month = st.selectbox("Journey Month", [1,2,3,4,5,6,7,8,9,10,11,12])

days = st.slider("Trip Days", 1, 10, 3)
hotel = st.selectbox("Hotel Type", list(hotel_map.keys()))
season = st.selectbox("Season", list(season_map.keys()))
user_type = st.selectbox("User Type", list(user_map.keys()))

# ---------- Engineered ----------
route_count = stops + 1
week_group = journey_day % 7
fuel_index = (distance * 0.08) + (duration * 0.12)

predict = st.button("Predict Budget")

# ---------- Prediction ----------
if predict:

    sample = pd.DataFrame([[
        airline_map[airline],
        city_map[source],
        city_map[destination],
        duration,
        stops,
        journey_day,
        journey_month,
        week_group,
        dep_hour,
        arrival_hour,
        route_count,
        fuel_index,
        hotel_map[hotel],
        season_map[season],
        user_map[user_type],
        days
    ]], columns=[
        "Airline",
        "Source",
        "Destination",
        "Duration",
        "Total_Stops",
        "Journey_Day",
        "Journey_Month",
        "Week_Group",
        "Dep_Hour",
        "Arrival_Hour",
        "Route_Count",
        "Fuel_Index",
        "Hotel_Type",
        "Season",
        "User_Type",
        "Days"
    ])

    prediction = model.predict(sample)[0]

    # ---------- Mode Adjustment ----------
    if travel_mode == "Train":
        prediction *= 0.75
    elif travel_mode == "Bus":
        prediction *= 0.60

    # ---------- User Adjustment ----------
    if user_type == "Student":
        prediction *= 0.90
    else:
        prediction *= 1.10

    # ---------- Output ----------
    st.subheader("Trip Summary")
    st.success(f"Estimated Budget: ₹ {round(prediction, 2)}")

    # ---------- Tourist Suggestions ----------
    if destination in tourist_places:
        st.subheader(f"Top Places in {destination}")
        for place in tourist_places[destination]:
            st.write(f"- {place}")

    # ---------- Student Suggestions ----------
    if user_type == "Student":
        st.subheader("Budget Friendly Suggestions")
        st.write("- Prefer hostel or dormitory stay")
        st.write("- Use local transport or metro")
        st.write("- Visit free public attractions first")
        st.write("- Eat at affordable local food spots")