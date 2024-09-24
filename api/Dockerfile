FROM ubuntu:22.04
# Installing dependencies for running a python application
RUN apt-get update && apt-get install -y python3 python3-pip wget
# Install pipenv
RUN pip3 install poetry icalendar flask flask_sqlalchemy ics flask-cors
# Setting the working directory
WORKDIR /app
# Install pipenv dependencies
COPY pyproject.toml ./
RUN poetry install --no-root
# Copying our application into the container
COPY app app

# Running our application
CMD ["poetry", "run", "flask", "--app", "app", "run", "--host=0.0.0.0", "--port", "3801", "--debug"]
