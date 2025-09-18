import requests
from src.config.settings import GOOGLE_MAPS_API_KEY
from src.models.external.google_location import GoogleLocationResponse


def get_location_by_address(address: str, country="IN") -> GoogleLocationResponse:
    countryParam = (
        "locationrestriction=rectangle:36.0,-25.0|71.185,60.0"
        if country == "EU"
        else f"components=country:{country}"
    )
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&{countryParam}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    response_json = response.json()
    google_location_response = GoogleLocationResponse(**response_json)
    return google_location_response


def get_location_by_lat_lng(lat: float, lng: float) -> GoogleLocationResponse:
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    response_json = response.json()
    google_location_response = GoogleLocationResponse(**response_json)
    return google_location_response


def get_location_by_place_id(place_id: str) -> GoogleLocationResponse:
    url = f"https://maps.googleapis.com/maps/api/geocode/json?place_id={place_id}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    response_json = response.json()
    google_location_response = GoogleLocationResponse(**response_json)
    return google_location_response
