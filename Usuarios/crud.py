from sqlalchemy.orm import Session
from fastapi import HTTPException
from utils import hash_password, verify_password
import schemas
import models
from auth import create_access_token

def obtener_usuarios(db: Session):
    return db.query(models.Usuario).all()

def obtener_usuario_por_email(email: str, db: Session):
    return db.query(models.Usuario)\
        .filter(models.Usuario.email == email)\
        .first()

def registrar_usuario(usuario_front: schemas.UsuarioRegistro, db: Session):
    try:
        existing_user = obtener_usuario_por_email(usuario_front.email, db)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email ya registrado")
            
        hashed_password = hash_password(usuario_front.password)
        db_usuario = models.Usuario(
            email=usuario_front.email,
            password=hashed_password,
            role=usuario_front.role,
            name=usuario_front.name,
            register_date=usuario_front.register_date,
            status=usuario_front.status
        )
        
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def loggear_usuario(usuario_front: schemas.UsuarioLogin, db: Session):
    usuario_db_encontrado = db.query(models.Usuario)\
        .filter(models.Usuario.email == usuario_front.email)\
        .first()

    if not usuario_db_encontrado:
        raise HTTPException(
            status_code=404,
            detail=f"No existe cuenta con este correo: {usuario_front.email}"
        )
    
    if usuario_db_encontrado.status == "false":
        raise HTTPException(
            status_code=403,
            detail="Esta cuenta está deshabilitada"
        )
    
    if not verify_password(usuario_front.password, usuario_db_encontrado.password):
        raise HTTPException(
            status_code=401,
            detail="Contraseña incorrecta"
        )

    # Generar el token
    access_token = create_access_token(
        data={"sub": usuario_db_encontrado.email}
    )
    
    # Devolver respuesta con token y datos del usuario
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "email": usuario_db_encontrado.email,
            "name": usuario_db_encontrado.name,
            "role": usuario_db_encontrado.role
        }
    }
def actualizar_usuario(usuario_front: schemas.UsuarioActualizar, db: Session):
    try:
        usuario_db_encontrado = db.query(models.Usuario)\
            .filter(models.Usuario.email == usuario_front.email)\
            .first()

        if not usuario_db_encontrado:
            raise HTTPException(
                status_code=404,
                detail=f"No existe cuenta con este correo: {usuario_front.email}"
            )

        if usuario_front.password:
            usuario_db_encontrado.password = hash_password(usuario_front.password)
        if usuario_front.name:
            usuario_db_encontrado.name = usuario_front.name
        if usuario_front.birth_date:
            usuario_db_encontrado.birth_date = usuario_front.birth_date
        if usuario_front.cellphone:
            usuario_db_encontrado.cellphone = usuario_front.cellphone
        if usuario_front.street:
            usuario_db_encontrado.street = usuario_front.street
        if usuario_front.house_number:
            usuario_db_encontrado.house_number = usuario_front.house_number
        if usuario_front.suburb:
            usuario_db_encontrado.suburb = usuario_front.suburb
        if usuario_front.city:
            usuario_db_encontrado.city = usuario_front.city
        if usuario_front.state:
            usuario_db_encontrado.state = usuario_front.state
        if usuario_front.postal_code:
            usuario_db_encontrado.postal_code = usuario_front.postal_code
        if usuario_front.social_media:
            usuario_db_encontrado.social_media = usuario_front.social_media

        db.commit()
        db.refresh(usuario_db_encontrado)
        return usuario_db_encontrado

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def eliminar_usuario(email: str, db: Session):
    try:
        usuario_db_encontrado = db.query(models.Usuario)\
            .filter(models.Usuario.email == email)\
            .first()

        if not usuario_db_encontrado:
            raise HTTPException(
                status_code=404,
                detail=f"No existe cuenta con este correo: {email}"
            )

        # Asegurarnos que el status sea el formato correcto
        usuario_db_encontrado.status = "false"  # o "0" dependiendo de tu esquema

        try:
            db.commit()  # Guardar los cambios
            db.refresh(usuario_db_encontrado)  # Refrescar el objeto
            
            # Verificar que el cambio se realizó
            print(f"Status actualizado a: {usuario_db_encontrado.status}")
            
            return {
                "message": "Usuario desactivado exitosamente",
                "status": usuario_db_encontrado.status
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al guardar en la base de datos: {str(e)}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )
    
def recuperar_usuario(email: str, db: Session):
    try:
        usuario_db_encontrado = db.query(models.Usuario)\
            .filter(models.Usuario.email == email)\
            .first()

        if not usuario_db_encontrado:
            raise HTTPException(
                status_code=404,
                detail=f"No existe cuenta con este \
                    correo en el historial: {email}"
            )

        # Asegurarnos que el status sea el formato correcto
        usuario_db_encontrado.status = "true"  

        try:
            db.commit()  # Guardar los cambios
            db.refresh(usuario_db_encontrado)  # Refrescar el objeto
            
            # Verificar que el cambio se realizó
            print(f"Status actualizado a: {usuario_db_encontrado.status}")
            
            return {
                "message": "Usuario reactivado exitosamente",
                "status": usuario_db_encontrado.status
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al guardar en la base de datos: {str(e)}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )