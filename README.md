# Welcome to Day 'n Knight
Day 'n Knight is a chessboard scheduling device, created by Systems Syndicate for DECO3801, Semester 2 2024. The project consists of two key parts, the chessboard device and the companion mobile application. The hardware uses NFC tags to distinguish between different users and display the corresponding users schedule on the chessboard. Overall, the aim of the project was to improve social connectedness and promote social spontaneity, whilst disgusing the device in an ambient way within the home.

## Table of Contents

## Running Day 'n Knight
To run Day 'n Knight, you will need the following devices:
- 1 tablet device (e.g. iPad, Android Galaxy Fold) for the chessboard with Expo Go application downloaded
- 1 computer to host the back-end and chessboard front-end
- 1 smartphone (to simulate a household member) with Expo Go application downloaded
- 1 NFC chip, attached to a chess piece

To begin, ensure all devices are connected to the same network (e.g. connect to a hotspot) - this allows all devices to connect to the IP address hosted on the computer.

The computer will be running multiple terminal sessions to run the back-end and front-end operations (chessboard and mobile phone).

### Starting the Back-End Server
On the computer, open a new terminal and run the following commands:

`cd app-back-end`

`cd api`

`poetry run flask --app app run -p 3801 --debug --host=0.0.0.0`

This will run locally on: `localhost:{number:4 digit}`

To test if the server is running try: `localhost{number: digit}/health`

### Starting the Front-End Chessboard
On the computer, open another terminal and run the following commands:

`cd frontend`

`cd chessboard`

`npx expo start` 

On the tablet device, scan the QR code generated in the terminal to open the app in Expo Go.

### Starting the Front-End Mobile App
On the computer, open another terminal and run the following commands:

`cd frontend`

`cd phone`

`npx expo start` 

If this is taking too long to run, try: `npx expo start --tunnel`

On the tablet device, scan the QR code generated in the terminal to open the app in Expo Go.

The system is now ready to be run.

## Code Structure
### Back-End
The back-end code consists of the API and the endpoints to write to the iCalendar files, which is backed up on an SQLAlchemy database. The code is organised into two sub-directories, `models` (containing the setup code for the database) and `views` (containing the endpoints to write to the iCalendar files).

Links to these files can be found here:
- [init.py](app-back-end\\api\\app\\__init__.py): initialises the database tables
- [views/routes.py](app-back-end\api\app\views\routes.py): contains the code to create/edit/delete calendar events, save to the iCalendar file, and retrieve users based on their NFC id
- [models/tables.py](app-back-end\api\app\models\tables.py): creates the columns for the database

### Front-End Chessboard
The front-end chessboard contains multilple different interfaces, one for the actual chessboard display and one for the calendar display. The chessboard is best viewed when run on a tablet or an Android Galaxy Fold and then can be connected to an external monitor via a HDMI cable.

Links to the important files can be found here:
- [components/chessboard.tsx](frontend\chessboard\components\Chessboard.tsx): 
- [co]

### Front-End Phone






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
