from sqlalchemy.orm import Session
import schemas
import models

def obtener_usuarios(db: Session):
    return db.query(models.Usuario).all()

def obtener_usuario_por_email(email: str, db: Session):
    return db.query(models.Usuario) \
    .filter(models.Usuario.email == email) \
    .first()


def registrar_usuario(usuario_front: schemas.UsuarioRegistro, db: Session):
    db_usuario = models.Usuario(
        email = usuario_front.email,
        password = usuario_front.password,
        role = usuario_front.role,
        name = usuario_front.name,
        register_date = usuario_front.register_date,
        status = usuario_front.status
    )

    try:
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    except Exception as e:
        db.rollback()
        raise Exception(f'el error es este {e}')

def loggear_usuario(usuario_front: schemas.UsuarioLogin, db: Session):
    usuario_db_encontrado = db.query(models.Usuario) \
    .filter(models.Usuario.email == usuario_front.email) \
    .first()

    if not usuario_db_encontrado:
        return f"no existe cuenta con este correo: {usuario_front.email}"
    if usuario_db_encontrado.status == "0":
        return f'Esta cuenta esta deshabilitada'
    if usuario_db_encontrado.password != usuario_front.password:
            return f'Contraseña incorrecta'

    return usuario_db_encontrado

def actualizar_usuario(usuario_front: schemas.UsuarioActualizar, db: Session):
    usuario_db_encontrado = db.query(models.Usuario) \
    .filter(models.Usuario.email == usuario_front.email) \
    .first()

    if not usuario_db_encontrado:
        return f"no existe cuenta con este correo: {usuario_front.email}"


    if (usuario_front.name):
        usuario_db_encontrado.name = usuario_front.name
    if (usuario_front.password):
        usuario_db_encontrado.password = usuario_front.password
    if (usuario_front.cellphone):
        usuario_db_encontrado.cellphone = usuario_front.cellphone
    if (usuario_front.city):
        usuario_db_encontrado.city = usuario_front.city
    if (usuario_front.house_number):
        usuario_db_encontrado.house_number = usuario_front.house_number
    if (usuario_front.postal_code):
        usuario_db_encontrado.postal_code = usuario_front.postal_code
    if (usuario_front.social_media):
        usuario_db_encontrado.social_media = usuario_front.social_media
    if (usuario_front.suburb):
        usuario_db_encontrado.suburb = usuario_front.suburb
    if (usuario_front.street):
        usuario_db_encontrado.street = usuario_front.street
    if (usuario_front.birth_date):
        usuario_db_encontrado.birth_date = usuario_front.birth_date
    if (usuario_front.state):
        usuario_db_encontrado.state = usuario_front.state
    
    try:
        db.commit()
        db.refresh(usuario_db_encontrado)
        return usuario_db_encontrado
    except Exception as e:
        db.rollback()
        raise Exception(f'el error es este {e}')


def eliminar_usuario(email: str, db: Session):
    usuario_db_encontrado = db.query(models.Usuario) \
    .filter(models.Usuario.email == email) \
    .first()

    if not usuario_db_encontrado:
        return f"no existe cuenta con este correo: {email}"

    usuario_db_encontrado.status = False

    try:
        db.commit()
        db.refresh(usuario_db_encontrado)
        return f'Usuario eliminado'
    except Exception as e:
        db.rollback()
        raise Exception(f'el error es este {e}')


    
    



