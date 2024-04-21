import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import date

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def authenticate(credentials_file):
    """Authenticate with Google Calendar API using service account credentials."""
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    try:
        creds = service_account.Credentials.from_service_account_file(credentials_file, scopes=SCOPES)
        return build('calendar', 'v3', credentials=creds)
    except Exception as e:
        logger.error("Failed to authenticate with Google Calendar API: %s", e)
        return None

def fetch_daily_calendar(service, date):
    """Fetch daily calendar events."""
    try:
        start_time = f"{date}T00:00:00Z"
        end_time = f"{date}T23:59:59Z"
        events_result = service.events().list(calendarId='primary', timeMin=start_time, timeMax=end_time, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events
    except Exception as e:
        logger.error("Failed to fetch daily calendar events: %s", e)
        return []

def output_daily_calendar(events, filename):
    """Output daily calendar events to a file."""
    try:
        with open(filename, 'w') as file:
            if not events:
                file.write("No events scheduled for the day.")
            else:
                for event in events:
                    start_time = event.get('start', {}).get('dateTime', event.get('start', {}).get('date'))
                    end_time = event.get('end', {}).get('dateTime', event.get('end', {}).get('date'))
                    summary = event.get('summary', 'N/A')
                    location = event.get('location', 'N/A')
                    file.write(f"Start Time: {start_time}\n")
                    file.write(f"End Time: {end_time}\n")
                    file.write(f"Summary: {summary}\n")
                    file.write(f"Location: {location}\n")
                    file.write("\n")
    except Exception as e:
        logger.error("Failed to output daily calendar to file: %s", e)

def main():
    # Authenticate with Google Calendar API
    service = authenticate('smart-mirror-v1-421000-e44953c1918a.json')
    if service:
        # Fetch and output daily calendar events
        today = date.today().isoformat()
        events = fetch_daily_calendar(service, today)
        output_daily_calendar(events, 'daily_calendar.txt')

if __name__ == "__main__":
    main()
