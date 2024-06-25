import random
import string
import re
import phonenumbers

def generate_random_string(length):
    # Derived from https://pynative.com/python-generate-random-string/
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str

def is_valid_email(email):
    # Derived from https://www.zerobounce.net/python-email-verification/

    # Regular expression for validating an Email
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

    # If the string matches the regex, it is a valid email
    if re.match(regex, email):
        return True
    else:
        return False

def is_valid_phone_number(phone):
    return phonenumbers.is_valid_number(phonenumbers.parse(phone, "CA"))

def format_phone_number(phone):
    return phonenumbers.format_number(phonenumbers.parse(phone, "CA"), phonenumbers.PhoneNumberFormat.INTERNATIONAL)