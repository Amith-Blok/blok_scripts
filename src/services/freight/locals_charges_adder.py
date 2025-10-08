import pandas as pd
from collections import defaultdict
from typing import DefaultDict, List, Dict
from src.models.db.lines import Lines
from src.models.external.line import DenormalizeLine
from src.models.db.lines_old import OldSection, OldSectionData
from src.services.freight.hapag_utils import generate_old_sea_section
from src.utils.csv_util import csv_to_list
from src.config.ind_local_charges import INDIA_EXPORT_LOCAL_CHARGES
from src.database.distination_charges import get_test_destination_charges_by_port_code
from src.config.logger import logger


def get_india_export_local_charges(terminal_charges: dict) -> OldSection:
    local_charges_list: OldSection = OldSection(
        name="EXPORT_SURCHARGES",
        label="Export Surcharge",
        data=[],
    )
    local_charges_list.data.append(
        OldSectionData(
            name="Terminal Handling Charges Org",
            code="THO",
            currency="INR",
            isConsideredForTotal=True,
            additionalNotes="",
            container1=terminal_charges["20STD"],
            container2=terminal_charges["40STD"],
            container3=terminal_charges["45HC"],
        )
    )
    for value in INDIA_EXPORT_LOCAL_CHARGES:
        local_charges_list.data.append(
            OldSectionData(
                name=value["label"],
                code=value["code"],
                currency=value["currency"],
                isConsideredForTotal=True,
                additionalNotes="",
                container1=value["container1"],
                container2=value["container2"],
                container3=value["container3"],
            )
        )
    return local_charges_list

def generate_destination_charges(end_code:str) -> OldSection or None:
    if end_code.startswith('US') or end_code.startswith('CA'):
        logger.info(f"Skipping Destination Charges for {end_code}. It is a US or CA port")
        return None
    local_charges_list: OldSection = OldSection(
        name="DESTINATION_CHARGES",
        label="Destination Charges",
        data=[],
    )
    destination_charges = get_test_destination_charges_by_port_code(end_code)
    if not destination_charges:
        return None
    local_charges_list.data.append(
        OldSectionData(
            name="Destination Charges",
            code="DST",
            currency=destination_charges.currency,
            isConsideredForTotal=True,
            additionalNotes="",
            container1=destination_charges.d2,
            container2=destination_charges.d4,
            container3=destination_charges.d4,
        )
    )
    return local_charges_list
def ind_export_locals_charges_adder_by_df(denormalized_df: pd.DataFrame) -> List[Dict]:
    """
    Adds export locals charges to the lines.
    """
    india_terminal_charges_list = csv_to_list(
        path="./data/ind-terminal-handling-charges.csv"
    )
    india_terminal_charges_lookup: DefaultDict[str, Dict] = defaultdict(dict)
    for charge in india_terminal_charges_list:
        india_terminal_charges_lookup[charge["port_name"].strip().upper()] = charge
    # print(india_terminal_charges_lookup)

    denormalized_blok = denormalized_df.to_dict(orient="records")
    logger.info(f"denormalize blok: {denormalized_blok[0]}")
    logger.info(f"denormalize blok: {len(denormalized_blok)}")
    denormalized_blok_list: List[DenormalizeLine] = [
        DenormalizeLine(**line) for line in denormalized_blok
    ]
    logger.info(f"Denormalized blok list: {denormalized_blok_list[0]}")
    logger.info(f"Denormalized blok list: {len(denormalized_blok_list)}")

    # Group denormalized blok lines by pol_code:pod_code
    normalized_blok_lookup: DefaultDict[str, List[DenormalizeLine]] = defaultdict(list)
    for blok in denormalized_blok_list:
        normalized_blok_lookup[f"{blok.pol_code}:{blok.pod_code}"].append(blok)

    final_lines_records: List[Dict] = []
    for key, bloks in normalized_blok_lookup.items():
        logger.info(f"key: {key}")
        # get local charges for this route
        terminal_charges = india_terminal_charges_lookup.get(
            bloks[0].pol_code.strip().upper()
        )
        if not terminal_charges:
            logger.info(f"Terminal charges not found for {bloks[0].pol_code}")
            continue
        local_charges = get_india_export_local_charges(terminal_charges)
        # Prepare the output dictionary for this route
        lines_dict = {
            "start_code": bloks[0].pol_code,
            "start_name": bloks[0].pol_name,
            "end_code": bloks[0].pod_code,
            "end_name": bloks[0].pod_name,
            "available_lines": [],
            "lines": [],
        }
        destination_charges = generate_destination_charges(bloks[0].pod_code)
        for line in bloks:
            line_data = {}
            # generate the sea section for this blok line and append local charges
            line_sections = [
                generate_old_sea_section(d2=line.d2 or 0, d4=line.d4 or 0)
            ] + [local_charges]
            if destination_charges and destination_charges.data[0].code=='DST':
                logger.info(f"Adding Destination Charges for {bloks[0].pod_code}")
                line_sections.append(destination_charges)
            line_data["line_name"] = line.line_name
            line_data["estimated_days"] = line.transit_time or 0
            line_data["valid_to"] = line.validity or ""
            line_data["routing"] = []
            line_data["sections"] = [section.model_dump() for section in line_sections]
            lines_dict["available_lines"].append(line.line_name)
            lines_dict["lines"].append(line_data)
        Lines.model_validate(lines_dict)
        final_lines_records.append(lines_dict)

    return final_lines_records
