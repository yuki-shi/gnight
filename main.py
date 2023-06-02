#!/usr/bin/env python3

from gnight import read_from_sheets

sheet_name = 'Página1'
sheet_range = 'A1:E10'
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1xC9T3xb_u_FYwc7XpGXHE2k245BRw_JkelTbKKkZW4A/edit#gid=0'

df = read_from_sheets(spreadsheet_url, sheet_name, sheet_range)
print(df)
