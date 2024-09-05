import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



from flask import Flask, jsonify, redirect
from flask import request

SCOPES = ["https://www.googleapis.com/auth/calendar"]

app = Flask(__name__)


flow = Flow.from_client_secrets_file(
    'client_secrets.json',
    scopes=SCOPES
)

flow.redirect_uri = 'http://localhost:8080/oauth2callback'


def verify_credentials(credentials, scopes):
    if not credentials or not os.path.exists('token.json'):
        return redirect('authorize')
    if not credentials.valid:
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            return redirect('authorize')
    return True

@app.route('/')
def index():
    return "Welcome to the Google Calendar API integration!<br><a href='/authorize'>Authorize</a>", 200

@app.route('/authorize')
def authorize():
    authorization_url, _ = flow.authorization_url(prompt='consent')
    return redirect(authorization_url), 302

@app.route('/oauth2callback')
def oauth2callback():
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    
    # Store the credentials for the user
    with open('token.json', 'w') as token:
        token.write(credentials.to_json())
    return redirect('/list_events'), 302

@app.route('/list_events')
def list_events():
    
    try:
    # Retrieve stored credentials
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        if token_verified := verify_credentials(credentials, SCOPES):
            service = build('calendar', 'v3', credentials=credentials)
            events_result = service.calendarList().list(maxResults=10).execute()
            events = events_result.get('items', [])
            return jsonify({"events": events})
        
    except FileNotFoundError:
        # redirecting to '/authorize'
        return redirect('/authorize'), 307
    
    except Exception:
        # for any other exceptions
        return jsonify({"error": "Something went wrong"}), 400

@app.route('/calendar')
def list_tasks():
    
    try:
    # Retrieve stored credentials
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        if token_verified := verify_credentials(credentials, SCOPES):
            service = build('calendar', 'v3', credentials=credentials)
            events_result = service.calendarList().get(calendarId = 'calenderId').execute()
            return jsonify({"events": events_result})
    
    except FileNotFoundError:
        # redirecting to /authorize
        return redirect('/authorize'), 307
    except Exception:
        return jsonify({"error": "Something went wrong"}), 400


@app.route('/create_event')
def create_event():
    # retrieve credentials
    try:
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    
        if token_verified := verify_credentials(credentials, SCOPES):
            service = build('calendar', 'v3', credentials=credentials)
            event = {
                'summary': 'Test Event',
                'start': {
                    'dateTime': '2024-07-20T10:00:00-07:00',
                    'timeZone': 'Asia/Kolkata',
                },
                'end': {
                    'dateTime': '2024-07-20T11:00:00-07:00',
                    'timeZone': 'Asia/Kolkata',
                },
            }
            event = service.events().insert(calendarId='calendarId', body=event).execute()
            return jsonify({"event": event}), 200
        
    except FileNotFoundError:
        redirect('/authorize'), 302
    except Exception as e:
        return jsonify({"error": "Something went wrong", "error_message": e.error_details}), 500

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run('localhost', 8080, debug=True)

