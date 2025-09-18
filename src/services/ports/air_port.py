from typing import Dict, List
from src.config.logger import logger
import pandas as pd
from time import sleep
from src.integrations.google.location_client import get_location_by_address
from src.services.ports.common import COUNTRY_REGION_MAPPER


def add_location_format_df_to_list(df: pd.DataFrame) -> List[Dict]:
    records = []
    for _, row in df.iterrows():
        airport_name = row['airport_name']
        airport_country = row["country_code"]
        airport_code = row["airport_code"]
        airport_city = row["airport_city"]
        airport_country_name=row["country_name"]

        city = str(airport_city).strip()
        country = str(airport_country).strip()
        region = COUNTRY_REGION_MAPPER[country]["region"]

        if not (city and country):
            continue

        try:
            location = get_location_by_address(address=city, country=country)
            if location and getattr(location, "results", []):
                result = location.results[0]
                lat_val = result.geometry.location.lat
                lng_val = result.geometry.location.lng
                place_id_val = result.place_id
                formatted_addr_val = result.formatted_address

                records.append(
                    {
                        "port_name": airport_name.upper() ,
                        "port_code": airport_code.upper(),
                        "port_region": region.upper(),
                        "port_address": formatted_addr_val,
                        "port_country": country.upper(),
                        "port_country_name": airport_country_name.upper(),
                        "port_type": "AIRPORT",
                        "place_id": place_id_val,
                        "location": {
                            "type": "Point",
                            "coordinates": [lng_val, lat_val],
                        },
                       
                    }
                )

                logger.info(f"Successfully processed {airport_name}, {country}")
                logger.info(f"{place_id_val}: {formatted_addr_val}")
        except Exception as e:
            logger.error(f"Failed {airport_name}, {country}: {e}")

        sleep(0.1)
    logger.info(f"Successfully processed {len(records)} rows")
    return records
