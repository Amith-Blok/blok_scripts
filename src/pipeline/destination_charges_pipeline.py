from src.config.logger import logger
from src.services.excel_exporter import export_destination_charges_sheet_to_excel
from src.services.destination_charges.format import format_destination_charges, format_destination_charges_to_list
from src.database.distination_charges import bulk_upsert_test_destination_charges

def destination_charges_pipeline():
    logger.info("Starting destination charges pipeline")
    df = export_destination_charges_sheet_to_excel()
    df = format_destination_charges(df)
    logger.info(f"Found {len(df)} dataframe")
    destination_charges_list = format_destination_charges_to_list(df)
    logger.info(f"Found {len(destination_charges_list)} destination charges")
    logger.info(f"Upserting {len(destination_charges_list)} destination charges to test db")
    bulk_upsert_test_destination_charges(destination_charges_list)
    logger.info(f"Finished upserting {len(destination_charges_list)} destination charges to test db")

    logger.info("Finished destination charges pipeline")