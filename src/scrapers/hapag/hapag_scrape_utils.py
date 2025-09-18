from typing import Literal
from config.logger import logger
from utils.datetime_util import iso_time_now
from seleniumbase import SB
from curl_cffi import requests
from config.hapag import (
    HAPAG_ACCOUNTS,
    HAPAG_QUOTE_HEADER,
    HAPAG_QUOTE_URL,
    HAPAG_LOCATION_URL,
)


# get quotes from hapag
def hapag_quote_api(
    token: str | None,
    cookies: dict,
    start_code: str,
    start_name: str,
    end_name: str,
    end_code: str,
    is_end_port: bool = True,
    is_start_port: bool = True,
):
    if not token:
        return None
    HAPAG_QUOTE_HEADER["x-token"] = token
    # print(
    #     f"token:{token},cookies:{cookies}, start_code:{start_code} start_name:{start_name} end_name:{end_name} end_code:{end_code}"
    # )
    date_now = iso_time_now()
    json_data = {
        "dangerousGoods": {
            "isHazardous": False,
        },
        "end": {
            "name": end_name,
            "locode": end_code,
            "haulage": "MERCHANT_HAULAGE",
            "isPortLocation": is_end_port,
        },
        "equipmentTypeGroup": "STANDARD",
        "language": "EN",
        "start": {
            "name": start_name,
            "locode": start_code,
            "haulage": "MERCHANT_HAULAGE",
            "isPortLocation": is_start_port,
        },
        "validFrom": date_now,
        "shippersOwnedContainer": False,
    }
    session = requests.Session()
    session.cookies.update(cookies)
    # print("SESSION:", session.cookies.get_dict())

    try:
        response = session.post(
            HAPAG_QUOTE_URL,
            impersonate="chrome100",
            headers=HAPAG_QUOTE_HEADER,
            json=json_data,
        )
        if not response.ok:
            print("status_code:", response.status_code)
            # print("headers:",response.headers)
            logger.critical(response.text)
            error_json = response.json()
            error_reason = error_json.get("errorReason", "")
            if error_reason == "RequestsLimitExceeded":
                return "RESQUEST_EXCEEDED"
            return None

        data = response.json()

        quotation = data["quotation"]
        quotation["start_code"] = start_code
        quotation["start_name"] = start_name
        quotation["end_name"] = end_name
        quotation["end_code"] = end_code
        return quotation

    except Exception as e:
        print("Execptions at hapag request quotation:")
        logger.critical(e)
        return None


# get cookies from hapag browser
def get_hapag_cookies(acount_no: Literal[0, 1]) -> tuple[str | None, dict | None]:
    account = HAPAG_ACCOUNTS[acount_no]
    user_name = account["email"]
    password = account["password"]

    with SB(uc=True, test=True, incognito=True, undetectable=True) as sb:
        # url =HAPAG_LOGIN_URL
        quote_url = (
            "https://www.hapag-lloyd.com/solutions/new-quote/#/quick-quotes?language=en"
        )
        sb.uc_open_with_reconnect(quote_url, 20)
        sb.uc_gui_click_captcha()
        sb.wait_for_element("button#accept-recommended-btn-handler", timeout=30)
        sb.uc_click("button#accept-recommended-btn-handler", timeout=30)
        sb.type("#signInName", user_name)
        sb.type("#password", password)
        sb.uc_click("button#next", 20)
        sb.sleep(5)
        sb.uc_open_with_reconnect(quote_url)
        sb.sleep(2)
        # Get token
        local_storage = sb.execute_script("return window.localStorage;")
        token = local_storage["token"]
        # Get Cookies
        cookies = sb.driver.get_cookies()
        cookies_dict = {cookie["name"]: cookie["value"] for cookie in cookies}
        # Print Local storage
        print("token:", token)
        print("cookes_dict:", cookies_dict)
        if not token:
            return None, None
        return token, cookies_dict


def get_hapag_location_details(token: str, port_code: str) -> None | dict:
    if not token:
        print("no token found")
        return None
    HAPAG_QUOTE_HEADER["x-token"] = token
    params = {
        "search": port_code,
        "limit": "1",
        "orderType": "seaportsfirst",
    }
    try:
        response = requests.post(
            HAPAG_LOCATION_URL,
            impersonate="chrome123",
            params=params,
            headers=HAPAG_QUOTE_HEADER,
        )

        if not response.ok:
            print(f"Request failed with status code: {response.status_code}")
            print(f"Response content: {response.text}")
            return None

        data = response.json()
        print(f"Response JSON: {data}")

        locations = data.get("locations", [])
        if not locations:
            print("No locations found in the response.")
            return None

        location = locations[0]
        location_details = {
            "h_code": location.get("locationNumber"),
            "port_name": location.get("businessLocationName"),
            "port_code": location.get("businessLocode"),
        }

        return location_details

    except Exception as e:
        print("Something went wrong in get_hapag_location_details()")
        print(f"Error: {e}")
        return None


def test_request(token: str):
    try:
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.8",
            "content-type": "application/json",
            "hlag-app-request-origin": "new_quote",
            "origin": "https://www.hapag-lloyd.com",
            "priority": "u=1, i",
            "referer": "https://www.hapag-lloyd.com/",
            "sec-ch-ua": '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
            "x-token": token,
        }
        json_data = {
            "dangerousGoods": {
                "isHazardous": False,
            },
            "end": {
                "name": "SEATTLE, WA",
                "locode": "USSEA",
                "haulage": "MERCHANT_HAULAGE",
                "isPortLocation": True,
            },
            "equipmentTypeGroup": "STANDARD",
            "language": "EN",
            "start": {
                "name": "INCOK",
                "locode": "INDRI",
                "haulage": "MERCHANT_HAULAGE",
                "isPortLocation": True,
            },
            "validFrom": "2025-04-07",
            "shippersOwnedContainer": False,
        }
        response = requests.post(
            "https://qbe.api.hlag.cloud/api/quotations/quotation",
            impersonate="chrome100",
            headers=headers,
            json=json_data,
        )
        print(f"Resposne:{response.text}")
    except Exception as e:
        print(f"ERROR:{e}")


if __name__ == "__main__":
    pass
