# Set a base image that includes Lambda Runtime API
FROM amazon/aws-lambda-python:3.11

# Optional: ensure that pip is up to date
RUN pip install --upgrade pip

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy function code
COPY src/ .

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "main.handler" ]
