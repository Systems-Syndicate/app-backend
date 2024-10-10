# Welcome to the KnightAPI

This API serves as the backbones of our project and is used to allow communication between the NFC scanners and the front-end via API calls. It also serves as the database to store user calendars.

> `main.py` is `@cybrsucks`'s project, have a look,
> it shows the interaction between Google API.

## To run:

### Docker

If you have docker, In `api` (the directory that has the Dockerfile 😊), just do:

- `docker build -t test .`
- `docker run -d -p 80:3801 test`

or run the shell script:

`./run.sh`

> This is the only way for the API server to run on your local WiFi idk why...

This will run locally on: `localhost`, to test if the server is running try: `localhost/health`.

### Manual

Install python and pip

(Ubuntu/WSL)

- `sudo apt-get update && apt-get install -y python3 python3-pip wget`

(MacOS)

- `brew update && brew install python3 wget`
- `python3 -m pip install --upgrade pip`

Install poetry

- `pip3 install poetry icalendar flask flask_sqlalchemy ics flask-cors`

- `poetry install --no-root`

In the `api` directory, run:

- `poetry run flask --app app run -p {number} --debug`

This will run locally on: `localhost:{number:4 digit}`

To test if the server is running try: `localhost{number: digit}/health`
