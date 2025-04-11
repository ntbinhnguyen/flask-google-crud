import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(os.getenv("SHEET_ID")).sheet1

def get_all_data():
    return sheet.get_all_records()

def add_row(data):
    sheet.append_row(data)

def delete_row(index):
    sheet.delete_row(index + 2)

def update_row(index, data):
    sheet.update(f"A{index + 2}:C{index + 2}", [data])