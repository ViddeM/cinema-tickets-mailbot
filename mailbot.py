import base64
from email.mime.text import MIMEText

from googleapiclient import errors


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return { 'raw': base64.urlsafe_b64encode(message.as_string())}


def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print("Message Id: %s" % message["id"])
        return message
    except errors.HttpError as error:
        print("An error occured: %s" % error)




send_message()