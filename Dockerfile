FROM python:3.9

# Set the working directory
WORKDIR /anp-code

# Environment variables from .env file
ENV AWS_ACCESS_KEY_ID = ${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY = ${AWS_SECRET_ACCESS_KEY}
ENV SLACK_TOKEN = ${SLACK_TOKEN}
ENV ANP_LOAD_URI = ${ANP_LOAD_URI}

# Copy the project source code from the local host to the filesystem of the container at the working directory
COPY . .

# Install requirements.txt
RUN pip3 install -r requirements.txt
 
# Run the crawler when the container launches
CMD ["python3", "./trigger_anp_crawler.py"]