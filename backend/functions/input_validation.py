import re


class InputValidator:

    @staticmethod
    def is_valid_email_address(email_address: str):
        pattern = r'^[^@]+@[^@]+\.[^@]+$'
        return isinstance(email_address, str) and re.match(pattern, email_address)

    @staticmethod
    def is_valid_username(username: str) -> str:
        return ""
