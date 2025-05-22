from config.db import engine, Base
from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, mapped_column, relationship
from pydantic import BaseModel
import datetime

class Pago(Base):
   
   __tablename__ = "pagos"

   id = mapped_column("id", Integer, primary_key=True)
   carrera_id = mapped_column(ForeignKey("carreras.id"))
   user_id = mapped_column(ForeignKey("usuarios.id"))
   monto = mapped_column(Integer)
   mes = mapped_column(DateTime)
   creado_en = mapped_column(DateTime, default=datetime.datetime.now())
   user = relationship("User", uselist=False, back_populates="pago")
   carrera = relationship("Carrera", uselist=False)

   def __init__(self, carrera_id, user_id, monto, mes):
       self.carrera_id = carrera_id
       self.user_id = user_id
       self.monto = monto
       self.mes = mes
       
class NuevoPago(BaseModel):
   carrera_id: int
   user_id: int
   monto: int
   mes: datetime.datetime
   creado_en: datetime.datetime = datetime.datetime.now()

# Eliminamos la creación de tablas de aquí
Session = sessionmaker(bind=engine)
session = Session()