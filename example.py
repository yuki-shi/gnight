#!/usr/bin/env python3

from gnight import read_from_sheets, update_sheets
import pandas as pd

# Worksheet name
sheet_name = 'Página1'

# Basically, all visible cells
sheet_range = 'A1:ZZ'

# URL of target Google Sheets File
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1xC9T3xb_u_FYwc7XpGXHE2k245BRw_JkelTbKKkZW4A/edit#gid=0'

# Import Sheet's data to a DataFrame
df = read_from_sheets(spreadsheet_url, sheet_name, sheet_range)

# Transformation logic
df['formato'] = df['formato'].str.lower()

# Insert updated DataFrame on Google Sheets
update_sheets(df, spreadsheet_url, sheet_name, sheet_range)
