from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import pandas as pd
import os
import re

SERVICE_ACCOUNT_PATH = os.getenv('SERVICE_ACCOUNT_PATH')

def validate_connection(func):
    def wrapper(*args, **kwargs):
        # Get credentials from service account file in JSON format
        try:
            creds = service_account.Credentials.from_service_account_file(
                    filename=SERVICE_ACCOUNT_PATH
            )
            service = build('sheets', 'v4', credentials=creds)
            sheet = service.spreadsheets()
            func(sheet, *args, **kwargs)
            return 
        except HttpError as err:
            print(err)
            return
    return wrapper

def get_id_from_url(url: str) -> str:
    """
    Search for the spreadsheet id within its url

    Args:
        url (str): spreadsheet's URL

    Returns:
        str: Spreadsheet ID
    """
    return re.findall(r'(?<=d\/).*(?=\/)', url)[0]

@validate_connection
def read_to_dataframe(sheet,
                      speadsheet_url: str,
                      sheet_name: str,
                      sheet_range: str) -> pd.DataFrame:
    """
    Read worksheet data into a Pandas' DataFrame

    Args:
        spreadsheet_url (str): Spreadsheet's URL
        sheet_name (str): Worksheet name. It can also be its index in int format
        sheet_range (str): Desired extraction range in A1 syntax
    
    Returns:
        pd.DataFrame: Worksheet data in DataFrame format
    """
    spreadsheet_id = get_id_from_url(spreadsheet_url)

    # If worksheet index was inputted, search for its name in the spreadsheet's metadata
    if type(sheet_name) == int:
        metadata = sheet.get(spreadsheetId=spreadsheet_id).execute()
        page_names = metadata.get('sheets', {})
        for index, page_title in enumerate(page_names):
            if index == sheet_name:
                sheet_name = page_title['properties']['title']

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
