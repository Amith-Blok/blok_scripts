from src.config.haulage import INDIAN_OUTBOUND_HAULAGE_PATH
from src.services.haulage.haulage_format import format_haulage
import pandas as pd


def outbound_haulage_pipeline(path=INDIAN_OUTBOUND_HAULAGE_PATH):
    """
    Pipeline for outbound haulage.
    """
    final_df = format_haulage(path)
    print(final_df.head())
    print("Total rows:", len(final_df))
    final_df.to_csv("outbound_haulage.csv",index=False)

