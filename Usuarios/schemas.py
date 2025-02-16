from pydantic import BaseModel
from typing import Optional

class UsuarioRegistro(BaseModel):
    id: Optional[int] = None
    email: str
    password: str
    confirm_password: str
    role: str
    register_date: str
    name: str
    status: str

class UsuarioLogin(BaseModel):
    email: str
    password: str

class UsuarioActualizar(BaseModel):

    password: Optional[str] = None
    name: Optional[str] = None
    birth_date: Optional[str] = None
    cellphone: Optional[int] = None
    street: Optional[str] = None
    house_number: Optional[str] = None
    suburb: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    social_media: Optional[str] = None