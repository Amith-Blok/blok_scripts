import pandas as pd
from src.config.logger import logger
from src.services.excel_exporter import (
    export_airfreight_import_af_to_india_sheet_to_excel,
    export_airfreight_import_us_to_india_sheet_to_excel,
    export_airfreight_import_canada_to_india_sheet_to_excel,
    export_airfreight_import_eu_to_india_sheet_to_excel,
    export_airfreight_import_fe_to_india_sheet_to_excel,
    export_airfreight_import_me_to_india_sheet_to_excel,
    export_airfreight_import_sa_to_india_sheet_to_excel,
    export_airfreight_export_us_to_india_sheet_to_excel,
    export_airfreight_export_canada_to_india_sheet_to_excel,
    export_airfreight_export_eu_to_india_sheet_to_excel,
    export_airfreight_export_fe_to_india_sheet_to_excel,
    export_airfreight_export_me_to_india_sheet_to_excel,
    export_airfreight_export_sa_to_india_sheet_to_excel,
    export_airfreight_export_af_to_india_sheet_to_excel,
)
from src.utils.convert import string_to_snake_case

AIR_FREIGHT_TRANSIT_AVG_DAYS = {
    "EU": 3,  # Europe: usually 2–4 days
    "NA": 4,  # North America: 3–5 days
    "SA": 5,  # South America: 4–6 days (longer via hubs)
    "OC": 3,  # Australia, New Zealand etc
    "AF": 3,  # Africa: 2–4 days (East Africa faster, West Africa slower)
    "ME": 2,  # Middle East: 1–3 days (many direct flights)
    "FE": 2,  # Far East (East Asia): 1–3 days
    "SE": 2,  # Southeast Asia: 1–3 days
    "IS": 1,  # Indian Subcontinent (Nepal, Bangladesh, Sri Lanka): <2 days
}


def combined_airfreight_import_df():
    """
    Export and combine all airfreight import data into a single DataFrame.

    Returns:
        pd.DataFrame: Combined DataFrame with all airfreight import data

    Raises:
        ValueError: If required columns are missing from any sheet
    """
    # Export individual sheets
    sheet_functions = [
        ("NA", export_airfreight_import_us_to_india_sheet_to_excel),
        ("NA", export_airfreight_import_canada_to_india_sheet_to_excel),
        ("EU", export_airfreight_import_eu_to_india_sheet_to_excel),
        ("FE", export_airfreight_import_fe_to_india_sheet_to_excel),
        ("ME", export_airfreight_import_me_to_india_sheet_to_excel),
        ("SA", export_airfreight_import_sa_to_india_sheet_to_excel),
        ("AF", export_airfreight_import_af_to_india_sheet_to_excel),
    ]

    required_columns = ["origin_code", "destination_code", "rate"]
    processed_dfs = []

    for sheet_name, export_function in sheet_functions:
        try:
            # Get the DataFrame from the export function
            sheet_df = export_function()

            # Convert column names to snake_case and handle multiple spaces
            sheet_df.columns = [
                string_to_snake_case(col.strip()) for col in sheet_df.columns
            ]

            # Check if all required columns exist
            missing_columns = [
                col for col in required_columns if col not in sheet_df.columns
            ]
            if missing_columns:
                raise ValueError(
                    f"Missing required columns in {sheet_name} sheet: {missing_columns}. "
                    f"Available columns: {list(sheet_df.columns)}"
                )

            # Select only required columns
            filtered_df = sheet_df[required_columns].copy()

            # Add source sheet identifier (optional, for tracking)
            filtered_df["source_sheet"] = sheet_name

            processed_dfs.append(filtered_df)

        except Exception as e:
            raise ValueError(f"Error processing {sheet_name} sheet: {str(e)}")

    # Combine all DataFrames
    if not processed_dfs:
        raise ValueError("No valid DataFrames to combine")

    combined_df = pd.concat(processed_dfs, ignore_index=True)

    return combined_df

def combined_airfreight_export_df():
    """
    Export and combine all airfreight export data into a single DataFrame.

    Returns:
        pd.DataFrame: Combined DataFrame with all airfreight export data

    Raises:
        ValueError: If required columns are missing from any sheet
    """
    # Export individual sheets
    sheet_functions = [
        ("NA", export_airfreight_export_us_to_india_sheet_to_excel),
        ("NA", export_airfreight_export_canada_to_india_sheet_to_excel),
        ("EU", export_airfreight_export_eu_to_india_sheet_to_excel),
        ("FE", export_airfreight_export_fe_to_india_sheet_to_excel),
        ("ME", export_airfreight_export_me_to_india_sheet_to_excel),
        ("SA", export_airfreight_export_sa_to_india_sheet_to_excel),
        ("AF", export_airfreight_export_af_to_india_sheet_to_excel),
    ]

    required_columns = ["origin_code", "destination_code", "rate"]
    processed_dfs = []

    for sheet_name, export_function in sheet_functions:
        try:
            # Get the DataFrame from the export function
            sheet_df = export_function()

            # Convert column names to snake_case and handle multiple spaces
            sheet_df.columns = [
                string_to_snake_case(col.strip()) for col in sheet_df.columns
            ]

            # Check if all required columns exist
            missing_columns = [
                col for col in required_columns if col not in sheet_df.columns
            ]
            if missing_columns:
                raise ValueError(
                    f"Missing required columns in {sheet_name} sheet: {missing_columns}. "
                    f"Available columns: {list(sheet_df.columns)}"
                )

            # Select only required columns
            filtered_df = sheet_df[required_columns].copy()

            # Add source sheet identifier (optional, for tracking)
            filtered_df["source_sheet"] = sheet_name

            processed_dfs.append(filtered_df)

        except Exception as e:
            raise ValueError(f"Error processing {sheet_name} sheet: {str(e)}")

    # Combine all DataFrames
    if not processed_dfs:
        raise ValueError("No valid DataFrames to combine")

    combined_df = pd.concat(processed_dfs, ignore_index=True)

    return combined_df


def combined_airfreight_export_and_import_df(is_export: bool = None,is_import: bool = None):
    logger.info("Combining airfreight export and import dataframes")
    export_df = None
    import_df = None
    if is_export:
        export_df = combined_airfreight_export_df()
    if is_import:
        import_df = combined_airfreight_import_df()
    return pd.concat([export_df, import_df], ignore_index=True)



def format_airfreight_df_to_list(df: pd.DataFrame) -> list:
    records = []
    for _, row in df.iterrows():
        records.append(
            {
                "start_code": row["origin_code"],
                "end_code": row["destination_code"],
                "airlines": [
                    {
                        "code": "QA",
                        "name": "Qatar Airways",
                        "value": row["rate"],
                        "currency": "USD",
                        "transit_time": AIR_FREIGHT_TRANSIT_AVG_DAYS[
                            row["source_sheet"]
                        ],
                    },
                    {
                        "code": "EK",
                        "name": "Emirates",
                        "value": row["rate"],
                        "currency": "USD",
                        "transit_time": AIR_FREIGHT_TRANSIT_AVG_DAYS[
                            row["source_sheet"]
                        ],
                    },
                ],
            }
        )
    return records
