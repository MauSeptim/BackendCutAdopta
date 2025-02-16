from fastapi import FastAPI, Depends, middleware
from sqlalchemy.orm import Session
from database import get_db
from fastapi.middleware.cors import CORSMiddleware
import crud
import schemas

app = FastAPI()
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

@app.post("/crear_usuario")
def crear_usuario(usuario_front: schemas.UsuarioRegistro, db: Session = Depends(get_db)):
    if (usuario_front.password != usuario_front.confirm_password):
        return "Las contraseñas no coinciden"

    return crud.registrar_usuario(usuario_front, db)

@app.post("/login")
def login(usuario_front: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    return crud.loggear_usuario(usuario_front, db)

@app.post("/actualizar_usuario")
def actualizar_usuario(usuario_front: schemas.UsuarioActualizar, db: Session = Depends(get_db)):
    return crud.actualizar_usuario(usuario_front, db)

@app.get("/usuarios")
def obtener_usuarios(db: Session = Depends(get_db)):
    return crud.obtener_usuarios(db)

@app.get("/usuario/{email}")
def obtener_usuario_por_email(email: str, db: Session = Depends(get_db)):
    return crud.obtener_usuario_por_email(email, db)

@app.post("/eliminar_usuario/{email}")
def eliminar_usuario(email: str, db: Session = Depends(get_db)):
    return crud.eliminar_usuario(email, db)