from GCD_SETUP.gcp_setup import get_pool
from datetime import datetime
import hashlib
from sqlalchemy import text
from sqlalchemy.exc import InterfaceError


class UserDatabaseManager:

    _instance = None
    table_name = 'server.users'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def is_username_exists(self, username: str):
        try:
            engine = get_pool()
            with engine.connect() as conn:
                query = text(f"SELECT COUNT(*) FROM {self.table_name} WHERE user_id = '{username}'")
                result = conn.execute(query)
                exists = result.scalar() > 0
                return exists
        except InterfaceError:
            return None
        except Exception:
            return None

    def hash_password(self, password: str):
        # Hash the password using SHA-256
        return hashlib.sha256(password.encode()).hexdigest()

    def load_new_user_to_database(self, username: str, password: str, email_address: str):

        hash_pass = self.hash_password(password=password)
        try:
            engine = get_pool()
            with engine.connect() as conn:
                insert_query = text(
                    f"""
                    INSERT INTO {self.table_name} (user_id,
                                                    hash_pass,
                                                    email_address,
                                                    install_date,
                                                    creation_date,
                                                    update_date)
                    VALUES ('{username}','{hash_pass}','{email_address}','{datetime.now()}','{datetime.now()}','{datetime.now()}' )
    
                    """
                )
                conn.execute(insert_query)
                conn.commit()
                return 1
        except InterfaceError:
            return -1
        except Exception:
            return -1

    def get_all_users_info(self):
        try:
            engine = get_pool()
            with engine.connect() as conn:
                result = conn.execute(
                    text(f'SELECT * FROM {self.table_name}'))  # Use conn.execute instead of engine.execute
                return result.fetchall()
        except InterfaceError:
            return 1
        except Exception:
            return 2

    def authenticate_user_password(self, username: str, password: str):
        # given user name exists
        try:
            engine = get_pool()
            with engine.connect() as conn:
                hash_pass = self.hash_password(password)
                query = text(f"SELECT COUNT(*) FROM {self.table_name} WHERE user_id = '{username}'"
                             f" AND hash_pass = '{hash_pass}'")
                result = conn.execute(query)
                exists = result.scalar() > 0
                return exists
        except Exception:
            return None
    def change_password(self, username: str, password: str):
        # given user name exists
        engine = get_pool()
        with engine.connect() as conn:
            query = text(f"UPDATE {self.table_name} SET hash_pass = '{password}' WHERE user_id = '{username}'")
            print(query)
            result = conn.execute(query)
            conn.commit()
