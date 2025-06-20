from fastapi import APIRouter, Request
from models.pago import Pago, NuevoPago, session
from models.user import User
from auth.seguridad import Seguridad
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

@pago.get("/pago/VerPagos")
def ver_mispagos(user_id: int, req: Request):
    has_access = Seguridad.verificar_token(req.headers)
    if "iat" in has_access:
        usuario = session.query(User).filter(User.id == user_id).first()
        if usuario:
            return usuario.pago
        else:
            return JSONResponse(status_code=404, content={"success": False, "message": "Usuario no encontrado"})
    else:
        return JSONResponse(status_code=401, content=has_access)