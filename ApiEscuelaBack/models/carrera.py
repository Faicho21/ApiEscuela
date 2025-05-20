from config.db import engine, Base
from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import sessionmaker, mapped_column, relationship
from pydantic import BaseModel

class Carrera(Base):
    
    __tablename__ = "carreras"

    id = mapped_column("id", Integer, primary_key=True)
    nombre = mapped_column("nombre", String)
    estado = mapped_column("estado", String)
    user_id = mapped_column(ForeignKey("users.id"))
    materias = relationship("Materia", back_populates="carrera")
    user = relationship("User", uselist=False, back_populates="carrera")

    def __init__(self, nombre, estado, user_id):
        self.nombre = nombre
        self.estado = estado
        self.user_id = user_id
        
class NuevaCarrera(BaseModel):
    nombre: str
    estado: str
    user_id: int
        

Base.metadata.create_all(bind=engine)

# creo una clase tipo sessionmaker
Session = sessionmaker(bind=engine)


# instancio un objeto que apunte a cada clase Session
session = Session()