from sqlalchemy import Column, Integer, String, JSON, DateTime, func, Float
from database import Base
from pgvector.sqlalchemy import Vector

class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    asin = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    url = Column(String, index=True)
    price = Column(Float, index=True)
    description = Column(String)
    json_scraped = Column(JSON)
    summary = Column(String)
    vector = Column(Vector(768))
    created_in = Column(DateTime(timezone=True), server_default=func.now())
    updated_in = Column(DateTime(timezone=True), onupdate=func.now())
