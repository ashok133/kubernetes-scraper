# reference - https://gspread.readthedocs.io/en/latest/oauth2.html,

import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# ref - https://stackoverflow.com/questions/40781295/how-to-find-the-first-empty-row-of-a-google-spread-sheet-using-python-gspread
def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))  # fastest
    return str(len(str_list)+1)

def append_row(row_data_list):
    media_id = row_data_list[0]
    url = row_data_list[1]
    data = row_data_list[2]
    # sheet = open_sheet('scraped_data')
    next_row = next_available_row(sheet) #can't be optimized? - Each worker takes up one media_id from the topic and appends it to the sheet
    sheet.update_acell("A{}".format(next_row), media_id)
    sheet.update_acell("B{}".format(next_row), url)
    sheet.update_acell("C{}".format(next_row), data)

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('metrix_drive_api_service_account_key.json', scope)

gs = gspread.authorize(credentials)

sheet = gs.open('scraped_data').sheet1
