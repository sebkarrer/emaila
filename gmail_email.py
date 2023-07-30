import os.path
import base64
import re
import time
import dateutil.parser as parser
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me',labelIds = ['INBOX'],q="is:unread",maxResults=1).execute()
        message = results.get('messages')

        if not message:
            print('No new messages.')
        else:
            message = message[0]
            msg = service.users().messages().get(userId='me', id=message['id']).execute() 
            email_data = msg['payload']['headers']
            for values in email_data:
                name = values['name']
                if name == 'From':
                    from_name = values['value']
                    for part in msg['payload']['parts']:
                        try:
                            data_text = part['body']["data"]
                            byte_code = base64.urlsafe_b64decode(data_text)
                            text = byte_code.decode("utf-8")
                            print("Message: ", text)
                        except BaseException as error:
                            pass
    except Exception as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
