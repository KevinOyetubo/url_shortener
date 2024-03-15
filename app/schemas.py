from pydantic import BaseModel

class URLBase(BaseModel):
    original_url: str

class CustomURL(URLBase):
    custom_url: str = ""

class ShowURL(URLBase):
    clicks: int
    url: str

    class Config:
        orm_mode: True

class URLInfo(ShowURL):
    is_active: bool
