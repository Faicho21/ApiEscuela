from config.db import engine, Base
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel

class Carrera(Base):
    
    __tablename__ = "carreras"

    id = Column ("id", Integer, primary_key=True)
    nombre = Column("nombre", String)
    estado = Column("estado", String)
    user_id = Column(ForeignKey("usuarios.id"))
    materias = relationship("Materia", back_populates="carrera")
    user = relationship("User", uselist=False, back_populates="carrera")
    career = relationship("PivoteUserCareer", back_populates="career", uselist=False)
   


    def __init__(self, nombre, estado, user_id,):
        self.nombre = nombre
        self.estado = estado
        self.user_id = user_id
        
        
class NuevaCarrera(BaseModel):
    nombre: str
    estado: str
    user_id: int

# Eliminamos la creación de tablas de aquí
Session = sessionmaker(bind=engine)
session = Session()