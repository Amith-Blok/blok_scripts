from src.database.airfreight import  bulk_upsert_blok_airfreights, bulk_upsert_test_airfreights, delete_test_airfreights
from src.services.air_freight.helper import  combined_airfreight_export_and_import_df, combined_airfreight_export_df, combined_airfreight_import_df
from src.config.logger import logger
from src.services.air_freight.helper import format_airfreight_df_to_list


def airfreight_db_pipeline():
    logger.info("Starting airfreight db pipeline")
    combined_df = combined_airfreight_export_and_import_df()
    logger.info(f"Found {len(combined_df)} dataframes")

    logger.info("Formatting airfreight df to list")
    airfreight_list = format_airfreight_df_to_list(combined_df)
    logger.info(f"Found {len(airfreight_list)} airfreight")

    # logger.info("Deleting all airfreight from test db")
    # delete_blok_airfreights()
    # logger.info("Finished deleting all airfreight from test db")

    logger.info("Upserting airfreight to test db")
    bulk_upsert_blok_airfreights(airfreight_list)
    logger.info("Finished airfreight db pipeline")
