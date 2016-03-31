#! python3.4
# -*- encoding: utf-8 -*-
from os import path
import dumbyaml as yaml
import requests
import json
from datetime import datetime


ERROR_MAIL = """
<p>Hello,</br>
The amazing Quick 'n' Dirty API tester failed to assert that the path</br>
<b>{path}</b> returned a HTTP-200 code.</br>
The test was performed at {datetime}</br></p>
<p>Best of luck,</br>
QNDAPIT<p>
"""

def main():
    try:
        current_dir = path.dirname(__file__)
        config_path = path.join(current_dir, 'config.yaml')
        config = yaml.load(open(config_path).read())

        apis = config['APIs']

        for api in apis.keys():
            endpoints = [str(api) + str(endpoint)
                         for endpoint in list(apis[api])]

        for endpoint in endpoints:
            request = requests.get(endpoint)
            try:
                assert request.status_code == 200
            except AssertionError:
                now = datetime.now().strftime("%d/%m/%Y @ %Hh%mmin")
                message = ERROR_MAIL.format(path=endpoint, datetime=now)
                subject = "QNDAPIT Error!"
                receiver = str(config['email']['receiver'])
                driver = str(config['email']['driver'])

                if driver == 'devnup-email':
                    api_data = {
                        'token': str(config['email']['token']),
                        'message': {
                            'to': receiver,
                            'subject': subject,
                            'body': message
                        }
                    }
                    requests.post('http://email.devnup.com/api/gateway/send',
                                  data=json.dumps(api_data))
    except:
        raise


if __name__ == "__main__":
    main()
