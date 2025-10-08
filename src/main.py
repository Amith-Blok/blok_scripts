from src.database.seaports import create_seaport_map
from src.integrations.google.location_client import (
    get_location_by_address,
    get_location_by_place_id,
)
from src.pipeline.sea_freight_db_pipeline import sea_freight_db_pipeline
from src.pipeline.sea_rail_db_pipeline import sea_rail_db_pipeline
from src.pipeline.air_port_db_pipeline import airport_db_pipeline
from src.config.logger import logger, config_logger
from src.services.air_freight.excel_to_csv import airfreight_excel_to_csv
from src.pipeline.airfreight_db_pipeline import airfreight_db_pipeline
from src.services.exchange_rates import get_exchange_rates
from src.pipeline.destination_charges_pipeline import destination_charges_pipeline


def main():
    config_logger()
    sea_freight_db_pipeline(["IS","CA"])
    # get_exchange_rates()
    # sea_rail_db_pipeline()
    # destination_charges_pipeline()
    # airfreight_db_pipeline()
    # create_seaport_map()
    # logger.info("Starting main")
    # response=get_location_by_address(address="Hong Kong",country="HK")
    # logger.info(f"formatted address: {response.results[0].formatted_address}")
    # logger.info(f"place_id: {response.results[0].place_id}")


if __name__ == "__main__":
    main()
