import pandas as pd

from src.config.logger import logger
from src.utils.google_sheet import (
    get_google_workbook_by_id,
    get_last_google_sheet_by_id,
)
from src.config.google_sheet import (
    AIR_FREIGHT_IMPORT_AF_TO_INDIA_GOOGLE_SHEET_ID,
    AIR_FREIGHT_IMPORT_CANADA_TO_INDIA_GOOGLE_SHEET_ID,
    AIR_FREIGHT_IMPORT_EU_TO_INDIA_GOOGLE_SHEET_ID,
    AIR_FREIGHT_IMPORT_FE_TO_INDIA_GOOGLE_SHEET_ID,
    AIR_FREIGHT_IMPORT_ME_TO_INDIA_GOOGLE_SHEET_ID,
    AIR_FREIGHT_IMPORT_SA_TO_INDIA_GOOGLE_SHEET_ID,
    AIR_FREIGHT_IMPORT_US_TO_INDIA_GOOGLE_SHEET_ID,
    CENTRAL_AMERICA_GOOGLE_SHEET_ID,
    INDIAN_SUBCONTINENT_GOOGLE_SHEET_ID,
    USA_CANADA_GOOGLE_SHEET_ID,
    SOUTH_AMERICA_GOOGLE_SHEET_ID,
    EUROPE_TURKEY_GOOGLE_SHEET_ID,
    ALL_SEA_RAIL_GOOGLE_SHEET_ID,
    NEWZEALAND_AUSTRALIA_GOOGLE_SHEET_ID,
    CHINA_GOOGLE_SHEET_ID,
    FAR_EAST_GOOGLE_SHEET_ID,
    MIDDLE_EAST_GOOGLE_SHEET_ID,
    AFRICA_GOOGLE_SHEET_ID,
    ALL_AIR_PORTS_GOOGLE_SHEET_ID,
    AIR_FREIGHT_EXPORT_US_TO_INDIA_GOOGLE_SHEET_ID,
    AIR_FREIGHT_EXPORT_AF_TO_INDIA_GOOGLE_SHEET_ID,
    AIR_FREIGHT_EXPORT_CANADA_TO_INDIA_GOOGLE_SHEET_ID,
    AIR_FREIGHT_EXPORT_EU_TO_INDIA_GOOGLE_SHEET_ID,
    AIR_FREIGHT_EXPORT_FE_TO_INDIA_GOOGLE_SHEET_ID,
    AIR_FREIGHT_EXPORT_ME_TO_INDIA_GOOGLE_SHEET_ID,
    AIR_FREIGHT_EXPORT_SA_TO_INDIA_GOOGLE_SHEET_ID,
    DESTINATION_CHARGES_GOOGLE_SHEET_ID,
        )


