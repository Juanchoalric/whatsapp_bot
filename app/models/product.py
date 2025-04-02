from sqlalchemy import Column, Integer, String, Float, Text
from app.database.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    image_url = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<Product {self.name}>" 