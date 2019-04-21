from __future__ import print_function

import base64
import datetime
import os.path
import pickle
import time
from email.mime.text import MIMEText

import requests
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.send", "https://www.googleapis.com/auth/gmail.modify",
          "https://www.googleapis.com/auth/gmail.compose", "https://www.googleapis.com/auth/gmail.settings.sharing"]

service = None
has_sent_mail = False
check_interval = 30
movie_id = "NCG997491"
date = "2019-05-05"
movie_name = "Avengers: Endgame"
cinema_api_url = "https://www.filmstaden.se/api/v2/show/stripped/sv/1/1024?filter.countryAlias=se&filter.cityAlias=GB"
reciever_mail = "vidar.halmstad@hotmail.com"


def main():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    global service
    service = build("gmail", "v1", credentials=creds)

    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])

    if not labels:
        print("No labels found.")
    else:
        print("Labels:")
        for label in labels:
            print(label["name"])


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def send_message(user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print("Message Id: %s" % message["id"])
        return message
    except HttpError as error:
        print("An error occured: %s" % error)


def check_for_tickets(movie_id, date, movie_name, cinema_api_url, reciever_url):
    content = requests.get(url=cinema_api_url)
    correct_shows = []
    for show in content.json()["items"]:
        if show["mId"] == movie_id and date in show["utc"]:
            correct_shows.append(show)

    shows_info = ""
    for show in correct_shows:
        time = get_correct_time(datetime.datetime.strptime(show["utc"], "%Y-%m-%dT%H:%M:%SZ"))
        text = time + " in " + show["ct"] + ", " + show["st"]
        shows_info = shows_info + text + "\n"

    mail_subject = "The cinema tickets you've been waiting for " + movie_name + " are now are now available"
    mail_text = "Hi there! \n\nThere are now cinema tickets available for Avengers: Endgame on " + date +\
                " at the following times/locations: \n " + shows_info

    if len(correct_shows) > 0:
        send_message("me", create_message("noreply@vidarmagnusson.com", reciever_url, mail_subject,
                                          mail_text))

        return True
    return False


# TODO: Make this dynamic.
def get_correct_time(datetime):
    return "{}:{}".format(datetime.hour + 2, str(datetime.minute).zfill(2))


if __name__ == "__main__":
    main()


while not has_sent_mail:
    has_sent_mail = check_for_tickets()
    print(str(datetime.datetime.now()) + " checked for tickets, sent email? " + str(has_sent_mail))
    if not has_sent_mail:
        time.sleep(check_interval)
