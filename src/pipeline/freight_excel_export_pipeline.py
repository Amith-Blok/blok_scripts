from typing import List
from pandas import DataFrame
from src.services.excel_exporter import (
    export_central_america_sheet_to_excel,
    export_indian_subcontinent_sheet_to_excel,
    export_us_canada_sheet_to_excel,
    export_south_america_sheet_to_excel,
    export_eu_sheet_to_excel,
    export_oc_sheet_to_excel,
    export_me_sheet_to_excel,
    export_fe_sheet_to_excel,
    export_cn_sheet_to_excel,
    export_af_sheet_to_excel,
)

SEA_FREIGHT_DATA= {
    "EU": export_eu_sheet_to_excel,
    "SA": export_south_america_sheet_to_excel,
    "NA": export_us_canada_sheet_to_excel,
    "OC": export_oc_sheet_to_excel,
    "ME": export_me_sheet_to_excel,
    "FE": export_fe_sheet_to_excel,
    "CN": export_cn_sheet_to_excel,
    "AF": export_af_sheet_to_excel,
    "IS": export_indian_subcontinent_sheet_to_excel,
    "CA": export_central_america_sheet_to_excel,
}


def freight_excel_export_pipeline(run_list: List[str]=["EU", "NA", "OC", "ME", "FE", "CN", "AF", "SA","IS","CA"])->List[DataFrame]:
    records=[]
    for sheet_name in run_list:
        records.append(SEA_FREIGHT_DATA[sheet_name](save_to_excel=False))
    return records
