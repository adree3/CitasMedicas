from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from app import schemas
from app.schemas import Medico
from app.db.database import get_db
from app import models
from app.exceptions import NotFoundException
from app.security import get_current_user

router = APIRouter(
    prefix="/medico",
    tags=["Medico"]
)

@router.get("/", summary="Obtener medicos")
def getMedicos(db:Session=Depends(get_db)):
    """
    Obtener todos los medicos
    """
    data = db.query(models.Medico).all()
    
    resultado = [
        {
            "id": item.id,
            "nombre ": item.nombre,
            "especialidad": item.especialidad,
            "horario": item.horario,
        }
        for item in data
    ]
    return resultado

@router.get("/buscar", summary="Obtener medicos por su especialidad")
def getMedicosPorEspecialidad(
    especialidad: str = Query(..., description="Especialidad a buscar", min_length=1),
    db: Session = Depends(get_db)
):
    """
    Filtra los medicos por la especialidad indicada. (cardiologia)
    """
    data = db.query(models.Medico).filter(
        func.trim(func.lower(models.Medico.especialidad)) == func.lower(func.trim(especialidad))
    ).all()

    resultado = [
        {
            "id": item.id,
            "nombre": item.nombre,
            "especialidad": item.especialidad,
            "horario": item.horario,
        }
        for item in data
    ]
    return resultado

@router.post("/crearMedico", summary="Crear médico")
def crearMedico(medico: Medico, db: Session = Depends(get_db)):
    """
    Crea un medico por los atributos indicados
    """
    newMedico = models.Medico(
        nombre=medico.nombre,
        especialidad=medico.especialidad,
        horario=medico.horario,
    )
    db.add(newMedico)
    db.commit()
    db.refresh(newMedico)
    return {"Respuesta": "Medico creado"}

@router.put("/actualizar/{id}", summary="Actualizar médico")
def actualizarMedico(id: int, medico: schemas.Medico, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """
    Actualiza el medico indicado por el id, con los atributos recibidos.
    Necesita auntenticación JWT
    """
    medico_db = db.query(models.Medico).filter(models.Medico.id == id).first() 
    if medico_db is None:
        raise NotFoundException(detail="No existe ese medico")

    medico_db.nombre = medico.nombre
    medico_db.especialidad = medico.especialidad
    medico_db.horario = medico.horario

    db.commit() 
    db.refresh(medico_db)  

    return {"mensaje": "Medico actualizado"}


@router.delete("/eliminar/{id}", summary="Eliminar un médico")
def eliminarMedico(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)): 
    """
    Elimina el medico indicado por el id.
    Necesita auntenticación JWT
    """
    medico = db.query(models.Medico).filter(models.Medico.id == id).first()
    if medico is None:
        raise NotFoundException(detail="No existe ese medico")

    db.delete(medico)
    db.commit()
    return {"mensaje": "Medico eliminado"}