# InvestorPro DataOps

## Overview

This guide will walk you through the InvestorPro DataOps semi-project. To effectively use this project, you'll need:

1. **TASE HUB API Account**: This is the Israeli stock market API used in this project. You can also choose any other API, but remember to update the API calls accordingly.
2. **Postgres Instance on GCP**: This will serve as our database for the project.
3. **Docker & Airflow**: We use Airflow for running our ETL processes, and Docker to containerize the environment.

## Project Structure

After cloning the InvestorPro project to your local machine, you will find the two main folders we will use for the DataOps part :

- **`dataOps-dev`**: This is our development environment. It is used for testing and manually performing operations against the TASE HUB API and the database.

- **`airflow`**: This folder contains our production environment. It includes all the ETL processes required to supply the application with necessary data.


## dataOps-dev 
### set up the environment
In order to work with the development environment, lets start with creating our virtual env,
open a terminal and go to the dataOps_dev folder (or you can create the virtual env wherever you want...) and run the following command: 
1. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

2. **Activate the virtual environment:**
    ```bash
    source venv/bin/activate
    ```

3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Configure Database Credentials
Since we need to push data to the database, you'll have to configure your credentials. We use system environment variables for this purpose, but you can choose any other method if you prefer.
the only function we need those credential for is the getconn function located in the dataOps_dev/UTILS/utils.py
```python
def getconn() -> pg8000.Connection:
    conn: pg8000.Connection = pg8000.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME'),
        host=os.getenv('DB_HOST'),
    )
    return conn
```

 


## Airflow

### Set Up and Start Airflow

**Build the Docker Airflow Image:**

1. **Make sure Docker is running on your machine.**

2. **Open a terminal in the `airflow` folder and run:**
   ```bash
    docker-compose up --build
   ```
After a few moments and some logs in the terminal (without any errors I hope), you should be able to log in at: http://localhost:8080/home and see the Airflow Home screen UI.

**Set up the connection to Postgres**

Go to Admin->connection in the top bar, and add a new gcpcloudsqldb type connection with the Conn Id : investor_pro, there you will have to list the DB host, and the DB port   

### airflow Dags 
for this project, we created 3 dags, each has its one responsibility:
1. tase_stock_extract -> This dag extract data from the TASE_API and store it into the database.
2. tase_stock_stats -> This dag extract stock data from the database, calculates statistics for each stock and save the statistics into the database.
3. tase_stock_predict -> This dag extract stock data from both the database and the TASE_API(since we didn't want to save so much data into the database) and run a closing price prediction on each stock using a XGBRegressor, after the preidiction where made, it stores it into the database as well.


## thanks for reading! and have a great coding day :) ##

