import os
from sqlalchemy import text
import pg8000
import sqlalchemy


############################################################################
def getconn() -> pg8000.Connection:
    """
    Establishes and returns a connection to the PostgreSQL database using pg8000.

    This function connects to the PostgreSQL database using credentials and configuration details
    obtained from environment variables. The connection is established using the pg8000 library.

    Returns:
        pg8000.Connection: A connection object to the PostgreSQL database.

    """
    conn: pg8000.Connection = pg8000.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME'),
        host=os.getenv('DB_HOST'),
    )
    return conn

def get_pool():
    """
    Creates and returns a SQLAlchemy engine for connecting to a PostgreSQL database using pg8000.

    This function sets up a SQLAlchemy engine configured to connect to a PostgreSQL database. The engine
    is created using the pg8000 library as the database driver. Connection details are obtained from
    environment variables.

    Returns:
        sqlalchemy.engine.Engine: A SQLAlchemy engine instance configured for PostgreSQL.

    """
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASS')
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')
    pool = sqlalchemy.create_engine(
        f"postgresql+pg8000://{db_user}:{db_pass}@{db_host}/{db_name}",
        creator=getconn,
        future=True
        # Additional options if needed
    )
    return pool


def get_all_records_from_table(table_name):
    engine = get_pool()
    with engine.connect() as conn:
        result = conn.execute(text(f'SELECT * FROM {table_name}'))  # Use conn.execute instead of engine.execute
        return result.fetchall()


if __name__ == '__main__':
    print("db host:", os.getenv('DB_HOST'))
    print("db name:", os.getenv('DB_NAME'))
    print("db pass:", os.getenv('DB_PASS'))
    print("db user:", os.getenv('DB_USER'))
    print("INSTANCE_CONNECTION_NAME:", os.getenv('INSTANCE_CONNECTION_NAME'))
