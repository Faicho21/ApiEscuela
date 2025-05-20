from fastapi import APIRouter
from models.pago import Pago, NuevoPago, session
from fastapi.responses import JSONResponse
from psycopg2 import IntegrityError
from sqlalchemy.orm import (
   joinedload,
)

user = APIRouter()
userDetail = APIRouter()
materia = APIRouter()
pago = APIRouter()

@pago.post("/pago")

def crear_pago(pago: NuevoPago):
    try:
        nuevo_pago = Pago(
            career_id=pago.career_id,
            user_id=pago.user_id,
            monto=pago.monto,
            mes=pago.mes
        )
        session.add(nuevo_pago)
        session.commit()
        return JSONResponse(status_code=200, content={"message": "Pago creado exitosamente"})
    except IntegrityError:
        session.rollback()
        return JSONResponse(status_code=400, content={"message": "Error al crear el pago"})