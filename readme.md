# Quick 'n' Dirty API Tester

This gotta be the simplest and easiest API tester in the market.
Quite simply, you just add a bunch of APIs' addresses and some endpoints in the `config.yaml` file. The program will then loop through all of them, try to connect to them, check if the endpoint returned an HTTP-200. If anything goes wrong, it shoots an email.
Very useful to use with a `cron` job to test periodically.
Unfortunately, it is not use-ready just yet. The whole email sending thing is non functional as I'm using an internal API of mine to do the job. I'll allow for SMTP soon.

## Installing
1. Git clone the repo
2. `cd` into the folder
3. Start a virtual environment with Python 3.4. `virtualenv -p python3.4 venv`
4. Activate the env `source \folder-you-cloned-the-repo\venv\bin\activate`
5. Install the requirements `pip -r requirements.txt`
6. Copy the `config.sample.yaml` file to `config.yaml`
7. Edit the `config.yaml` file for your needs

## Usage
Well you can just run the code manually. Being with the virtualenvironment set just run `python qndapi.py`
You can also set up a cron job. Keep in mind that you'll **have to reference to the Python binary inside the virtual environment!**
Your cron command should be something like: `/path-to-qndapi/venv/bin/python /path-to-qndapi/qndapi.py`

## Contributing
Open issues, open PRs, talk to me. The basics. Contributors welcome!

## Licensing
MIT

Copyright © 2016 Felipe 'Bidu' Rodrigues

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

