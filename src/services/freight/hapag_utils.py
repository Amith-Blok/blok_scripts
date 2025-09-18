from typing import List
from src.models.external.hapag import Section, SectionData
from src.models.external.line import DenormalizeLine
from src.config.logger import logger
from src.database.line_rates import get_blok_line_by_codes
from src.models.db.lines_old import OldSection, OldSectionData
from src.utils.json_util import write_data_json
from src.utils.csv_util import csv_to_list


def get_local_charges_no_sea(sections: List[Section]) -> List[Section]:
    return [
        section_data
        for section_data in sections
        if not section_data.name == "SEA_FREIGHT"
    ]


def get_old_local_charges_no_sea(charges: List[OldSection]) -> List[OldSection]:
    return [charge for charge in charges if not charge.name == "SEA_FREIGHT"]


def generate_sea_section(d2: float, d4: float) -> OldSection:
    return Section(
        name="SEA_FREIGHT",
        label="Freight Charges",
        data=[
            OldSection(
                name="Ocean Freight",
                code="SEA",
                currency="USD",
                isConsideredForTotal=True,
                additionalNotes="",
                container1=d2,
                container2=d4,
                container3=d4,
            )
        ],
    )


def generate_old_sea_section(d2: float, d4: float) -> OldSection:
    return OldSection(
        name="SEA_FREIGHT",
        label="Freight Charges",
        data=[
            OldSectionData(
                name="Ocean Freight",
                code="SEA",
                currency="USD",
                isConsideredForTotal=True,
                additionalNotes="",
                container1=d2,
                container2=d4,
                container3=d4,
            )
        ],
    )


def write_hapag_from_blok_db(input_path: str, output_path: str):
    lookup_ports_list = [DenormalizeLine(**row) for row in csv_to_list(input_path)]
    records = []
    for lookup_ports in lookup_ports_list:
        logger.info(f"{lookup_ports.pol_code} -> {lookup_ports.pod_code}")

        result = get_blok_line_by_codes(
            start_code=lookup_ports.pol_code, end_code=lookup_ports.pod_code
        )
        if not result:
            logger.info(
                f"NOT FOUND: start_code:{lookup_ports.pol_code} end_code:{lookup_ports.pod_code}"
            )
            continue
        lines = result.get("rates")
        if not lines or len(lines) < 1:
            logger.info(
                f"Empty Lines.Please debug {lookup_ports.pol_code} -> {lookup_ports.pod_code}"
            )
            continue
        hapag_line = lines[0]
        hapag_line["start_code"] = lookup_ports.pol_code
        hapag_line["end_code"] = lookup_ports.pod_code
        records.append(hapag_line)
    write_data_json(records=records, path=output_path)
