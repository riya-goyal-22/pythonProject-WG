import email_validator
from email_validator import EmailNotValidError
import re
from typing import List,Dict

class Validator:
    @staticmethod
    def validate_required_fields(dict,list: List[str])->bool:
        for field in list:
            if field not in dict:
                return False

        return True

    @staticmethod
    def is_valid_email(email: str):
        try:
            email_validator.validate_email(email)
            return True

        except EmailNotValidError as e:
            return False

    @staticmethod
    def is_valid_password(password):
        # Check for minimum length
        if len(password) < 8:
            return False

        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            return False

        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password):
            return False

        # Check for at least one digit
        if not re.search(r'[0-9]', password):
            return False

        # Check for at least one special character
        if not re.search(r'[@#$%^&+=]', password):
            return False

        # Check if password contains common passwords
        common_passwords = ['password', '123456']
        if password.lower() in common_passwords:
            return False

        # If all checks pass, the password is valid
        return True


    @staticmethod
    def validate_phone_no(phone_no: str)->bool:
        # Remove all non-digit characters from the phone number
        cleaned_number = ''.join(char for char in phone_no if char.isdigit())

        # Check if the length matches the expected length
        if len(cleaned_number) == 10:
            return True
        else:
            return False


