import uuid
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE') 
SCOPES = ['https://www.googleapis.com/auth/drive']
PROJECT_ID = os.getenv('PROJECT_ID')
TOPIC_NAME = os.getenv('TOPIC_NAME')

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

drive_service = build('drive', 'v3', credentials=credentials)

start_page_token = drive_service.changes().getStartPageToken().execute()
print("Start token:", start_page_token)

channel_id = str(uuid.uuid4())
watch_request_body = {
    "id": "drive-watch-003",
    "type": "web_hook",
    "address": "https://your-server.com/drive-notify-endpoint"
}

watch_response = drive_service.changes().watch(
    pageToken=start_page_token['startPageToken'],
    body=watch_request_body
).execute()

print("Watch response:", watch_response)
