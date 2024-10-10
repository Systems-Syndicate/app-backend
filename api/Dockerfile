# Use Python 3.12 base image
FROM python:3.12-slim

# Installing dependencies
RUN apt-get update && apt-get install -y wget

# Install poetry and other Python packages
RUN pip install poetry icalendar flask flask_sqlalchemy ics flask-cors

# Setting the working directory
WORKDIR /app

# Install dependencies using poetry
COPY pyproject.toml ./ 
RUN poetry install --no-root
RUN poetry add flask-cors icalendar ics flask_sqlalchemy

# Copy application files
COPY app app

# Running the application
CMD ["poetry", "run", "flask", "--app", "app", "run", "--host=0.0.0.0", "--port", "3801", "--debug"]
