from typing import List
from src.config.logger import logger
from src.services.ports.common import get_df_from_workbook
from src.services.excel_exporter import export_all_sea_rail_sheets_to_excel
from src.services.ports.sea_rail import add_location_format_df_to_list
from src.database.rail import bulk_upsert_test_rail, delete_test_rail


def sea_rail_db_pipeline(ignoreSheetTitle: List[str] = ["INFO"]):
    logger.info("Starting rail db pipeline")
    workbooks = export_all_sea_rail_sheets_to_excel()
    logger.info(f"Found {workbooks.id} workbooks")

    logger.info(f"Getting df from workbook with ignoreSheetTitle: {ignoreSheetTitle}")
    all_rail_df = get_df_from_workbook(workbooks, ignoreSheetTitle)
    logger.info(f"Found {len(all_rail_df)} dataframes")
    logger.info(all_rail_df.head(3))

    logger.info(f"Processing {len(all_rail_df)} dataframes")
    rail_list = add_location_format_df_to_list(all_rail_df)
    logger.info(f"Found {len(rail_list)} rails")

    logger.info(f"Deleting all rails from test db")
    delete_test_rail()
    logger.info(f"Finished deleting all rails from test db")

    logger.info(f"Upserting rails to test db")
    bulk_upsert_test_rail(rail_list)
    logger.info(f"Finished upserting rails to test db")

    logger.info(f"Finished rail db pipeline")
