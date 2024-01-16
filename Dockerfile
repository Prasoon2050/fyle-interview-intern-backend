# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the contents of the local src directory to the working directory
COPY . .

# Create and activate a virtual environment
RUN python3 -m venv env
RUN . env/bin/activate

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Reset DB and apply migrations
ENV FLASK_APP=core/server.py
RUN rm core/store.sqlite3
RUN flask db upgrade -d core/migrations/

# Make port 7755 available to the world outside this container
EXPOSE 7755

# Run your script
CMD ["./run.sh"]
