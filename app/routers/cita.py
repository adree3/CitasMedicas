from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas
from app.schemas import Cita
from app.db.database import get_db
from app import models
from app.exceptions import NotFoundException
from app.security import get_current_user

router = APIRouter(
    prefix="/cita",
    tags=["Cita"]
)

@router.get("/", summary= "Obtener todas las citas")
def getCitas(db:Session=Depends(get_db)):
    """
    Obtiene todos las citas.
    """
    data = db.query(models.Cita).all()
    
    resultado = [
        {
            "id": item.id,
            "fecha ": item.fecha,
            "estado": item.estado,
            "usuario_id": item.usuario_id,
            "medico_id": item.medico_id,
        }
        for item in data
    ]
    return resultado

@router.get("/fecha/{fecha}", summary="Obtener citas por fecha")
def getCitasPorFecha(fecha: date, db: Session = Depends(get_db)):
    """
    Obtiene todas las citas sobre la fecha indicada.
    Ej (2025-02-21)
    """
    data = db.query(models.Cita).filter(models.Cita.fecha == fecha).all()
    
    if not data:
        raise NotFoundException(detail="No se encontraron citas para esta fecha")

    resultado = [
        {
            "id": item.id,
            "fecha": item.fecha,
            "estado": item.estado,
            "usuario_id": item.usuario_id,
            "medico_id": item.medico_id,
        }
        for item in data
    ]
    return resultado

@router.post("/crearCita", summary="Crear cita")
def crearCita(cita: Cita, db: Session = Depends(get_db)):
    """
    Crea una cita con los atributos recibidos.
    """
    newCita = models.Cita(
        fecha=cita.fecha,
        estado=cita.estado,
        usuario_id=cita.usuario_id,
        medico_id=cita.medico_id,
    )
    db.add(newCita)
    db.commit()
    db.refresh(newCita)
    return {"Respuesta": "Cita creada"}

@router.put("/actualizar/{id}", summary="Actualizar cita")
def actualizarCita(id: int, cita: schemas.Cita, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    """
    Actualiza la cita indicada por el id, con los atributos recibidos.
    Necesita auntenticación JWT
    """
    cita_db = db.query(models.Cita).filter(models.Cita.id == id).first() 
    if cita_db is None:
        raise NotFoundException(detail="No existe esa cita")

    cita_db.fecha = cita.fecha
    cita_db.estado = cita.estado
    cita_db.usuario_id = cita.usuario_id
    cita_db.medico_id = cita.medico_id

    db.commit() 
    db.refresh(cita_db)  

    return {"mensaje": "Cita actualizada"}

@router.delete("/eliminar/{id}", summary= "Eliminar una cita")
def eliminarCita(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """
    Elimina la cita indicada por el id.
    Necesita auntenticación JWT
    """
    cita = db.query(models.Cita).filter(models.Cita.id == id).first()
    if cita is None:
        raise NotFoundException(detail= "No existe la cita")
    db.delete(cita)
    db.commit()
    return {"mensaje": "Cita eliminada"}
