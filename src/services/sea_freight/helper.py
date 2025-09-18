from datetime import datetime, timedelta
from dateutil import parser
import pandas as pd
import re

from src.config.lines import ALL_LINES
from src.utils.convert import string_to_snake_case
from src.database.seaports import get_blok_seaports_by_port_code


def format_sea_freight_df(df: pd.DataFrame) -> pd.DataFrame:
    # Lowercase headers
    df.columns = [string_to_snake_case(str(col.strip())) if col else "" for col in df.columns]
    print("df.columns:", df.columns.tolist())
    # Drop the second row (subheading)
    df = df.iloc[1:].reset_index(drop=True)
    df = df.dropna(subset=["pod"])
    # Remove rows where 'pod' is empty or whitespace
    df = df.loc[df["pod"].astype(str).str.strip() != ""]
    valid_validity_columns = [f"{line}_validity" for line in ALL_LINES]
    valid_transit_time_columns = [f"{line}_transit_time" for line in ALL_LINES]
    valid_d2_columns = [f"{line}_d2" for line in ALL_LINES]
    valid_d4_columns = [f"{line}_d4" for line in ALL_LINES]
    for col in df.columns:
        # print("pol or pod", col)
        if col in ["pol_name", "pod_name", "pol", "pod"]:
            # Convert to string
            df[col] = df[col].astype(str).str.upper().str.strip()
        elif col in valid_validity_columns:
            # print("validity", col)
            def format_date(val):
                try:
                    if isinstance(val, datetime):
                        return val.strftime("%Y-%m-%d")
                    else:
                        cell_date = parser.parse(str(val))
                        return cell_date.strftime("%Y-%m-%d")
                except Exception as e:
                    # print(f"Failed to parse date in column '{col}': {val} error:{e}")
                    return None

            df[col] = df[col].apply(format_date)

        elif col in valid_transit_time_columns:
            # print("transit", col)

            def clean_transit(val):
                try:
                    # Convert to integer
                    intval = int(val)
                    return intval if intval != 0 else pd.NA
                except:
                    # For non-integers or errors, return blank
                    return pd.NA

            df[col] = df[col].apply(clean_transit).astype("Int64")

        elif col in valid_d2_columns or col in valid_d4_columns:
            # print("Print lines:", col)
            # Convert to float and handle missing/invalid values
            df[col] = df[col].astype(str).str.replace(r"[\$,]", "", regex=True)
            df[col] = pd.to_numeric(df[col], errors="coerce").round(2)

    return df


def detect_carriers(df):
    """
    Dynamically detect which carriers are present in the dataframe
    based on column naming patterns
    """
    carriers = set()

    # Pattern to match carrier columns (carrier_validity, carrier_transit_time, carrier_d2, carrier_d4)
    pattern = r"^([a-zA-Z_]+)_(validity|transit_time|d2|d4)$"

    for col in df.columns:
        match = re.match(pattern, col)
        if match:
            carrier = match.group(1)
            carriers.add(carrier.lower())

    return sorted(list(carriers))


