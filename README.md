# Welcome to the KnightAPI

This API serves as the backbones of our project and is used to allow communication between the NFC scanners and the front-end via API calls. It also serves as the database to store user calendars.

> `main.py` is `@cybrsucks`'s project, have a look,
> as it shows the interaction between Google API.

## To run:

### Docker

If you have docker, In `api` (the directory that has the Dockerfile 😊), just do:

- `docker build -t test .`
- `docker run -d -p 80:3801 test`

This will run locally on: `localhost`, to test if the server is running try: `localhost/health`.

### Manual

Install python and pip

- `sudo apt-get update && apt-get install -y python3 python3-pip wget`

Install poetry

- `pip3 install poetry`

- `poetry install --no-root`

In the `app` directory, run:

- `poetry run flask --app app run -p {number} --debug`

This will run locally on: `localhost:{number}`

To test if the server is running try: `localhost{number}/health`
