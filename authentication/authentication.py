import sys
import logging
import configparser
from os.path import join
from typing import List
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

UNTAPPD = "UNTAPPD"
EMAIL_SENDER = "SENDER_EMAIL"
EMAIL_RECEIVER = "RECEIVER_EMAIL"

CREDENTIALS_DIR = "credentials"
AUTHENTICATION_DIR = "authentication"
CONFIG_FILENAME = "config.ini"


def _get_config_path():
    return join(AUTHENTICATION_DIR, CREDENTIALS_DIR, CONFIG_FILENAME)


def _get_credentials(category: str, parameter: str):
    try:
        path = _get_config_path()
        config = configparser.ConfigParser()
        config.read(path)
        cat = config[category]
    except KeyError as err:
        raise KeyError(f"{CONFIG_FILENAME} seems to be invalid \n{err}")
    return cat[parameter]


def authorize_untappd(urls: List[str]):
    try:
        result = []
        for url in urls:
            my_id = _get_credentials(UNTAPPD, "CLIENT_ID")
            my_secret = _get_credentials(UNTAPPD, "CLIENT_SECRET")
            url += f"&client_id={my_id}&client_secret={my_secret}"
            result.append(url)
    except FileNotFoundError:
        logging.error(f"\nPlease, save your credentials to the {CONFIG_FILENAME} file")
        sys.exit(1)
    return result


def _get_email_data(who: str, param: str):
    assert who in ['SENDER_EMAIL', 'RECEIVER_EMAIL']
    try:
        path = _get_config_path()
        config = configparser.ConfigParser()
        config.read(path)
        result = config[who][param]
    except FileNotFoundError:
        logging.error(f"\nPlease, save your {who} & {param} data to the {CONFIG_FILENAME} file")
        sys.exit(1)
    if result is not None:
        return str(result)


def send_email(message: str):
    sg = sendgrid.SendGridAPIClient(api_key=_get_email_data("SENDER_EMAIL", "SG_KEY"))
    from_email = Email(_get_email_data("SENDER_EMAIL", "ADDRESS"))  # Change to your verified sender
    to_email = To(_get_email_data("RECEIVER_EMAIL", "ADDRESS"))  # Change to your recipient
    subject = "Untappd Daily Feed"
    content = Content("text/plain", message)
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)
