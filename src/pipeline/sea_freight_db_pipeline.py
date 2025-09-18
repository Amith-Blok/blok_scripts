import json
from src.config.logger import logger
from typing import List
from src.database.line_rates import delete_test_lines, upsert_test_lines
from src.pipeline.freight_excel_export_pipeline import freight_excel_export_pipeline
from src.services.freight.locals_charges_adder import (
    ind_export_locals_charges_adder_by_df,
)
from src.services.sea_freight.helper import (
    clean_denormalized_data,
    flexible_denormalize_with_melt,
    format_sea_freight_df,
)


def sea_freight_db_pipeline(
    run_list: List[str] = ["EU", "NA", "OC", "ME", "FE", "CN", "AF", "SA"]
):
    logger.info("Starting sea freight db pipeline")
    df_list = freight_excel_export_pipeline(run_list)

    # logger.info("Deleting all lines from test db")
    # delete_test_lines()
    # logger.info("Finished deleting all lines from test db")

    for df in df_list:
        formated_df = format_sea_freight_df(df)
        logger.info(f"Found {len(formated_df)} dataframes")
        logger.info(formated_df.head(3))
        denormalized_df = flexible_denormalize_with_melt(formated_df)
        logger.info(f"Found {len(denormalized_df)} dataframes")
    
        cleaned_denormalized_df = clean_denormalized_data(denormalized_df)
        cleaned_denormalized_df.to_csv(
            "./data/cleaned_denormalized_df.csv", index=False
        )
        cleaned_denormalized_local_added_record = ind_export_locals_charges_adder_by_df(
            cleaned_denormalized_df
        )
        logger.info(f"Found {len(cleaned_denormalized_local_added_record)} dataframes")

        logger.info(
            f"Upserting {len(cleaned_denormalized_local_added_record)} lines to test db"
        )
        upsert_test_lines(cleaned_denormalized_local_added_record)
        logger.info(
            f"Finished upserting {len(cleaned_denormalized_local_added_record)} lines to test db"
        )

