#! python3.4
# -*- encoding: utf-8 -*-
from os import path
import dumbyaml as yaml
import requests
import json
from datetime import datetime
from model import Log

ASSERTION_ERROR_MAIL = """
<p>Hello,</br>
The amazing Quick 'n' Dirty API tester failed to assert that the path</br>
<b>{path}</b> of the API {api} returned a HTTP-200 code.</br>
The test was performed at {datetime}</br></p>
<p>Best of luck,</br>
QNDAPIT<p>
"""

CONNECTION_ERROR_MAIL = """
<p>Hello,</br>
The amazing Quick 'n' Dirty API tester failed to connect to</br>
<b>{path}</b> of the API {api}.</br>
The test was performed at {datetime}</br></p>
<p>Best of luck,</br>
QNDAPIT<p>
"""

def main():
    try:
        # Loading the settings
        current_dir = path.dirname(__file__)
        config_path = path.join(current_dir, 'config.yaml')
        config = yaml.load(open(config_path).read())

        apis = config['APIs']

        # For each API
        for api in apis.keys():
            # Load the endpoints
            api = str(api)
            endpoints = list(apis[api])

            # For each endpoint
            for endpoint in endpoints:
                endpoint = str(endpoint)
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
                        # We try to assert that the response was 200
                        assert request.status_code == 200
                    except AssertionError:
                        # If we fail...
                        Log(line='HTTP Error', api=api, endpoint=endpoint,
                            timestamp=datetime.now()).save()

                        timestamp = now.strftime("%d/%m/%Y @ %Hh%mmin")
                        message = ASSERTION_ERROR_MAIL.format(path=endpoint,
                                                    datetime=timestamp,
                                                    api=api)

                        subject = "QNDAPIT Error!"
                        receiver = str(config['email']['receiver'])
                        token = str(config['email']['token'])

                        send_assertion_error_email(token, receiver,
                                                   subject, message)
                    else:
                        # If we do assert that the HTTP code was 200
                        Log(line='Success', api=api,
                            endpoint=endpoint, timestamp=now).save()
    except:
        # If we fail to load the config file
        raise

def send_assertion_error_email(token, receiver, subject, message):
    api_data = {
        'token': token,
        'message': {
            'to': receiver,
            'subject': subject,
            'body': message
        }
    }
    requests.post('http://email.devnup.com/api/gateway/send', json=api_data)

if __name__ == "__main__":
    main()
