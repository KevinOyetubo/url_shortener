import string
import secrets

from sqlalchemy.orm import Session

def generate_key(lenght: int = 5):
    characters = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(characters) for _ in range(lenght))

def generate_unique_key(db: Session):
    key = generate_key()
    from crud import get_url_by_key
    while get_url_by_key(key, db):
        key = generate_key
    return key