from ast import Dict
from typing import List
import pandas as pd
from src.config.logger import logger
from src.utils.convert import string_to_snake_case


def format_destination_charges(df: pd.DataFrame) -> pd.DataFrame:
    """
    Formats the destination charges dataframe.
    """
    logger.info(f"Formatting destination charges dataframe: {df.head(3)}")
    required_columns = ["pol_name", "pod_name", "pol", "pod", "d2", "d4", "currency"]
    df.columns = [
        string_to_snake_case(str(col.strip())) if col else "" for col in df.columns
    ]
    if not all(col in df.columns for col in required_columns):
        logger.error(f"columns: {df.columns}")
        raise ValueError(
            f"Required columns are missing from the dataframe: {required_columns}"
        )
    logger.info(f"length of df: {len(df)}")
    logger.info(f"df: {df.head(3)}")
    df = clean_destination_charges(df)
    logger.info(f"Formatted destination charges dataframe: {df.head(3)}")
    return df


def clean_destination_charges(destination_charges_df, remove_empty_rows=True):
    """
    Clean destination charges data by removing rows only if both d2 and d4 are empty/invalid,
    and setting default values for missing transit_time and validity
    """
    # Make a copy to avoid modifying the original dataframe
    df = destination_charges_df.copy()

    if remove_empty_rows:
        # Only remove rows if essential data is missing
        def should_remove_row(row):
            # Check if d2 and d4 have valid numeric values
            try:
                d2_value = pd.to_numeric(row.get("d2"), errors="coerce")
                d4_value = pd.to_numeric(row.get("d4"), errors="coerce")
                d2_invalid = pd.isna(d2_value)
                d4_invalid = pd.isna(d4_value)
            except:
                d2_invalid = True
                d4_invalid = True

            # Check if pol and pod codes are valid strings (not empty or null)
            pol_code = row.get("pol")
            pod_code = row.get("pod")

            pol_code_invalid = pd.isna(pol_code) or str(pol_code).strip() == ""
            pod_code_invalid = pd.isna(pod_code) or str(pod_code).strip() == ""

            # Remove row if any essential field is invalid
            return (
                d2_invalid
                or d4_invalid
                or pol_code_invalid
                or pod_code_invalid
            )

        # Create mask for rows to keep
        mask = ~df.apply(should_remove_row, axis=1)
        df = df[mask]
    logger.info(f"length of df: {len(df)}")
    logger.info(f"df: {df.head(3)}")

    return df


def format_destination_charges_to_list(df: pd.DataFrame) -> List[Dict]:
    """
    Formats the destination charges dataframe to a list of dictionaries.
    """
    records=[]
    for _, row in df.iterrows():
        records.append(
            {
                "port_code": row["pod"],
                "d2": row["d2"],
                "d4": row["d4"],
                "currency": row["currency"],
            }
        )
    return records