from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from fastapi.middleware.cors import CORSMiddleware
from auth import get_current_user
import crud
import schemas
import models
from fastapi.middleware.cors import CORSMiddleware


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
    if usuario_front.password != usuario_front.confirm_password:
        raise HTTPException(status_code=400, detail="Las contraseñas no coinciden")
    return crud.registrar_usuario(usuario_front, db)

@app.post("/login")
def login(usuario_front: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    return crud.loggear_usuario(usuario_front, db)

@app.post("/actualizar_usuario")
def actualizar_usuario(
    usuario_front: schemas.UsuarioActualizar,
    current_user: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.email != usuario_front.email and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para actualizar este usuario"
        )
    return crud.actualizar_usuario(usuario_front, db)

@app.get("/usuarios")
def obtener_usuarios(
    current_user: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Solo los administradores pueden ver todos los usuarios"
        )
    return crud.obtener_usuarios(db)

@app.get("/usuario/{email}")
def obtener_usuario_por_email(
    email: str,
    current_user: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.email != email and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para ver este usuario"
        )
    return crud.obtener_usuario_por_email(email, db)

@app.post("/eliminar_usuario/{email}")
def eliminar_usuario(
    email: str,
    current_user: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Solo los administradores pueden eliminar usuarios"
        )
    return crud.eliminar_usuario(email, db)

@app.post("/recuperar_usuario/{email}")
def recuperar_usuario(
    email: str,
    current_user: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Solo los administradores pueden reactivar usuarios"
        )
    return crud.recuperar_usuario(email, db)