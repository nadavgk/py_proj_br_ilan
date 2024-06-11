import json
import requests
import webbrowser

def load_config(file):
    try:
        config = json.load(file)
        return config
    except json.JSONDecodeError:
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
        return []

def open_google_maps(lat, lon, api_key):
    base_url = "https://www.google.com/maps"
    maps_url = f"{base_url}?q={lat},{lon}"

    if api_key and check_street_view_availability(lat, lon, api_key):
        street_view_url = f"{base_url}?cbll={lat},{lon}&layer=c"
        webbrowser.open_new(street_view_url)
    else:
        webbrowser.open_new(maps_url)
