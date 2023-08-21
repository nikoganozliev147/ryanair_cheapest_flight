from datetime import datetime
# import schedule
# import time
from ryanair import Ryanair
from ryanair.types import Flight
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


credentials = Credentials.from_service_account_file('credentials.json')
service = build('sheets', 'v4', credentials=credentials)
spreadsheet_id = '1IowLG7wSccUK36WNrFOO4fPJHsJqHoBm1rANrUNL164'
sheet_name = 'Sheet1'


def get_cheapest_flight_and_update_spreadsheet():
    api = Ryanair(currency="EUR")
    start_date = datetime(2023, 9, 6).date()
    end_date = datetime(2023, 9, 15).date()

    flights = api.get_cheapest_flights("SOF", start_date, end_date, destination_airport="BHX")
    flight: Flight = flights[0]
    flight_dict = flight._asdict()

    update_spreadsheet(flight_dict)


def update_spreadsheet(flight_dict):
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sheet_values = [
        [
            current_datetime,
            flight_dict['departureTime'].isoformat(),
            flight_dict['flightNumber'],
            flight_dict['price'],
            flight_dict['currency'],
            flight_dict['origin'],
            flight_dict['originFull'],
            flight_dict['destination'],
            flight_dict['destinationFull']
        ]
    ]

    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A1",
        valueInputOption='USER_ENTERED',
        body={'values': sheet_values}
    ).execute()


# Schedule the job to run every 10 seconds
# schedule.every(1).hours.do(get_cheapest_flight_and_update_spreadsheet)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1 * 60 * 60)

get_cheapest_flight_and_update_spreadsheet()
