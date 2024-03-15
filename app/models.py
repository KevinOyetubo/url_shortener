from sqlalchemy import Column, String, Integer, Boolean
import sqlalchemy as sa

from database import Base 

class URL(Base):
    __tablename__ = "urls" 

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    original_url = Column(String)
    is_active = Column(Boolean, server_default=sa.literal(True))
    qr_code_path = Column(String)
    clicks = Column(Integer, server_default=sa.literal(0))