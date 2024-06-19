import base64
import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

class GmailDownloader:
    def __init__(self, credentials_file, token_dir, base_download_dir, user_email):
        self.credentials_file = credentials_file
        self.token_file = os.path.join(token_dir, f"token_{user_email}.pickle")
        self.base_download_dir = base_download_dir
        self.user_email = user_email
        self.download_dir = os.path.join(base_download_dir, user_email)
        os.makedirs(token_dir, exist_ok=True)
        self.service = self.authenticate_gmail()

    def authenticate_gmail(self):
        
        creds = None
        if os.path.exists(self.token_file):
            with open(self.token_file, "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open(self.token_file, "wb") as token:
                pickle.dump(creds, token)
        return build("gmail", "v1", credentials=creds)

    def list_messages(self, user_id="me"):
       
        try:
            response = self.service.users().messages().list(userId=user_id).execute()
            messages = []
            if "messages" in response:
                messages.extend(response["messages"])
            while "nextPageToken" in response:
                page_token = response["nextPageToken"]
                response = self.service.users().messages().list(userId=user_id, pageToken=page_token).execute()
                if "messages" in response:
                    messages.extend(response["messages"])
            return messages
        except Exception as error:
            print(f"Erro ao listar mensagens: {error}")
            return []

    def get_message(self, user_id, msg_id):
       
        try:
            message = self.service.users().messages().get(userId=user_id, id=msg_id, format="raw").execute()
            return message
        except Exception as error:
            print(f"Erro ao obter mensagem: {error}")
            return None

    def save_email_content(self, msg, store_dir):
        
        raw_email = base64.urlsafe_b64decode(msg["raw"].encode("ASCII"))
        email_file_path = os.path.join(store_dir, f"{msg['id']}.eml")

        with open(email_file_path, "wb") as f:
            f.write(raw_email)
            print(f'Saved email to: {email_file_path}')

    def download_emails_and_attachments(self):
        
        messages = self.list_messages()
        print(f'Total messages: {len(messages)}')

        for message in messages:
            msg_id = message["id"]
            msg = self.get_message("me", msg_id)
            if msg:
                self.save_email_content(msg, self.download_dir)

def main():
    credentials_file = "credentials/.credentials.json"
    token_dir = "tokens"
    base_download_dir = "downloaded_emails"
    user_email = input("Enter the user's email address: ")

    downloader = GmailDownloader(credentials_file, token_dir, base_download_dir, user_email)
    os.makedirs(downloader.download_dir, exist_ok=True)
    downloader.download_emails_and_attachments()

if __name__ == "__main__":
    main()
