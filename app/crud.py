from sqlalchemy.orm import Session
from models import URL
from schemas import URLBase, ShowURL, CustomURL
from utilities import raise_bad_request, generate_qrcode
from keygen import generate_unique_key

import validators
from cachetools import TTLCache
 
cache = TTLCache(maxsize=100, ttl=600)

def get_url_by_key(url_key: str, db: Session):
    if url_key in cache:
        return cache[url_key] 
    db_query = db.query(URL).filter(url_key == URL.key).first()
    if db_query:
        cache[url_key] = db_query
    return db_query

def create_db_url(original_url: str, db: Session):
    if not validators.url(original_url):
        return None
    short_url = URL(key = generate_unique_key(db=db), original_url = original_url)
    qr_code_path = generate_qrcode(short_url.original_url, short_url.key)
    db_url = URL(key = short_url.key, original_url = short_url.original_url, qr_code_path = qr_code_path)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url
 
def create_custom_db_url(url_original: str, custom_url: str, db: Session):
    if not validators.url(url_original):
        return None
    from crud import get_url_by_key
    if get_url_by_key(custom_url, db):
        return None
    short_url = URL(key = custom_url, original_url = url_original)
    qr_code_path = generate_qrcode(short_url.original_url, short_url.key)
    db_url = URL(key = short_url.key, original_url = short_url.original_url, qr_code_path = qr_code_path)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url




    


def update_clicks(db_url: ShowURL, db: Session):
    db_url.clicks += 1
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def deactiavte_url(key: str, db: Session):
    url = get_url_by_key(key, db)
    if url:
        url.is_active = False
        db.commit()
        db.refresh(url)
    return url