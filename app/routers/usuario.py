from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import Login, Usuario
from app.db.database import get_db
from app import models
from app.utiles import hashearContrasena, comprobarContrasena
from app.security import crear_jwt
router = APIRouter(
    prefix="/usuario",
    tags=["Usuario"]
)

@router.get("/", summary="Obtener usuarios")
def getUsuarios(db: Session = Depends(get_db)):
    """
    Obtiene todos los usuarios
    """
    data = db.query(models.Usuario).all()
    resultado = [
        {
            "id": item.id,
            "nombre": item.nombre,
            "email": item.email,
            "contraseña": item.contrasena,
            "rol": item.rol,
        }
        for item in data
    ]
    return resultado

@router.post("/registrar", summary="Crear usuario")
def registerUsario(usuario: Usuario, db: Session = Depends(get_db)):
    """
    Crear un usuario con los atributos indicados
    """
    hashed_password = hashearContrasena(usuario.contrasena)
    newUser = models.Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        contrasena=hashed_password,
        rol=usuario.rol,
    )
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return {"Respuesta": "Usuario creado"}

@router.post("/login", summary="Loggearse")
def loginUser(login_data: Login, db: Session = Depends(get_db)):
    """
    Inicia sesion con un usuario existente, este te devolvera un token el cual tienes
    que poner en la autentificación
    """
    usuario = db.query(models.Usuario).filter(models.Usuario.email == login_data.email).first()
    
    if usuario and comprobarContrasena(login_data.contrasena, usuario.contrasena):  
        token = crear_jwt(usuario.email)
        return {"access_token": token, "token_type": "bearer"}
    
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")