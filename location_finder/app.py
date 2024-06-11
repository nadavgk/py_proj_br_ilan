import streamlit as st
from google_places_finder import load_config, find_nearby_places, open_google_maps
from jpg_coordinates_extractor import get_jpg_coor

st.title("Google Places Finder")

uploaded_file = st.file_uploader("Upload JSON Configuration File", type=["json"])

place_type = st.selectbox(
    "Select Place Type",
    ["restaurant", "gas_station", "cafe", "hospital", "hotel", "park", "store"]
)

latitude = st.number_input("Enter Latitude", value=40.748817, format="%.6f")
longitude = st.number_input("Enter Longitude", value=-73.985428, format="%.6f")

uploaded_jpg = st.file_uploader("Upload JPG File", type=["jpg", "jpeg"])

use_jpg_coords = st.checkbox("Use coordinates from JPG file")

if uploaded_file:
    config = load_config(uploaded_file)
    if config:
        google_api_key = config.get('GOOGLE_API_KEY')

        if not google_api_key:
            st.error("Google API Key not found in the configuration file.")
        else:
            if use_jpg_coords and uploaded_jpg:
                try:
                    # Save the uploaded JPG file
                    jpg_path = f"/tmp/{uploaded_jpg.name}"
                    with open(jpg_path, "wb") as f:
                        f.write(uploaded_jpg.getbuffer())

                    latitude, longitude = get_jpg_coor(jpg_path)
                    st.success(f"Coordinates extracted from JPG: {latitude}, {longitude}")
                except Exception as e:
                    st.error(f"Error extracting coordinates: {e}")

            if st.button("Find Nearby Places"):
                if use_jpg_coords and not uploaded_jpg:
                    st.error("Please upload a JPG file to extract coordinates.")
                else:
                    nearby_places = find_nearby_places(latitude, longitude, place_type, google_api_key)

                    if nearby_places:
                        st.write(f"Nearby {place_type.capitalize()}s:")
                        for place in nearby_places:
                            st.write(f"{place['name']} - {place['vicinity']}")

                        open_google_maps(latitude, longitude, google_api_key)
                    else:
                        st.write("No nearby places found.")
else:
    st.info("Please upload a JSON configuration file and fill in all fields.")
