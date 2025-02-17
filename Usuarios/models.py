from sqlalchemy import Column, String, BigInteger, Integer, Date, Text
from passlib.context import CryptContext
from utils import hash_password
from database import Base
from database import engine

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(BigInteger, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(255))
    birth_date = Column(Date)
    cellphone = Column(Integer)
    street = Column(String(255))
    house_number = Column(Integer)
    suburb = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    postal_code = Column(Integer)
    role = Column(String(10), nullable=False)
    register_date = Column(Date, nullable=False)
    status = Column(String(10))
    social_media = Column(Text)

    def set_password(self, password_user: str):
        self.hashed_password = hash_password(password_user)

# Crear las tablas en la BD
Base.metadata.create_all(engine)