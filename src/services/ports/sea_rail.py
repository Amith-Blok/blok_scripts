from time import sleep
from typing import Dict, List
import pandas as pd
from src.config.logger import logger
from src.database.seaports import get_blok_seaports_by_port_code
from src.integrations.google.location_client import get_location_by_address


def add_location_format_df_to_list(df: pd.DataFrame) -> List[Dict]:
    records = []
    for _, row in df.iterrows():
        nearest_port_records = []

        port_name = str(row["port_name"]).strip()
        port_country = str(row["port_country"]).strip()
        port_code = str(row["port_code"]).strip()
        port_type = str(row["port_type"]).strip()
        port_region = str(row["port_region"]).strip()
        nearest_port_codes = str(row["nearest_port_codes"]).split(",")

        if not (port_name and port_type and port_country and port_code and port_region):
            logger.info(
                f"Skipping {port_name}, {port_type}, {port_country}, {port_code}, {port_region} Reason: Missing required fields"
            )
            continue
        if port_type.upper() != "RAIL" and port_type.upper() != "PORT":
            logger.info(
                f"Skipping {port_name}, {port_type}, {port_country}, {port_code}, {port_region}, {nearest_port_codes}.Reason: Port_Type is not RAIL or PORT"
            )
            continue
        try:

            if port_country == "IN" and port_type == "RAIL":
                print("Nearest port codes:", nearest_port_codes)
                for code in nearest_port_codes:
                    nearest_db_data = get_blok_seaports_by_port_code(
                        port_code=code.strip()
                    )
                    print("Nearest db data:", nearest_db_data)
                    nearest_port_records.append(
                        {
                            "port_name": nearest_db_data.port_name,
                            "port_code": nearest_db_data.port_code,
                        }
                    )


            location = get_location_by_address(address=port_name, country=port_country)

            if location and getattr(location, "results", []):
                result = location.results[0]
                lat_val = result.geometry.location.lat
                lng_val = result.geometry.location.lng
                place_id_val = result.place_id
                formatted_addr_val = result.formatted_address
                data = {
                    "port_name": port_name.upper(),
                    "port_code": port_code.upper(),
                    "port_region": port_region.upper(),
                    "port_address": formatted_addr_val,
                    "port_country": port_country.upper(),
                    "port_type": port_type.upper(),
                    "place_id": place_id_val,
                    "location": {
                        "type": "Point",
                        "coordinates": [
                            lng_val,
                            lat_val,
                        ],
                    },
                    "haulage_type": "EXPORT",
                }
                if nearest_port_records:
                    data["nearest_ports"] = nearest_port_records
                records.append(data)
                logger.info(f"Successfully processed {port_name}, {port_country}")
                logger.info(f"{place_id_val}: {formatted_addr_val}")
        except Exception as e:
            logger.error(f"Error getting location for {port_name}: {e}")
            continue
        sleep(0.1)
    logger.info(f"Successfully processed {len(records)} rows")
    return records
