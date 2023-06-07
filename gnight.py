"""
Based on the official quickstart script found on
https://developers.google.com/sheets/api/quickstart/python
"""

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from typing import Dict
import pandas as pd
import os
import re
import sys

SERVICE_ACCOUNT_PATH = os.getenv('SERVICE_ACCOUNT_PATH')

def validate_connection(func):
    def wrapper(*args, **kwargs):
        # Get credentials from service account file in JSON format
        try:
            if SERVICE_ACCOUNT_PATH is None:
                raise TypeError('No SERVICE_ACCOUNT_PATH enviromental variable found')
            creds = service_account.Credentials.from_service_account_file(
                    filename=SERVICE_ACCOUNT_PATH
            )
            service = build('sheets', 'v4', credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = func(sheet, *args, **kwargs)
            return result
        except HttpError as err:
            print(err)
            return
    return wrapper

def get_id_from_url(url: str) -> str:
    """
    Search for the spreadsheet ID within its URL

    Args:
        url (str): spreadsheet's URL

    Returns:
        str: Spreadsheet ID
    """
    return re.findall(r'(?<=d\/).*(?=\/)', url)[0]

@validate_connection
def get_sheet_metadata(spreadsheet_url: str) -> Dict[int, str]:
    """
    From the spreadsheet URL, get information about each of its worksheets.

    Args:
        spreadsheet_url (str): Spreadsheet's URL

    Returns:
        output_dict (dict): Dictionary containing each worksheet index as key and its name as value. 
    """
    spreadsheet_id = get_id_from_url(spreadsheet_url)
    output_dict = {}

    metadata = sheet.get(spreadsheetId=spreadsheet_id).execute()
    page_names = metadata.get('sheets', {})

    for index, page_title in enumerate(page_names):
        output_dict[index] = page_title
    return output_dict
        
@validate_connection
def read_from_sheets(sheet,
                     speadsheet_url: str,
                     sheet_name: str,
                     sheet_range: str,
                     to_dataframe=True) -> pd.DataFrame:
    """
    Read worksheet data into a Pandas DataFrame.

    Args:
        spreadsheet_url (str): Spreadsheet's URL
        sheet_name (str): Worksheet name. It can also be its index in int format
        sheet_range (str): Desired extraction range in A1 syntax
        to_dataframe (bool): Specify the output format, it can be either a list of lists or DataFrame. Default to True.
    
    Returns:
        pd.DataFrame: Worksheet data in DataFrame format
    """
    spreadsheet_id = get_id_from_url(speadsheet_url)

    # If worksheet index was inputted, search for its name in the spreadsheet's metadata
    if type(sheet_name) == int:
        page_names = get_sheet_metadata()
        for index, page_title in enumerate(page_names):
            if index == sheet_name:
                sheet_name = page_title['properties']['title']

    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=f'{sheet_name}!{sheet_range}').execute()
    values = result.get('values', [])

    if not values:
        print('No data found')
        
    if to_dataframe == True:
        return pd.DataFrame(values[1:], columns=values[0])

    return values

@validate_connection
def update_sheets(sheet,
                  df: pd.DataFrame,
                  speadsheet_url: str,
                  sheet_name: str,
                  sheet_range: str,) -> Dict:
    """
    Update a Google Sheets file based on a Pandas DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame containing the data to be inserted on the Google Sheets file.
        spreadsheet_url (str): Spreadsheet's URL
        sheet_name (str): Worksheet name. It can also be its index in int format
        sheet_range (str): Desired extraction range in A1 syntax

    Returns:
        dict: Dictionary containing metadata of the updated Google Sheet File. Not rendered or used on other functions.  
    """
 
    spreadsheet_id = get_id_from_url(speadsheet_url)
   
    # Format dataframe into a list of lists
    values = df.values.tolist()
    # Add column headers as first element of the list
    values.insert(0, df.columns.tolist())

    data = [
            {
                'range': sheet_range,
                'values': values
                }
            ]
    body = {
            'valueInputOption': 'USER_ENTERED',
            #https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption
            'data': data
            }

    result = sheet.values().batchUpdate(spreadsheetId=spreadsheet_id,
                                        body=body).execute()
    print('Sheet updated!')
    return result

