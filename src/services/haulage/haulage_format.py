import pandas as pd


FILE_PATH = "Outbound Haulage_eff Sept 25_0.xlsx"


HAULAGE_HEADER_MAPPER = {
    "por code": "start_code",
    "por name": "start_name",
    "pol code": "end_code",
    "pol name": "end_name",
    "cargo type": "cargo_type",
    "cur.": "currency",
    "amount ( inr)": "rate",
    "effective date": "effective_date",
    "cargo weight min (mt)": "min",
    "cargo weight max (mt)": "max",
    "mode of transport": "transportation_mode",
}


# ------------------------------------------------------------
# Helper: Normalize column names
# ------------------------------------------------------------
def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace("\n", " ", regex=False)
        .str.replace("  ", " ", regex=False)
    )
    return df


# ------------------------------------------------------------
# Helper: Detect actual header row dynamically
# ------------------------------------------------------------
def detect_header_row(raw_df: pd.DataFrame) -> int | None:
    temp = raw_df.astype(str).apply(lambda x: x.str.lower())

    for idx, row in temp.iterrows():
        if row.str.contains("por code", na=False).any():
            return idx

    return None


# ------------------------------------------------------------
# Main Processing Function
# ------------------------------------------------------------
def format_haulage(path: str) -> pd.DataFrame:
    excel = pd.ExcelFile(path)
    all_sheets_data = []

    for sheet_name in excel.sheet_names:
        print(f"Processing sheet: {sheet_name}")

        # Read raw sheet without header
        raw_df = pd.read_excel(excel, sheet_name=sheet_name, header=None)

        header_row = detect_header_row(raw_df)

        if header_row is None:
            print(f"Skipping {sheet_name} (no table found)")
            continue

        # Re-read with correct header
        df = pd.read_excel(excel, sheet_name=sheet_name, header=header_row)

        # Normalize column names
        df = normalize_columns(df)

        # --------------------------------------------------------
        # Handle duplicate PER columns
        # pandas auto-renames duplicates as: per, per.1
        # --------------------------------------------------------
        if "per" in df.columns and "per.1" in df.columns:
            df = df.rename(columns={
                "per": "container_type",
                "per.1": "container_name"
            })

        # --------------------------------------------------------
        # Remove fully empty rows
        # --------------------------------------------------------
        df = df.dropna(how="all")

        # Remove footer rows where start_code is missing
        if "por code" in df.columns:
            df = df[df["por code"].notna()]

        # --------------------------------------------------------
        # Rename standard columns
        # --------------------------------------------------------
        df = df.rename(columns=HAULAGE_HEADER_MAPPER)

        # Keep only relevant columns (if they exist)
        final_columns = [
            "start_code",
            "start_name",
            "end_code",
            "end_name",
            "container_type",
            "container_name",
            "cargo_type",
            "currency",
            "rate",
            "effective_date",
            "min",
            "max",
            "transportation_mode",
        ]

        df = df[[col for col in final_columns if col in df.columns]]

        # Add sheet source (optional but useful)
        df["source_sheet"] = sheet_name

        all_sheets_data.append(df)

    # ------------------------------------------------------------
    # Merge all sheets
    # ------------------------------------------------------------
    if not all_sheets_data:
        return pd.DataFrame()

    final_df = pd.concat(all_sheets_data, ignore_index=True)

    # ------------------------------------------------------------
    # Data Cleaning & Type Conversion
    # ------------------------------------------------------------
    if "rate" in final_df.columns:
        final_df["rate"] = pd.to_numeric(final_df["rate"], errors="coerce")

    if "min" in final_df.columns:
        final_df["min"] = pd.to_numeric(
            final_df["min"], errors="coerce"
        )

    if "max" in final_df.columns:
        final_df["max"] = pd.to_numeric(
            final_df["max"], errors="coerce"
        )
    # ------------------------------------------------------------
    # Remove incomplete rows
    # ------------------------------------------------------------
    required_columns = [
        "start_code",
        "end_code",
        "min",
        "max",
        "rate",
    ]

    final_df = final_df.replace(r'^\s*$', pd.NA, regex=True)
    final_df = final_df.dropna(subset=required_columns)

    # ------------------------------------------------------------
    # Convert columns to uppercase
    # ------------------------------------------------------------
    columns_to_uppercase = [
        "start_code",
        "start_name",
        "end_code",
        "end_name",
        "container_type",
        "container_name",
        "cargo_type",
        "currency",
        "transportation_mode",
    ]

    for col in columns_to_uppercase:
        if col in final_df.columns:
            final_df[col] = (
                final_df[col]
                .astype(str)
                .str.strip()
                .str.upper()
            )


    # ------------------------------------------------------------
    # Replace & with / in container_type
    # ------------------------------------------------------------
    final_df["container_type"] = (
        final_df["container_type"]
        .str.upper()
        .str.strip()
        .str.replace(r"\s*&\s*", "/", regex=True)
    )
    return final_df

