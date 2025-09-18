from typing import Literal
from config.logger import logger
from utils.json_util import write_data_json
from utils.csv_util import csv_to_list
from scrapers.hapag.hapag_scrape_utils import get_hapag_cookies, hapag_quote_api


def get_hapag_rate(input_path: str, output_path: str, account_no: Literal[0, 1]):
    print(f"scrape:{input_path}")
    hapag_input_list = csv_to_list(path=input_path)
    hapag_token, hapag_cookies = get_hapag_cookies(account_no)
    records = []

    for idx, input_list in enumerate(hapag_input_list):
        if hapag_cookies is None:
            break
        start_code = input_list.get("pol_code")
        start_name = input_list.get("pol")
        end_code = input_list.get("pod_code")
        end_name = input_list.get("pod_name")
        logger.info(f"collecting the data {idx}. {start_code} -> {end_code}....")
        data = hapag_quote_api(
            token=hapag_token,
            cookies=hapag_cookies,
            start_code=start_code,
            start_name=start_name,
            end_code=end_code,
            end_name=end_name,
        )
        if not data:
            logger.info("no data")
            continue
        if data == "RESQUEST_EXCEEDED":
            break
        records.append(data)
    if not records:
        logger.warning("terminated: records empty :(")
        return
    logger.info("Finished: Data fetch completed 🏆")
    write_data_json(records=records, path=output_path)
    logger.info(f"Finished: json writing path {output_path}🏆")
    return records
