from typing import List
from src.database.airport import bulk_upsert_test_airports, delete_test_airports
from src.services.excel_exporter import export_all_air_port_sheets_to_excel
from src.config.logger import logger
from src.services.ports.common import get_df_from_workbook
from src.services.ports.air_port import add_location_format_df_to_list


def airport_db_pipeline(ignore_sheet_title: List[str] = ["INFO"], include_sheet_title: List[str] = None):

    logger.info("Starting airport db pipeline")
    workbooks = export_all_air_port_sheets_to_excel()
    logger.info(f"Found {workbooks.id} workbooks")

    logger.info(f"Getting df from workbook with ignore_sheet_title: {ignore_sheet_title}")
    all_airport_df = get_df_from_workbook(workbooks, ignore_sheet_title, include_sheet_title)
    logger.info(f"Found {len(all_airport_df)} dataframes")

    logger.info(f"Adding Location Info")
    airport_list = add_location_format_df_to_list(all_airport_df)
    logger.info(f"Found {len(airport_list)} airports")

    logger.info(f"Deleting all airports from test db")
    delete_test_airports()
    logger.info(f"Finished deleting all airports from test db")

    logger.info(f"Upserting airports to test db")
    bulk_upsert_test_airports(airport_list)
    logger.info(f"Finished airport db pipeline")