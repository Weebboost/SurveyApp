import random
import string
from app.models.user import User, UserCreate
from datetime import datetime, timezone
from app.core.password_utils import hash_password

def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_string() -> str:
    return "".join(random.choices(string.ascii_letters, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com" 


email = random_email()
password = random_string()
userCreate = UserCreate(email=email, password=password)