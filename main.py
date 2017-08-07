import os
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from oauth2client.service_account import ServiceAccountCredentials


SHEETS_DISCOVERY_URL='https://sheets.googleapis.com/$discovery/rest?version=v4'


def main(spreadsheet_key, sheet_name, range_name, service_account_json):
    """Returns data from sheet_name and range from a google sheet"""

    # We have to write it to a file because gcs library only accepts a file path.
    # Rewrite. Must not use /tmp because it is re-used
    credentials_path = '/tmp/credentials.json'
    with open(credentials_path, "w") as credentials_file:
        credentials_file.write(service_account_json)

    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path)
    service = discovery.build('sheets', 'v4', credentials=credentials, discoveryServiceUrl=SHEETS_DISCOVERY_URL)

    range_name = '{}!{}'.format(sheet_name, range_name)

    data = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_key, range=range_name, majorDimension='ROWS').execute()['values']

    # Delete so that it is not reused.
    # TODO: check if this is secure. What if this fails? This is NOT secure.
    os.remove(credentials_path)

    return data
