#! python3.4
# -*- encoding: utf-8 -*-
from os import path
import dumbyaml as yaml
import requests


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
            assert request.status_code == 200
    except:
        raise
if __name__ == "__main__":
    main()
