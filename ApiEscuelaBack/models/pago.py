from config.db import engine, Base
from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, mapped_column, relationship
from pydantic import BaseModel
import datetime

class Pago(Base):
   __tablename__ = "payments"


   id = mapped_column("id", Integer, primary_key=True)
   career_id = mapped_column(ForeignKey("careers.id"))
   user_id = mapped_column(ForeignKey("users.id"))
   monto = mapped_column(Integer)
   mes = mapped_column(DateTime)
   creado_en = mapped_column(DateTime, default=datetime.datetime.now())
   user = relationship("User", uselist=False, back_populates="payments")
   career = relationship("Career", uselist=False)


   def __init__(self, career_id, user_id, monto, mes):
       self.career_id = career_id
       self.user_id = user_id
       self.monto = monto
       self.mes = mes
       
class NuevoPago(BaseModel):
   career_id: int
   user_id: int
   monto: int
   mes: datetime.datetime
   creado_en: datetime.datetime = datetime.datetime.now()

       
Base.metadata.create_all(bind=engine)

# creo una clase tipo sessionmaker
Session = sessionmaker(bind=engine)


# instancio un objeto que apunte a cada clase Session
session = Session()