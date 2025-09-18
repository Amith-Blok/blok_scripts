import pandas as pd
from src.config.logger import logger


def airfreight_excel_to_csv():
    df = pd.read_excel("./data/airfreight/air_freight_export.xlsx", sheet_name=None)
    for sheet_name, sheet_df in df.items():
        name = "_".join(sheet_name.lower().strip().split(" "))
        sheet_df.to_excel(f"./data/airfreight/export/{name}.xlsx", index=False)
        logger.info(f"✅ Saved {name}.xlsx successfully")
