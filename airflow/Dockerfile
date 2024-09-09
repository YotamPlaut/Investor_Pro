# Use the Airflow base image with Python 3.9
FROM apache/airflow:2.5.1-python3.9

# Copy the requirements file into the container
COPY requirements.txt /requirements.txt

# Install Python packages from the requirements file
RUN pip install --no-cache-dir -r /requirements.txt