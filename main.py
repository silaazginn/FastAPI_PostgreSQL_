from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

DATABASE_URL = "postgresql://postgres:1031@localhost:5432/db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    price = Column(Float)
    bedroom = Column(Integer)
    bathroom = Column(Integer)
    reception = Column(Integer)
    size = Column(Float)

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    phone_number = Column(String)
    email = Column(String, unique=True, index=True)
    address = Column(String)

Base.metadata.create_all(bind=engine)

class PropertySchema(BaseModel):
    address: str
    price: float
    bedroom: int
    bathroom: int
    reception: int
    size: float

    class Config:
        from_attributes = True

class ContactSchema(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    address: str

    class Config:
        from_attributes = True

@app.post("/properties/")
def create_property(property: PropertySchema, db: Session = Depends(get_db)):
    db_property = Property(
        address=property.address,
        price=property.price,
        bedroom=property.bedroom,
        bathroom=property.bathroom,
        reception=property.reception,
        size=property.size
    )
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

@app.post("/contacts/")
def create_contact(contact: ContactSchema, db: Session = Depends(get_db)):
    db_contact = Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        phone_number=contact.phone_number,
        email=contact.email,
        address=contact.address
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.get("/properties/")
def get_properties(db: Session = Depends(get_db)):
    return db.query(Property).all()

@app.get("/contacts/")
def get_contacts(db: Session = Depends(get_db)):
    return db.query(Contact).all()
