from fastapi import APIRouter
from models.pago import Pago, NuevoPago, session
from models.user import User
from fastapi.responses import JSONResponse
from psycopg2 import IntegrityError
from sqlalchemy.orm import (
   joinedload,
)

pago = APIRouter()

@pago.post("/pago")

def nuevo_pago(pago: NuevoPago):
    
    try:
        nuevo_pago = Pago(
            carrera_id=pago.carrera_id,
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
    finally:
        session.close()

@pago.get("/pago/misPagos{_username}")

def ver_mispagos(_username: str):
    try:
        userEncontrado = session.query(User).filter(User.username == _username).first()
        if(userEncontrado):
            return userEncontrado.pago
        else:
            return "usuario no encontrado"
    except Exception as e:
        session.rollback()
        print("Error al traer usuario y/o pagos")
    
    finally:
        session.close()