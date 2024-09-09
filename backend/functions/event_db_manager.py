import json
import warnings
from GCD_SETUP.gcp_setup import get_pool
from datetime import datetime
from sqlalchemy import text


class EventDatabaseManager:

    _instance = None
    table_name = 'server.raw_actions'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def insert_raw_action(self, evt_name: str, server_time: datetime, user_id: str, evt_details: dict = None):
        """
        Inserts a raw action record into the database.

        :param user_id: user id- needs to be from server.users!
        :param evt_name: Name of the event.
        :param server_time: Timestamp representing the time when the event occurred on the server.
        :param evt_details: Additional details about the event, stored as a dictionary. Defaults to None.

        :return: A dictionary containing a code and a message indicating the result of the insertion operation.
            - 'code' (int): Indicates the status of the insertion operation. 1 indicates success, while None indicates an error occurred.
            - 'msg' (str): A message describing the outcome of the insertion operation. If successful, it indicates that the action was listed in the database.
        """
        if evt_details is None:
            evt_details = {}  # Set evt_details to an empty dictionary if None

        server_time_str = server_time.isoformat()

        # Convert evt_details to a JSON string
        evt_details_str = json.dumps(evt_details)

        try:
            insert_query = f"""
                INSERT INTO {self.table_name} (evt_date, evt_time, evt_name, server_time, evt_details, user_id)
                VALUES ('{datetime.now().date()}', '{datetime.now()}', '{evt_name}', '{server_time_str}', '{evt_details_str}' ,'{user_id}')
            """

            engine = get_pool()
            with engine.connect() as conn:
                with warnings.catch_warnings():
                    # warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                    conn.execute(text(insert_query))
                    conn.commit()
                return {'code': 1, 'msg': f"Action listed in db"}
        except Exception as e:
            print("Error occurred while running insert query:", e)
            return None

    def get_all_events(self):
        engine = get_pool()
        with engine.connect() as conn:
            result = conn.execute(
                text(f'SELECT * FROM {self.table_name}'))  # Use conn.execute instead of engine.execute
            return result.fetchall()
