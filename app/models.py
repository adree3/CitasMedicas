from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base


class Medico(Base):
    __tablename__ = "medicos"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    especialidad = Column(String, nullable=False)
    horario = Column(String)

class Cita(Base):
    __tablename__ = "citas"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    medico_id = Column(Integer, ForeignKey("medicos.id"))
    fecha = Column(Date, nullable=False)
    estado = Column(String, default="pendiente")
    usuario = relationship("Usuario")
    medico = relationship("Medico")

class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    contrasena = Column(String, nullable=False)
    rol = Column(String, default="paciente", nullable=False)

    