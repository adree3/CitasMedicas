from datetime import date, datetime
from pydantic import BaseModel

class Usuario(BaseModel):
    nombre: str
    email: str
    contrasena: str
    rol: str = "paciente"

class Login(BaseModel):
    email: str
    contrasena: str

    class Config:
        orm_mode = True 

class Medico(BaseModel):
    nombre: str
    especialidad: str
    horario : str
    class Config:
        orm_mode = True


class Cita(BaseModel):
    usuario_id: int
    medico_id: int
    fecha: date
    estado: str = "pendiente"

    class Config:
        orm_mode = True
