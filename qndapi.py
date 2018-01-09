#! python3.4
# -*- encoding: utf-8 -*-
"""
## Quick and Dirty Api Tester - _QNDAPI_

This program aims to be a very simples API tester. This is its main module.
"""

# Importing the path so I can find the current directory
from os import path
from sys import exit
# Importing an YAML parser
import dumbyaml as yaml
# Importing the YAMLError so that I can handle this kind of error properly
from yaml.error import YAMLError
# Importing the Requests library, to make HTTP requests
import requests
# Importing the datetime, to process the current date and time
from datetime import datetime
# Importing the Log class from the model module
from model import Log

# This is the e-mail message I'll send if any endpoint fails to send me a
# `HTTP-200 "OK"` code
ASSERTION_ERROR_MAIL = """
<p>Hello,</br>
The amazing Quick 'n' Dirty API tester failed to assert that the path</br>
<b>{path}</b> of the API {api} returned a HTTP-200 code.</br>
The test was performed at {datetime}</br></p>
<p>Best of luck,</br>
QNDAPIT<p>
"""

# This other e-mail message will be used if I'm not able to even connect to a
# host
CONNECTION_ERROR_MAIL = """
<p>Hello,</br>
The amazing Quick 'n' Dirty API tester failed to connect to</br>
<b>{path}</b> of the API {api}.</br>
The test was performed at {datetime}</br></p>
<p>Best of luck,</br>
QNDAPIT<p>
"""


def main():
    """
    This is the module's main function.
    It works, but it needs a little refactoring
    """
    # We'll start by trying to load the configuration file
    try:
        # First we find out the current directory
        current_dir = path.dirname(path.abspath(__file__))

        # Then we append our the configuration filename to it, creating the
        # configuration file's path
        config_path = path.join(current_dir, 'config.yaml')

        # Finally, we open the file, read its contents and load it as a YAML file
        config = yaml.load(open(config_path).read())

    # If we fail to load the config file
    except FileNotFoundError:
        print(
            "Sorry, I could not read the configuration file!\n" +
            "Please, make sure there is a valid config.yaml file at {dirname}"
            .format(dirname=current_dir)
        )
        exit(1)

    except YAMLError as yaml_error:
        print(
            "Sorry, I did find a file at {configpath} but it does not " +
            "seem to be a valid YAML file.\nAnyway, here's the error I got:\n\n\t" +
            str(yaml_error)
        )
        exit(1)

    apis = config['APIs']

    # For each API
    for api in apis.keys():
        # Load the endpoints
        api = str(api)
        endpoints = list(apis[api])

        # For each endpoint
        for endpoint in endpoints:
            endpoint = str(endpoint)
            test_endpoint(api, endpoint, config)




def test_endpoint(api, endpoint, config, expected_code=200):
    """
    Function that tests an endpoint
    """
    url = api + endpoint
    now = datetime.now()
    try:
        # We try to connect
        request = requests.get(url, timeout=5)
    except:
        # If we fail...
        Log(line='Connection error', api=api, endpoint=endpoint,
            timestamp=now).save()
    else:
        # If we succeed.
        try:
            # We try to assert that the response was the expected
            assert request.status_code == expected_code
        except AssertionError:
            # If we fail...
            Log(line='HTTP Error', api=api, endpoint=endpoint,
                timestamp=datetime.now()).save()

            timestamp = now.strftime("%d/%m/%Y @ %Hh%mmin")
            message = ASSERTION_ERROR_MAIL.format(path=endpoint,
                                                  datetime=timestamp, api=api)

            subject = "QNDAPIT Error!"
            receiver = str(config['email']['receiver'])
            token = str(config['email']['token'])

            send_assertion_error_email(token, receiver, subject, message)
        else:
            # If we do assert that the HTTP code was 200
            Log(line='Success', api=api, endpoint=endpoint,
                timestamp=now).save()


def send_assertion_error_email(token, receiver, subject, message):
    """
    Function that send an assertion error email
    """
    api_data = {
        'token': token,
        'message': {
            'to': receiver,
            'subject': subject,
            'html': message
        }
    }
    requests.post('http://email.devnup.com/api/gateway/send', json=api_data)

if __name__ == "__main__":
    main()