def flexible_denormalize_with_melt(df):
    """
    More efficient melt-based approach that automatically detects carriers
    """

    # Detect carriers
    carriers = detect_carriers(df)
    print(f"Detected carriers: {carriers}")

    if not all(carrier in ALL_LINES for carrier in carriers):
        raise ValueError(f"Carriers detected are not in the ALL_LINES list: {carriers}")

    # Base columns for identification
    pol_col = "pol" if "pol" in df.columns else "pol_code"
    pod_col = "pod" if "pod" in df.columns else "pod_code"
    base_cols = [pol_col, pod_col]

    # Port code:port_name lookup cache
    port_name_lookup = {}

    def get_port_name(port_code):
        """Get port name from database with caching"""
        if not port_code or pd.isna(port_code):
            return None

        # Convert to string and strip whitespace
        port_code = str(port_code).strip()

        if port_code in port_name_lookup:
            return port_name_lookup[port_code]

        try:
            port_data = get_blok_seaports_by_port_code(port_code)
            port_name = port_data.port_name if port_data else None
            port_name_lookup[port_code] = port_name
            return port_name
        except Exception as e:
            print(f"Error fetching port name for {port_code}: {e}")
            port_name_lookup[port_code] = None
            return None

    result_dfs = []

    # Process each detected carrier
    for carrier in carriers:
        # Find all columns for this carrier
        carrier_cols = [col for col in df.columns if col.startswith(f"{carrier}_")]

        if carrier_cols:
            # Create carrier-specific dataframe
            carrier_df = df[base_cols + carrier_cols].copy()

            # Rename columns to standard format
            column_mapping = {}
            for col in carrier_cols:
                if col.endswith("_validity"):
                    column_mapping[col] = "validity"
                elif col.endswith("_transit_time"):
                    column_mapping[col] = "transit_time"
                elif col.endswith("_d2"):
                    column_mapping[col] = "d2"
                elif col.endswith("_d4"):
                    column_mapping[col] = "d4"

            carrier_df = carrier_df.rename(columns=column_mapping)
            carrier_df["line_name"] = carrier.lower()

            # Ensure all expected columns exist (fill missing with None)
            expected_cols = [
                "pol_code",
                "pol_name",
                "pod_code",
                "pod_name",
                "line_name",
                "transit_time",
                "validity",
                "d2",
                "d4",
            ]

            # Rename pol/pod columns to standard names
            if pol_col in carrier_df.columns:
                carrier_df = carrier_df.rename(columns={pol_col: "pol_code"})
            if pod_col in carrier_df.columns:
                carrier_df = carrier_df.rename(columns={pod_col: "pod_code"})

            # Add missing columns as None
            for col in expected_cols:
                if col not in carrier_df.columns:
                    carrier_df[col] = None

            # Populate port names using the lookup function
            if "pol_code" in carrier_df.columns:
                carrier_df["pol_name"] = carrier_df["pol_code"].apply(get_port_name)
            if "pod_code" in carrier_df.columns:
                print("pod_code in carrier_df.columns")
                carrier_df["pod_name"] = carrier_df["pod_code"].apply(get_port_name)

            # Split port codes if they contain '/' separator
            expanded_rows = []
            for _, row in carrier_df.iterrows():
                pol_codes = (
                    str(row["pol_code"]).split("/")
                    if pd.notna(row["pol_code"])
                    else [row["pol_code"]]
                )
                pod_codes = (
                    str(row["pod_code"]).split("/")
                    if pd.notna(row["pod_code"])
                    else [row["pod_code"]]
                )

                # Create combinations of all pol_codes with all pod_codes
                for pol_code in pol_codes:
                    for pod_code in pod_codes:
                        new_row = row.copy()
                        new_row["pol_code"] = (
                            pol_code.strip() if pol_code.strip() != "nan" else None
                        )
                        new_row["pod_code"] = (
                            pod_code.strip() if pod_code.strip() != "nan" else None
                        )

                        # Update port names for the split codes
                        new_row["pol_name"] = (
                            get_port_name(new_row["pol_code"])
                            if new_row["pol_code"]
                            else None
                        )
                        new_row["pod_name"] = (
                            get_port_name(new_row["pod_code"])
                            if new_row["pod_code"]
                            else None
                        )

                        expanded_rows.append(new_row)

            # Convert expanded rows back to DataFrame
            if expanded_rows:
                carrier_df = pd.DataFrame(expanded_rows)
                # Select only expected columns in correct order
                carrier_df = carrier_df[expected_cols]

            result_dfs.append(carrier_df)

    if not result_dfs:
        return pd.DataFrame(
            columns=[
                "pol_code",
                "pol_name",
                "pod_code",
                "pod_name",
                "line_name",
                "transit_time",
                "validity",
                "d2",
                "d4",
            ]
        )

    # Combine all carriers
    final_df = pd.concat(result_dfs, ignore_index=True)

    # Remove rows where all important data is null
    final_df = final_df.dropna(
        subset=["transit_time", "validity", "d2", "d4"], how="all"
    )

    return final_df


def clean_denormalized_data(denormalized_df, remove_empty_rows=True):
    """
    Clean denormalized data by removing rows only if both d2 and d4 are empty/invalid,
    and setting default values for missing transit_time and validity
    """
    # Make a copy to avoid modifying the original dataframe
    df = denormalized_df.copy()

    if remove_empty_rows:
        # Only remove rows if both d2 and d4 are empty or not numeric
        def should_remove_row(row):
            d2_invalid = pd.isna(row.get("d2")) or not pd.api.types.is_numeric_dtype(
                type(row.get("d2"))
            )
            d4_invalid = pd.isna(row.get("d4")) or not pd.api.types.is_numeric_dtype(
                type(row.get("d4"))
            )
            pol_code_invalid = pd.isna(
                row.get("pol_code")
            ) or not pd.api.types.is_string_dtype(type(row.get("pol_code")))
            pod_code_invalid = pd.isna(
                row.get("pod_code")
            ) or not pd.api.types.is_string_dtype(type(row.get("pod_code")))
            pol_name_invalid = pd.isna(
                row.get("pol_name")
            ) or not pd.api.types.is_string_dtype(type(row.get("pol_name")))
            pod_name_invalid = pd.isna(
                row.get("pod_name")
            ) or not pd.api.types.is_string_dtype(type(row.get("pod_name")))
            return (
                d2_invalid
                or d4_invalid
                or pol_code_invalid
                or pod_code_invalid
                or pol_name_invalid
                or pod_name_invalid
            )

        # Create mask for rows to keep
        mask = ~df.apply(should_remove_row, axis=1)
        df = df[mask]

    # Set default values for missing transit_time and validity
    if "transit_time" in df.columns:
        # Set default transit time to 40 days for missing values
        df["transit_time"] = df["transit_time"].fillna(40)

    if "validity" in df.columns:
        # Set default validity to 15 days from now for missing values
        default_validity = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
        df["validity"] = df["validity"].fillna(default_validity)

    return df
