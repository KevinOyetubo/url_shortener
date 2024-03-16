from fastapi import status, HTTPException
from config import get_settings
from starlette.datastructures import URL
import os
import qrcode

# Functions for errors
def raise_bad_request(message):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

def raise_conflict(message):
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=message)

def raise_not_found(messgae):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messgae)

# Function to get a User-Friendly url_info
def get_info(db_url):
    base_url = URL(get_settings().base_url)
    db_url.url = str(base_url.replace(path=db_url.key))
    return db_url

def generate_qrcode(data, short_url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    qr_code_dir = os.path.join(base_dir, 'static', 'qr_code')

    os.makedirs(qr_code_dir, exist_ok=True)

    qr_code_path = os.path.join(qr_code_dir, f"{short_url}.png")
    qr_img.save(qr_code_path)
    return qr_code_path