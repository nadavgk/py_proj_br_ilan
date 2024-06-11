import json
import requests
import streamlit as st
import webbrowser


def load_config(file):
    try:
        config = json.load(file)
        return config
    except json.JSONDecodeError:
        st.error("Error: JSON configuration file is not valid.")
        return None


def check_street_view_availability(lat, lon, api_key):
    metadata_url = (
        f"https://maps.googleapis.com/maps/api/streetview/metadata?"
        f"location={lat},{lon}&key={api_key}"
    )
    response = requests.get(metadata_url)
    data = response.json()
    return data.get("status") == "OK"


def find_nearby_places(lat, lon, place_type, api_key):
    places_url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        f"location={lat},{lon}&radius=1500&type={place_type}&key={api_key}"
    )
    response = requests.get(places_url)
    places_data = response.json()
    if places_data.get("status") == "OK":
        return places_data.get("results")
    else:
        st.error(f"Error finding nearby places: {places_data.get('status')} - {places_data.get('error_message')}")
        return []


def open_google_maps(lat, lon, api_key):
    base_url = "https://www.google.com/maps"
    maps_url = f"{base_url}?q={lat},{lon}"

    if api_key and check_street_view_availability(lat, lon, api_key):
        street_view_url = f"{base_url}?cbll={lat},{lon}&layer=c"
        # Open Street View if available
        webbrowser.open_new(street_view_url)
    else:
        # Open Google Maps at the given latitude and longitude
        webbrowser.open_new(maps_url)


# Streamlit interface
st.title("Google Places Finder")

uploaded_file = st.file_uploader("Upload JSON Configuration File", type=["json"])

place_type = st.selectbox(
    "Select Place Type",
    ["restaurant", "gas_station", "cafe", "hospital", "hotel", "park", "store"]
)

latitude = st.number_input("Enter Latitude", value=40.748817, format="%.6f")
longitude = st.number_input("Enter Longitude", value=-73.985428, format="%.6f")

if uploaded_file and place_type and latitude and longitude:
    config = load_config(uploaded_file)
    if config:
        google_api_key = config.get('GOOGLE_API_KEY')

        if st.button("Find Nearby Places"):
            # Find nearby places
            nearby_places = find_nearby_places(latitude, longitude, place_type, google_api_key)

            if nearby_places:
                st.write(f"Nearby {place_type.capitalize()}s:")
                for place in nearby_places:
                    st.write(f"{place['name']} - {place['vicinity']}")

                # Optionally open Google Maps
                open_google_maps(latitude, longitude, google_api_key)
