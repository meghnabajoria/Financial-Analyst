FROM python:3.9.18

# Set the working directory in the container
WORKDIR /app

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y wget unzip && \
    rm -rf /var/lib/apt/lists/*

# Download and install Chromedriver
RUN wget https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.128/win64/chromedriver-win64.zip && \
    ls \ 
    unzip chromedriver-win64.zip && \
    mv chromedriver.exe /usr/local/bin/ && \
    rm chromedriver-win64.zip

# Download and install Chrome
RUN wget https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.128/win64/chrome-win64.zip && \
    unzip chrome-win64.zip && \
    mv chrome-win64/* /usr/local/bin/ && \
    rm -rf chrome-win64.zip chrome-win64

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the Flask application
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 server:app
