import pandas as pd
from src.config.lines import FE_ME_AF_CN_SEAFIEGHT_MAPPER
from src.services.freight.helper import (
    is_missing_header,
    format_columns,
    normalize_df,
    map_ports,
)
from src.config.ports import IN_PORTS_MAPPER, AF_PORTS_MAPPER
from src.utils.convert import remove_diacritics
from src.config.logger import logger


# TODO: MAKE IT REUSABLE
def correct_type_af(df: pd.DataFrame):
    """correct typo and append hapag meta data for EUROPE"""
    # Split 'pol' into lists
    df["pol_list"] = df["pol"].str.strip().str.split("/")

    # Explode to create new rows for each pol
    df_exploded = df.explode("pol_list").reset_index(drop=True)

    # Replace the 'pol' column with exploded pols
    df_exploded["pol"] = df_exploded["pol_list"]

    df_exploded["pod"] = (
        df_exploded["pod"].str.upper().str.replace("PORT OF", "", regex=False)
    )
    df_exploded["pod"] = df_exploded["pod"].apply(remove_diacritics)

    df_exploded["pol"] = df_exploded["pol"].str.upper().str.strip()
    df_exploded["pod"] = df_exploded["pod"].str.upper().str.strip()

    df_exploded["pol"] = df_exploded["pol"].replace(
        {
            "KATTAPULI": "KATTUPALLI",
            "KATAPULI": "KATTUPALLI",
            "KATTAPPULLI": "KATTUPALLI",
            "KATTUPPALLI": "KATTUPALLI",
            "KOLKOTTA": "KOLKATA",
        }
    )

    df_exploded["pod"] = df_exploded["pod"].replace({"ANTWERP-BRUGES": "ANTWERP"})

    df_exploded[["pol_hapag_code", "pol_code"]] = df_exploded["pol"].apply(
        map_ports, args=(IN_PORTS_MAPPER,)
    )

    df_exploded[["pod_hapag_code", "pod_code"]] = df_exploded["pod"].apply(
        map_ports, args=(AF_PORTS_MAPPER,)
    )
    return df_exploded


def format_af(path: str, denormaliz_save_path: str, normalize_save_path: str):
    # GET Last worksheet
    all_sheets = pd.read_excel(path, sheet_name=None, engine="openpyxl")
    print("all_sheets:", len(all_sheets))
    last_sheet_name = list(all_sheets)[-1]
    print("last_sheet_name:", last_sheet_name)
    df = all_sheets[last_sheet_name]

    if df.empty:
        raise ValueError("Worksheet not found or empty for AF blok sea freights")

    #  DENORMALIZE Data
    denormalized_df = format_columns(df)
    denormalized_df = denormalized_df.rename(columns=FE_ME_AF_CN_SEAFIEGHT_MAPPER)
    if is_missing_header(
        df=denormalized_df, expected_header=FE_ME_AF_CN_SEAFIEGHT_MAPPER
    ):
        raise ValueError("Script couldn't format header of AF:")
    denormalized_df = correct_type_af(denormalized_df)
    denormalized_df.to_csv(denormaliz_save_path, index=False)
    logger.info(f"Saved Denormalized to {denormaliz_save_path}")

    #  Normalized Data
    normalized_df = normalize_df(denormalized_df)
    normalized_df.to_csv(normalize_save_path, index=False)
    logger.info(f"Saved Normalized to {normalize_save_path}")
