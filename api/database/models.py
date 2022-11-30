from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Integer, ForeignKey


Base = declarative_base()

class Brand(Base):
    __tablename__ = "brand_table"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Product(Base):
    __tablename__ = "product_table"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    views = Column(Integer)
    brand = Column(Integer, ForeignKey("brand_table.id"))


class Review(Base):
    __tablename__ = "review_table"

    id = Column(Integer, primary_key=True)
    body = Column(String)
    rating = Column(Integer)
    product = Column(Integer, ForeignKey("product_table.id"))
