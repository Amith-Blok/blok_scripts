from utils.csv_util import csv_to_list, write_data_csv
from integrations.google.location_client import get_location_by_address


def add_geolocation():
    records = []
    aiport_list = csv_to_list(path="./data/airports/eu_airports.csv")
    for airport in aiport_list:
        airport_name = airport.get("airport_name")
        airport_code = airport.get("airport_code")
        airport_city = airport.get("airport_city")
        airport_country_code = airport.get("country_code")
        print(f"{airport_name},{airport_city},{airport_country_code},{airport_code}")

        airport_location = get_location_by_address(
            query=f"{airport_city}", country=airport_country_code
        )
        airport_location_lat = airport_location.results[0].geometry.location.lat
        airport_location_lng = airport_location.results[0].geometry.location.lng
        airport_location_place_id = airport_location.results[0].place_id

        print(
            f"{airport_location_lat},{airport_location_lng},{airport_location_place_id}"
        )
        print("____________________")
        records.append(
            {
                "port_name": airport_name,
                "port_code": airport_code,
                "place_id": airport_location_place_id,
                "port_type": "AIRPORT",
                "location.type": "Point",
                "location.coordinates[0]": airport_location_lng,
                "location.coordinates[1]": airport_location_lat,
                "port_country": "CA",
            }
        )
    write_data_csv(
        path="./data/airports/formatted/eu_airports.csv",
        records=records,
        headers=[
            "port_name",
            "port_code",
            "place_id",
            "port_type",
            "location.type",
            "location.coordinates[0]",
            "location.coordinates[1]",
            "port_country",
        ],
    )


def airfreight_generater():
    records = []
    origin_port_list = csv_to_list(
        path="./data/airports/formatted/in_airports.csv", skip_subheader=False
    )
    destination_port_list = csv_to_list(
        path="./data/airports/formatted/us_airports.csv", skip_subheader=False
    )

    for origin_port in origin_port_list:
        origin_port_code = origin_port.get("port_code")
        for destination_port in destination_port_list:
            destination_port_code = destination_port.get("port_code")
            records.append(
                {
                    "start_code": origin_port_code,
                    "end_code": destination_port_code,
                    # Qatar Airways
                    "airline[0].code": "QA",
                    "airline[0].name": "Qatar Airways",
                    "airline[0].value": 2.5,
                    "airline[0].currency": "USD",
                    "airline[0].transit_time": 2,
                    # Emirates
                    "airline[1].code": "EK",
                    "airline[1].name": "Emirates",
                    "airline[1].value": 2.5,
                    "airline[1].currency": "USD",
                    "airline[1].transit_time": 2,
                }
            )
    write_data_csv(
        path="./data/airfreight/formatted/in_us_airfreight.csv",
        records=records,
        headers=[
            "start_code",
            "end_code",
            "airline[0].code",
            "airline[0].name",
            "airline[0].value",
            "airline[0].currency",
            "airline[0].transit_time",
            "airline[1].code",
            "airline[1].name",
            "airline[1].value",
            "airline[1].currency",
            "airline[1].transit_time",
        ],
    )
