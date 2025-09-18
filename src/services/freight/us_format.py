import pandas as pd
from src.config.lines import US_SEAFRIEGHT_MAPPER
from src.services.freight.helper import (
    is_missing_header,
    format_columns,
    normalize_df,
    map_ports,
)
from src.config.ports import IN_PORTS_MAPPER, US_PORTS_MAPPER
from src.config.logger import logger


# TODO: MAKE IT REUSABLE
def correct_typo_us(df: pd.DataFrame):
    """correct typo and append hapag meta data for USA"""
    # Split 'pol' into lists
    df["pol_list"] = df["pol"].str.strip().str.split("/")

    # Explode to create new rows for each pol
    df_exploded = df.explode("pol_list").reset_index(drop=True)

    # Replace the 'pol' column with exploded pols
    df_exploded["pol"] = df_exploded["pol_list"]

    # Drop the helper column
    df_exploded = df_exploded.drop(columns=["pol_list"])

    # Split 'pod' into lists
    df_exploded["pod_list"] = df_exploded["pod"].str.strip().str.split("/")

    # Explode to create new rows for each pod
    df_exploded = df_exploded.explode("pod_list").reset_index(drop=True)

    # Replace the 'pod' column with exploded pods
    df_exploded["pod"] = df_exploded["pod_list"]

    # Drop the helper column
    df_exploded = df_exploded.drop(columns=["pod_list"])

    df_exploded["pod"] = df_exploded["pod"].str.strip()
    df_exploded["pol"] = df_exploded["pol"].str.strip()

    df_exploded["pol"] = df_exploded["pol"].str.upper()
    df_exploded["pod"] = df_exploded["pod"].str.upper()
    df_exploded["pol"] = df_exploded["pol"].replace(
        {
            "KATTAPULI": "KATTUPALLI",
            "KATAPULI": "KATTUPALLI",
            "KATTAPPULLI": "KATTUPALLI",
            "KATTUPPALLI": "KATTUPALLI",
            "KOLKOTTA": "KOLKATA",
        }
    )
    df_exploded["pod"] = df_exploded["pod"].replace(
        {
            "LB": "LONG BEACH, CA",
            "MONTERAL": "MONTREAL, QC",
            "VANCOVER": "VANCOUVER, BC",
        }
    )
    df_exploded["pod"] = df_exploded["pod"].replace({"LA": "LOS ANGELES, CA"})
    df_exploded[["pol_hapag_code", "pol_code"]] = df_exploded["pol"].apply(
        map_ports, args=(IN_PORTS_MAPPER,)
    )

    df_exploded[["pod_hapag_code", "pod_code"]] = df_exploded["pod"].apply(
        map_ports, args=(US_PORTS_MAPPER,)
    )
    return df_exploded


def format_us(
    path: str,
    denormaliz_save_path: str,
    normalize_save_path: str,
):
    # GET Last worksheet
    all_sheets = pd.read_excel(path, sheet_name=None)
    print("all_sheets:", len(all_sheets))
    last_sheet_name = list(all_sheets)[-1]
    print("last_sheet_name:", last_sheet_name)
    df = all_sheets[last_sheet_name]
    pd.set_option("display.max_columns", None)
    print("df:", df)

    if df.empty:
        raise ValueError("Worksheet not found or empty for US Blok sea freights")

    # NOTE: DENORMALIZE Data

    # format cell data
    denormalized_df = format_columns(df)
    # rename the columns header
    denormalized_df = denormalized_df.rename(columns=US_SEAFRIEGHT_MAPPER)
    # print("denormalized_df:", denormalized_df)
    # check header is correct or not
    if is_missing_header(df=denormalized_df, expected_header=US_SEAFRIEGHT_MAPPER):
        raise ValueError("Script couldn't format header of USA:")
    # check common typo and append hapag meta data
    denormalized_df = correct_typo_us(denormalized_df)
    print("denormalized_df:", denormalized_df.head())
    denormalized_df.to_csv(denormaliz_save_path, index=False)
    logger.info(f"Saved Denormalized csv to {denormaliz_save_path}")

    # NOTE: Normalized Data
    normalized_df = normalize_df(denormalized_df)
    print("normalized_df:", normalized_df.head())
    # print("normalized_df:", normalized_df)
    normalized_df.to_csv(normalize_save_path, index=False)
    logger.info(f"Saved Normalized to {denormaliz_save_path}")
