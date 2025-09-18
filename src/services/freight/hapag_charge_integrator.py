# This module integrates Hapag sea freight charges with normalized blok freight data.
# It provides functions to merge, process, and validate sea freight and local charge data from different sources.
# The main functions are `hapag_charge_integrator` for new data and `blok_hapag_charge_integrator` for legacy data.
#
# Imports
from collections import defaultdict
from typing import DefaultDict, List, Dict
from src.models.external.hapag import HapagQuotation
from src.models.external.line import NormalizeLine
from src.models.db.lines import Lines
from src.models.db.lines_old import OldLineData
from src.utils.json_util import load_json
from src.utils.csv_util import csv_to_list
from src.services.freight.hapag_utils import (
    generate_old_sea_section,
    generate_sea_section,
    get_local_charges_no_sea,
    get_old_local_charges_no_sea,
)


def hapag_charge_integrator(hapag_path: str, normalize_path: str) -> List[Dict]:
    """
    Integrates Hapag quotations with normalized blok freight data.
    Args:
        hapag_path (str): Path to the Hapag quotations JSON file.
        normalize_path (str): Path to the normalized blok CSV file.
    Returns:
        List[Dict]: List of dictionaries representing integrated line records.
    """
    # Load Hapag quotations from JSON and parse into HapagQuotation objects
    hapag_quotes_dict = load_json(path=hapag_path)
    hapag_record: List[HapagQuotation] = [
        HapagQuotation(**hapag_quote) for hapag_quote in hapag_quotes_dict
    ]
    # Create a lookup for Hapag quotations by start:end code
    hapag_lookup: Dict[str, HapagQuotation] = {
        f"{hapag.start_code}:{hapag.end_code}": hapag for hapag in hapag_record
    }
    # Load normalized blok data from CSV and parse into NormalizeLine objects
    normalize_blok = csv_to_list(path=normalize_path)
    normalized_blok_list: List[NormalizeLine] = [
        NormalizeLine(**line) for line in normalize_blok
    ]
    # Group normalized blok lines by pol_code:pod_code
    normalized_blok_lookup: DefaultDict[str, List[NormalizeLine]] = defaultdict(list)
    for blok in normalized_blok_list:
        normalized_blok_lookup[f"{blok.pol_code}:{blok.pod_code}"].append(blok)

    final_lines_records: List[Dict] = []
    # Iterate over each group of blok lines
    for key, bloks in normalized_blok_lookup.items():
        hapag_data = hapag_lookup.get(key)
        if not hapag_data:
            continue  # Skip if no matching Hapag data
        # Get local charges for this Hapag record (excluding sea charges)
        hapag_local_charges = get_local_charges_no_sea(hapag_data.sections)

        # Prepare the output dictionary for this route
        lines_dict = {
            "start_code": hapag_data.start_code,
            "start_name": hapag_data.start_name,
            "end_code": hapag_data.end_code,
            "end_name": hapag_data.end_name,
            "available_lines": [],
            "lines": [],
        }
        # For each blok line, generate the line data and sections
        for line in bloks:
            line_data = {}
            # Generate the sea section for this blok line and append local charges
            line_sections = [
                generate_sea_section(d2=line.d2 or 0, d4=line.d4 or 0)
            ] + hapag_local_charges

            line_data["line_name"] = line.line_name
            line_data["estimated_days"] = line.transit_time or 0
            line_data["valid_to"] = line.validity or ""
            line_data["routing"] = [route.model_dump() for route in hapag_data.routing]
            line_data["sections"] = [section.model_dump() for section in line_sections]
            lines_dict["available_lines"].append(line.line_name)
            lines_dict["lines"].append(line_data)

        # If 'hapag' line is not present, add it from the Hapag data
        if "hapag" not in lines_dict["available_lines"]:
            lines_dict["lines"].append(
                {
                    "line_name": "hapag",
                    "estimated_days": hapag_data.estimatedTransportDays,
                    "valid_to": hapag_data.validTo,
                    "routing": [route.model_dump() for route in hapag_data.routing],
                    "sections": [
                        section.model_dump() for section in hapag_data.sections
                    ],
                }
            )
            lines_dict["available_lines"].append("hapag")
        # Validate the output using the Lines model
        Lines.model_validate(lines_dict)
        final_lines_records.append(lines_dict)

    return final_lines_records


