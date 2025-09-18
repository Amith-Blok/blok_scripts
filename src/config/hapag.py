from config.settings import (
    HAPAG_LOGIN_EMAIL,
    HAPAG_LOGIN_EMAIL_TWO,
    HAPAG_LOGIN_PASSWORD,
    HAPAG_LOGIN_PASSWORD_TWO,
)

HAPAG_QUOTE_URL = "https://qbe.api.hlag.cloud/api/quotations/quotation"
HAPAG_QUOTE_HEADER = {
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
}
HAPAG_LOCATION_URL = "https://locations.api.hlag.cloud/api/locations"
HAPAG_LOCATION_HEADER = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "origin": "https://www.hapag-lloyd.com",
    "priority": "u=1, i",
    "referer": "https://www.hapag-lloyd.com/",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    "x-token": "eyJhbGciOiJSUzI1NiIsImtpZCI6InpaX3V5cWNMZEwtZFZSaTdkclRPbEZIMEctazJ2M2MtYnJ1bVJERVdwSVUiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE3MzIzMDQxOTUsIm5iZiI6MTczMjI5MzM5NSwidmVyIjoiMS4wIiwiaXNzIjoiaHR0cHM6Ly9obGFnd2VicHJvZC5iMmNsb2dpbi5jb20vNjNkZjhlNzEtMDYxMi00OTMyLWE2ZGUtMmEwZjVhYTNjNzhjL3YyLjAvIiwic3ViIjoiVzMyMDQ5MyIsImF1ZCI6IjY0ZDdhNDRiLTFjNWItNGI1Mi05ZmY5LTI1NGY3YWNkOGZjMCIsImFjciI6ImIyY18xYV9zaWdudXBfc2lnbmluIiwibm9uY2UiOiIwMTkzNTRiYi00OTA2LTdkNjYtYmIxZS1kNzYyY2U0MmUxM2IiLCJpYXQiOjE3MzIyOTMzOTUsImF1dGhfdGltZSI6MTczMjI5MzM5MiwianRpIjoiNjhiZGIwMWUtYmVkZS00ZTY4LTg2YWYtOGI0MmZiMzM1MzE5Iiwiam9iVGl0bGUiOiJnZW5lcmFsaXN0IiwiZXh0ZW5zaW9uX1VJRCI6IlczMjA0OTMiLCJ0aWQiOiI2M2RmOGU3MS0wNjEyLTQ5MzItYTZkZS0yYTBmNWFhM2M3OGMiLCJwYXNzd29yZEV4cGlyZWQiOmZhbHNlfQ.HP3S03i6JtlE7brg7kwT7eUF1kCp0e8itOVOH-Uxy3uH1QnqZOuM6e0zEbvpb4ERR39pPptz7lmfxpNkKFuckh8S_Abop9hNo_0810pGST4ZrNj-8Uq5-Mfa04sIARCSfxCO72PsSfzdFHBM73xUvmjpFhkx8JnhfQYi_Dd9YZlkVcLGkYyUFAuBaWqYhk7y0np_yvEVn64YoD05SQ9hWxUn3jjs3zFIbi_rztGXec9JxdRCKhB-xqraF5LNZ4XPdfPkNwITifGRcyXFfC3ytrseOFTsvsHx27aX5HFmQX6ExDG0XZGICJ6QFPmT25K8vJUbZKJWB8AYqzWFCf6u7g",
}
HAPAG_LOGIN_URL = "https://www.hapag-lloyd.com/solutions/auth/login.html"

HAPAG_ACCOUNTS = {
    0: {"email": HAPAG_LOGIN_EMAIL, "password": HAPAG_LOGIN_PASSWORD},
    1: {"email": HAPAG_LOGIN_EMAIL_TWO, "password": HAPAG_LOGIN_PASSWORD_TWO},
}
