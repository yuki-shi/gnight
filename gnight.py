from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import pandas as pd
import os
import re

SERVICE_ACCOUNT_PATH = os.getenv('SERVICE_ACCOUNT_PATH')

def validate_connection(func):
    def wrapper(*args, **kwargs):
        try:
            creds = service_account.Credentials.from_service_account_file(
                    filename=SERVICE_ACCOUNT_PATH
            )
            service = build('sheets', 'v4', credentials=creds)
            sheet = service.spreadsheets()
            print(type(sheet))
            func(sheet, *args, **kwargs)
            return 
        except HttpError as err:
            print(err)
            return
    return wrapper

def get_id_from_url(url: str) -> str:
    return re.findall(r'(?<=d\/).*(?=\/)', url)[0]

@validate_connection
def read_to_dataframe(sheet: googleapiclient.discovery.Resource,
                      speadsheet_url: str,
                      sheet_name: str,
                      sheet_range: str) -> pd.DataFrame:
    spreadsheet_id = get_id_from_url(spreadsheet_url)
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=f'{sheet_name}!{sheet_range}').execute()
    values = result.get('values', [])

    if not values:
        print('No data found')

    return pd.DataFrame(values[1:], columns=values[0])



sheet_name = ''
sheet_range = 'A1:E10'
spreadsheet_url = ''

df = read_to_dataframe(spreadsheet_url, sheet_name, sheet_range)
