from typing import List
from gspread import Spreadsheet
import pandas as pd

from src.config.logger import logger


def get_df_from_workbook(
    workbook: Spreadsheet,
    ignore_sheet_title: List[str] = [],
    include_sheet_title: List[str] = None,
):
    df = None
    worksheets = workbook.worksheets()
    ranges = [ws.title for ws in worksheets if ws.title not in ignore_sheet_title and (include_sheet_title is None or ws.title in include_sheet_title)]
    logger.info(f"Ranges after ignoring: {ranges}")

    if not ranges:
        return df

    batch_data = workbook.values_batch_get(ranges)

    # First pass: collect all unique headers to create a unified column structure
    all_headers = set()
    sheet_data_list = []

    for value_range in batch_data.get("valueRanges", []):
        sheet_name = value_range.get("range", "").split("!")[0].strip("'")
        logger.info(f"Processing sheet: {sheet_name}")
        values = value_range.get("values", [])
        if not values:
            continue

        sheet_header = values[0]
        sheet_data = values[1:]

        # Collect all unique headers
        all_headers.update(sheet_header)

        # Store sheet data for second pass
        sheet_data_list.append(
            {"name": sheet_name, "header": sheet_header, "data": sheet_data}
        )

    # Create unified header list
    unified_header = list(all_headers)
    logger.info(f"Unified header with {len(unified_header)} columns: {unified_header}")

    # Second pass: standardize all data rows to match unified header
    for sheet_info in sheet_data_list:
        sheet_header = sheet_info["header"]
        sheet_data = sheet_info["data"]

        # Create a mapping from unified header positions to sheet header positions
        header_mapping = {}
        for i, col in enumerate(unified_header):
            if col in sheet_header:
                header_mapping[i] = sheet_header.index(col)
            else:
                header_mapping[i] = None  # Missing column

        # Standardize each data row to match unified header length
        standardized_data = []
        for row in sheet_data:
            standardized_row = [""] * len(
                unified_header
            )  # Initialize with empty strings
            for unified_idx, sheet_idx in header_mapping.items():
                if sheet_idx is not None and sheet_idx < len(row):
                    standardized_row[unified_idx] = row[sheet_idx]
            standardized_data.append(standardized_row)

        # Create DataFrame for this sheet
        sheet_df = pd.DataFrame(standardized_data, columns=unified_header)

        if df is None:
            df = sheet_df
        else:
            df = pd.concat([df, sheet_df], ignore_index=True)

    return df


COUNTRY_REGION_MAPPER = {
    "IN": {"country": "INDIA", "region": "IS"},
    "US": {"country": "United States", "region": "NA"},
    "CA": {"country": "CANADA", "region": "NA"},
    "BR": {"country": "BRAZIL", "region": "SA"},
    "AR": {"country": "Arengentina", "region": "SA"},
    "CL": {"country": "Chile", "region": "SA"},
    "CO": {"country": "Coloumbo", "region": "SA"},
    "PE": {"country": "Peru", "region": "SA"},
    "ZA": {"country": "South Africa", "region": "AF"},
    "KE": {"country": "South Africa", "region": "AF"},
    "NG": {"country": "South Africa", "region": "AF"},
    "ET": {"country": "South Africa", "region": "AF"},
    "EG": {"country": "South Africa", "region": "AF"},
    "MA": {"country": "South Africa", "region": "AF"},
    "GH": {"country": "South Africa", "region": "AF"},
    "TZ": {"country": "South Africa", "region": "AF"},
    "AE": {"country": "United Arab Emirates", "region": "ME"},
    "QA": {"country": "Qatar", "region": "ME"},
    "OM": {"country": "Oman", "region": "ME"},
    "BH": {"country": "Bharain", "region": "ME"},
    "SA": {"country": "Saudi Arabia", "region": "ME"},
    "KW": {"country": "Kuwait", "region": "ME"},
    "CN": {"country": "China", "region": "FE"},
    "JP": {"country": "Japan", "region": "FE"},
    "KR": {"country": "Korea", "region": "FE"},
    "TW": {"country": "Taiwan", "region": "FE"},
    "HK": {"country": "Hong Kong", "region": "FE"},
    "SG": {"country": "Singapore", "region": "SE"},
    "GB": {"country": "United Kingdom", "region": "EU"},
    "DE": {"country": "Germany", "region": "EU"},
    "NL": {"country": "Netherlands", "region": "EU"},
    "FR": {"country": "France", "region": "EU"},
    "IT": {"country": "Italy", "region": "EU"},
    "ES": {"country": "Spain", "region": "EU"},
}
