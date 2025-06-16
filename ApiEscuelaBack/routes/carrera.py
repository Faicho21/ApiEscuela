from fastapi import APIRouter
from models.carrera import Carrera, NuevaCarrera, session

from fastapi.responses import JSONResponse
from psycopg2 import IntegrityError
from sqlalchemy.orm import (
   joinedload,
)
carrera = APIRouter()

@carrera.post("/nuevaCarrera")
def nueva_carrera(carrera: NuevaCarrera):
    try:
        nueva_carrera = Carrera(
            nombre=carrera.nombre,
            estado=carrera.estado,
            user_id=carrera.user_id
        )
        session.add(nueva_carrera)
        session.commit()
        return JSONResponse(status_code=200, content={"message": "Carrera creada exitosamente"})
    except IntegrityError:
        session.rollback()
        return JSONResponse(status_code=400, content={"message": "Error al crear la carrera"})
    finally:
        session.close()

