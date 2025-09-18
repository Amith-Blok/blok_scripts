import pandas as pd
from datetime import datetime
from dateutil import parser
from typing import List, Any, Dict
from src.models.external.line import DenormalizeLine
from src.config.lines import ALL_LINES


def format_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Lowercase headers
    df.columns = [str(col).strip().lower() if col else "" for col in df.columns]
    print("df.columns:", df.columns.tolist())
    # Drop the second row (subheading)
    df = df.iloc[1:].reset_index(drop=True)
    df = df.dropna(subset=["pod"])
    # Remove rows where 'pod' is empty or whitespace
    df = df.loc[df["pod"].astype(str).str.strip() != ""]

    for col in df.columns:
        # print("pol or pod", col)
        if col in ["pol", "pod"]:
            # Convert to string
            df[col] = df[col].astype(str).str.upper().str.strip()
        elif col.startswith("validity"):
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

        elif col.startswith("transit time"):
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

        elif col.split(".")[0] in ALL_LINES:
            # print("Print lines:", col)
            # Convert to float and handle missing/invalid values
            df[col] = df[col].astype(str).str.replace(r"[\$,]", "", regex=True)
            df[col] = pd.to_numeric(df[col], errors="coerce").round(2)

    return df


def map_ports(pol_val, mapper):
    pol_val = pol_val.strip().upper()
    for port_name, mapping in mapper.items():
        if port_name.startswith(pol_val) or pol_val in port_name:
            return pd.Series(
                {"h_code": mapping["h_code"], "port_code": mapping["port_code"]}
            )
    return pd.Series({"h_code": None, "port_code": None})


def is_missing_header(df: pd.DataFrame, expected_header: Dict[str, str]) -> bool:
    print("Raw columns from file:", df.columns.tolist())
    desired_columns = list(expected_header.values())
    print("desired_columns size", len(desired_columns))
    missing_columns = [col for col in desired_columns if col not in df.columns]
    print("missing column size", len(missing_columns))
    print(missing_columns)

    if missing_columns:
        print(f"desired_columns:{desired_columns}\nmissing_columns:{missing_columns}")
        return True
    return False


def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    normalized_data: List[DenormalizeLine] = []
    default_validity_date = datetime.now().strftime("%Y-%m-%d")

    for _, row in df.iterrows():
        pol_code = str(row.get("pol_code", ""))
        pod_code = str(row.get("pod_code", ""))

        for line in ALL_LINES:
            d2_val: Any = row.get(f"{line}_d2")
            d4_val: Any = row.get(f"{line}_d4")
            transit_time_val: Any = row.get(f"{line}_transit_time")
            validity_val: Any = row.get(f"{line}_validity")

            # 1. Critical field check for d2_val
            #    pd.isna() is robust for None, np.nan, pd.NA
            if d2_val is None or pd.isna(d2_val) or str(d2_val).strip() == "":
                continue

            current_d2: float
            try:
                current_d2 = float(str(d2_val))  # Ensure string conversion for float
            except ValueError:
                # Handle cases where d2_val might be something non-convertible
                # even if not strictly NA (e.g. malformed string)
                # Depending on requirements, you might log this or skip
                continue  # Or raise an error, or assign a default float

            # 2. transit_time
            current_transit_time: int = 0
            if transit_time_val is not None and not pd.isna(transit_time_val):
                tt_str = str(transit_time_val).strip()
                if tt_str:  # Check if not empty after stripping
                    try:
                        current_transit_time = int(
                            float(tt_str)
                        )  # float() handles "123.0" then int()
                    except ValueError:
                        current_transit_time = 0  # Or log error

            # 3. validity
            current_validity: str = default_validity_date
            if validity_val is not None and not pd.isna(validity_val):
                v_str = str(validity_val).strip()
                if v_str:
                    current_validity = v_str

            # 4. d4
            current_d4: float = float(0)
            if d4_val is not None and not pd.isna(d4_val):
                d4_str = str(d4_val).strip()
                if d4_str:
                    try:
                        current_d4 = float(d4_str)
                    except ValueError:
                        current_d4 = float(0)  # Or log error

            entry = DenormalizeLine(
                pol_code=pol_code,
                pod_code=pod_code,
                line_name=str(line),
                transit_time=current_transit_time,
                validity=current_validity,
                d2=current_d2,
                d4=current_d4,
            )
            normalized_data.append(entry)

    if not normalized_data:
        return pd.DataFrame([])

    return pd.DataFrame([data_row.model_dump() for data_row in normalized_data])
