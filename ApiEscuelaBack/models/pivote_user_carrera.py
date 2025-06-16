from config.db import engine, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel

class PivoteUserCareer(Base):
   __tablename__="pivote_user_career"
   id = Column(Integer, primary_key=True)
   id_career = Column(ForeignKey("carreras.id"))
   id_user = Column(ForeignKey("usuarios.id"))
   career = relationship("Carrera", uselist=False)
   user = relationship("User", uselist=False, back_populates="pivoteusercareer")


   def __init__(self, id_user, id_career):
       self.id_user = id_user
       self.id_career = id_career

class InputUserAddCareer(BaseModel):
   id_user: int
   id_career: int

Session = sessionmaker(bind=engine)
session = Session()