# NOTE: Temp solution for hapag_charge_integrator until i write new hapag scrape script
# This function is for legacy/old Hapag data format integration.
def blok_hapag_charge_integrator(
    blok_hapag_path: str, normalize_path: str
) -> List[Dict]:
    """
    Integrates legacy Hapag blok quotations with normalized blok freight data.
    Args:
        blok_hapag_path (str): Path to the legacy Hapag blok quotations JSON file.
        normalize_path (str): Path to the normalized blok CSV file.
    Returns:
        List[Dict]: List of dictionaries representing integrated line records (legacy format).
    """
    # Load legacy Hapag blok quotations and parse into OldLineData objects
    hapag_quotes_list = load_json(path=blok_hapag_path)
    hapag_record = [OldLineData(**hapag) for hapag in hapag_quotes_list]

    # Create a lookup for legacy Hapag quotations by start:end code
    hapag_lookup: Dict[str, OldLineData] = {
        f"{hapag.start_code}:{hapag.end_code}": hapag for hapag in hapag_record
    }
    # Load normalized blok data from CSV and parse into NormalizeLine objects
    normalize_blok = csv_to_list(path=normalize_path)
    normalized_blok_list: List[NormalizeLine] = [
        NormalizeLine(**line) for line in normalize_blok
    ]
    # Group normalized blok lines by pol_code:pod_code
    normalized_blok_lookup: DefaultDict[str, List[NormalizeLine]] = defaultdict(list)
    for blok in normalized_blok_list:
        normalized_blok_lookup[f"{blok.pol_code}:{blok.pod_code}"].append(blok)

    final_lines_records: List[Dict] = []
    # Iterate over each group of blok lines
    for key, bloks in normalized_blok_lookup.items():
        hapag_data = hapag_lookup.get(key)
        if not hapag_data:
            continue  # Skip if no matching Hapag data
        # Get local charges for this legacy Hapag record (excluding sea charges)
        hapag_local_charges = get_old_local_charges_no_sea(hapag_data.charges)

        # Prepare the output dictionary for this route
        lines_dict = {
            "start_code": hapag_data.start_code,
            "start_name": hapag_data.start_name,
            "end_code": hapag_data.end_code,
            "end_name": hapag_data.end_name,
            "available_lines": [],
            "lines": [],
        }
        # For each blok line, generate the line data and sections
        for line in bloks:
            line_data = {}
            # Generate the sea section for this blok line and append local charges
            line_sections = [
                generate_old_sea_section(d2=line.d2 or 0, d4=line.d4 or 0)
            ] + hapag_local_charges
            line_data["line_name"] = line.line_name
            line_data["estimated_days"] = line.transit_time or 0
            line_data["valid_to"] = line.validity or ""
            line_data["routing"] = [route.model_dump() for route in hapag_data.routing]
            line_data["sections"] = [section.model_dump() for section in line_sections]
            lines_dict["available_lines"].append(line.line_name)
            lines_dict["lines"].append(line_data)

        # If 'hapag' line is not present, add it from the legacy Hapag data
        if "hapag" not in lines_dict["available_lines"]:
            hapag_line = {
                "line_name": "hapag",
                "estimated_days": hapag_data.estimated_days,
                "valid_to": hapag_data.valid_to,
                "routing": [route.model_dump() for route in hapag_data.routing],
                "sections": [section.model_dump() for section in hapag_data.charges],
            }
            lines_dict["lines"].append(hapag_line)
            lines_dict["available_lines"].append("hapag")
        # Convert lines_dict into Line model format (legacy)
        lines_dict = Lines(**lines_dict).model_dump()
        final_lines_records.append(lines_dict)

    return final_lines_records