def export_indian_subcontinent_sheet_to_excel(
    sheet_id=INDIAN_SUBCONTINENT_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/indian_subcontinent_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df

def export_us_canada_sheet_to_excel(
    sheet_id=USA_CANADA_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/us_canada_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    # Convert list of lists to list of dicts for DictWriter
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df
def export_central_america_sheet_to_excel(
    sheet_id=CENTRAL_AMERICA_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/central_america_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df

def export_south_america_sheet_to_excel(
    sheet_id=SOUTH_AMERICA_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/south_america_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df

def export_eu_sheet_to_excel(
    sheet_id=EUROPE_TURKEY_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/eu_turkey_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df


def export_oc_sheet_to_excel(
    sheet_id=NEWZEALAND_AUSTRALIA_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/oc_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df


def export_me_sheet_to_excel(
    sheet_id=MIDDLE_EAST_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/me_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df


def export_fe_sheet_to_excel(
    sheet_id=FAR_EAST_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/fe_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)

    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df


def export_cn_sheet_to_excel(
    sheet_id=CHINA_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/cn_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df


def export_af_sheet_to_excel(
    sheet_id=AFRICA_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/africa_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df


def export_airfreight_import_af_to_india_sheet_to_excel(
    sheet_id=AIR_FREIGHT_IMPORT_AF_TO_INDIA_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/airfreight_import_af_to_india_sheet.xlsx",
):
    logger.info(f"Exporting {sheet_id} to {output_path}")
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df


def export_airfreight_import_us_to_india_sheet_to_excel(
    sheet_id=AIR_FREIGHT_IMPORT_US_TO_INDIA_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/airfreight_import_usa_to_india_sheet.xlsx",
):
    logger.info(f"Exporting {sheet_id} to {output_path}")
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df


def export_airfreight_import_canada_to_india_sheet_to_excel(
    sheet_id=AIR_FREIGHT_IMPORT_CANADA_TO_INDIA_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/airfreight_import_canada_to_india_sheet.xlsx",
):
    logger.info(f"Exporting {sheet_id} to {output_path}")
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df


def export_airfreight_import_eu_to_india_sheet_to_excel(
    sheet_id=AIR_FREIGHT_IMPORT_EU_TO_INDIA_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/airfreight_import_eu_to_india_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df


def export_airfreight_import_fe_to_india_sheet_to_excel(
    sheet_id=AIR_FREIGHT_IMPORT_FE_TO_INDIA_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/airfreight_import_fe_to_india_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df


def export_airfreight_import_me_to_india_sheet_to_excel(
    sheet_id=AIR_FREIGHT_IMPORT_ME_TO_INDIA_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/airfreight_import_me_to_india_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df


def export_airfreight_import_sa_to_india_sheet_to_excel(
    sheet_id=AIR_FREIGHT_IMPORT_SA_TO_INDIA_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/airfreight_import_sa_to_india_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df


def export_airfreight_export_us_to_india_sheet_to_excel(
    sheet_id=AIR_FREIGHT_EXPORT_US_TO_INDIA_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/airfreight_export_us_to_india_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df


def export_airfreight_export_canada_to_india_sheet_to_excel(
    sheet_id=AIR_FREIGHT_EXPORT_CANADA_TO_INDIA_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/airfreight_export_canada_to_india_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df


def export_airfreight_export_eu_to_india_sheet_to_excel(
    sheet_id=AIR_FREIGHT_EXPORT_EU_TO_INDIA_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/airfreight_export_eu_to_india_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df


def export_airfreight_export_fe_to_india_sheet_to_excel(
    sheet_id=AIR_FREIGHT_EXPORT_FE_TO_INDIA_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/airfreight_export_fe_to_india_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df


def export_airfreight_export_me_to_india_sheet_to_excel(
    sheet_id=AIR_FREIGHT_EXPORT_ME_TO_INDIA_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/airfreight_export_me_to_india_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df


def export_airfreight_export_sa_to_india_sheet_to_excel(
    sheet_id=AIR_FREIGHT_EXPORT_SA_TO_INDIA_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/airfreight_export_sa_to_india_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df


def export_airfreight_export_af_to_india_sheet_to_excel(
    sheet_id=AIR_FREIGHT_EXPORT_AF_TO_INDIA_GOOGLE_SHEET_ID,
    save_to_excel: bool = True,
    output_path: str = "./data/google_sheets/airfreight_export_af_to_india_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data = raw_data[1:]
    print(header)
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df



def export_all_air_port_sheets_to_excel(
    sheet_id=ALL_AIR_PORTS_GOOGLE_SHEET_ID,
    save_to_excel: bool = False,
    output_path: str = "./data/google_sheets/all_air_port_sheet.xlsx",
):
    workbook = get_google_workbook_by_id(sheet_id)
    all_dataframes = {}
    for worksheet in workbook.worksheets():
        data = worksheet.get_all_values()
        if data:
            header = data[0]
            data_rows = data[1:]
            df = pd.DataFrame(data_rows, columns=header)
            all_dataframes[worksheet.title] = df

    if save_to_excel:
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            for sheet_name, df in all_dataframes.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
    logger.info(f"Converted all worksheets from {sheet_id} to {output_path}")

    return workbook


def export_all_sea_rail_sheets_to_excel(
    sheet_id=ALL_SEA_RAIL_GOOGLE_SHEET_ID,
    save_to_excel: bool = False,
    output_path: str = "./data/google_sheets/all_sea_rail_sheet.xlsx",
):
    workbook = get_google_workbook_by_id(sheet_id)
    all_dataframes = {}
    for worksheet in workbook.worksheets():
        data = worksheet.get_all_values()
        if data:
            header = data[0]
            data_rows = data[1:]
            df = pd.DataFrame(data_rows, columns=header)
            all_dataframes[worksheet.title] = df

    if save_to_excel:
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            for sheet_name, df in all_dataframes.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
    logger.info(f"Converted all worksheets from {sheet_id} to {output_path}")

    return workbook

def export_destination_charges_sheet_to_excel(
    sheet_id=DESTINATION_CHARGES_GOOGLE_SHEET_ID,
    save_to_excel: bool = False,
    output_path: str = "./data/google_sheets/destination_charges_sheet.xlsx",
):
    worksheet = get_last_google_sheet_by_id(sheet_id)
    header = worksheet.get_all_values()[0]
    data = worksheet.get_all_values()[1:]
    df = pd.DataFrame(data, columns=header)

    if save_to_excel:
        df.to_excel(output_path, index=False)
        logger.info(f"Converted {sheet_id} to {output_path}")

    return df