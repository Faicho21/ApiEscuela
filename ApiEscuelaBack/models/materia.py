from config.db import engine, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from pydantic import BaseModel

class Materia(Base):
   
   __tablename__ = "materias"
   
   id = Column("id", Integer, primary_key=True)
   nombre = Column("nombre", String)   
   user_id = Column("user_id", Integer, ForeignKey("usuarios.id"), nullable=True)
   career_id = Column("career_id", Integer, ForeignKey("carreras.id"), nullable=True)
   carrera = relationship("Carrera", back_populates="materias", uselist=False)
   usuario = relationship("User", uselist=False, back_populates="rmateria")


   def __init__(self, nombre, user_id, career_id):
      self.nombre = nombre      
      self.career_id = career_id
      self.user_id = user_id

class InputMateria(BaseModel):
   nombre: str
   estado: str
   user_id: int
   career_id: int

# Crear la sesión
Session = sessionmaker(bind=engine)
session = Session() 