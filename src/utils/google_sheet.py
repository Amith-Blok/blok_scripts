import gspread
from oauth2client.service_account import ServiceAccountCredentials
DEFAULT_GOOGLE_SHEET_SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
DEFAULT_GOOGLE_SHEET_CREDENTIAL_PATH = "src/config/google_sheet_credential.json"

def get_google_sheet_client(credential_path: str = DEFAULT_GOOGLE_SHEET_CREDENTIAL_PATH, scope: list[str] = DEFAULT_GOOGLE_SHEET_SCOPE):
    creds = ServiceAccountCredentials.from_json_keyfile_name(credential_path, scope)
    client = gspread.authorize(creds)
    return client


def get_google_workbook_by_id(sheet_id: str,credential_path: str = DEFAULT_GOOGLE_SHEET_CREDENTIAL_PATH, scope: list[str] = DEFAULT_GOOGLE_SHEET_SCOPE) -> gspread.Spreadsheet:
    client = get_google_sheet_client(credential_path, scope)
    return client.open_by_key(sheet_id)

def get_google_workbook_by_name(sheet_name: str,credential_path: str = DEFAULT_GOOGLE_SHEET_CREDENTIAL_PATH, scope: list[str] = DEFAULT_GOOGLE_SHEET_SCOPE) -> gspread.Spreadsheet:
    client = get_google_sheet_client(credential_path, scope)
    return client.open(sheet_name)

def get_last_google_sheet_by_id(sheet_id: str,credential_path: str = DEFAULT_GOOGLE_SHEET_CREDENTIAL_PATH, scope: list[str] = DEFAULT_GOOGLE_SHEET_SCOPE) -> gspread.Spreadsheet:
    client = get_google_sheet_client(credential_path, scope)
    spreadsheet = client.open_by_key(sheet_id)
    return spreadsheet.worksheets()[-1]

