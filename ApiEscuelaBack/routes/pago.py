from fastapi import APIRouter, Request, Depends
from auth.seguridad import obtener_usuario_desde_token, Seguridad
from models.pago import Pago, NuevoPago, session
from models.user import User
from fastapi.responses import JSONResponse
from psycopg2 import IntegrityError
from sqlalchemy.orm import (
   joinedload,
)

pago = APIRouter()

@pago.post("/nuevoPago") #Ruta para  ADMIN ingrese un nuevo pago
def nuevo_pago(pago: NuevoPago, payload: dict = Depends(obtener_usuario_desde_token)):
    if payload["rol"] != "Admin":
        return JSONResponse(status_code = 403, detail = "No tienes permiso para Ingresar Pagos")
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

@pago.delete("/eliminarPago/{pago_id}") #Ruta para ADMIN eliminar un pago
def eliminar_pago(pago_id: int, payload: dict = Depends(obtener_usuario_desde_token)):
    if payload["rol"] != "Admin":
        return JSONResponse(status_code=403, detail="No tienes permiso para eliminar Pagos")
    try:
        pago = session.query(Pago).filter_by(id=pago_id).first()
        if not pago:
            return JSONResponse(status_code=404, content={"message": "Pago no encontrado"})

        session.delete(pago)
        session.commit()
        return {"message": "Pago eliminado"}
    finally:
        session.close()

@pago.put("/editarPago/{pago_id}") #Ruta para ADMIN editar un pago
def modificar_pago(pago_id: int, pago: NuevoPago, payload: dict = Depends(obtener_usuario_desde_token)):
    if payload["rol"] != "Admin":
        return JSONResponse(status_code=403, detail="No tienes permiso para editar Pagos")
    try:
        pago_existente = session.query(Pago).filter_by(id=pago_id).first()
        if not pago_existente:
            return JSONResponse(status_code=404, content={"message": "Pago no encontrado"})

        pago_existente.carrera_id = pago.carrera_id
        pago_existente.user_id = pago.user_id
        pago_existente.monto = pago.monto
        pago_existente.mes = pago.mes

        session.commit()
        return {"message": "Pago modificado exitosamente"}
    except IntegrityError:
        session.rollback()
        return JSONResponse(status_code=400, content={"message": "Error al modificar el pago"})
    finally:
        session.close()

@pago.get("/pagos/todos")  #para que el ADMIN vea todos los pagos
def ver_todos_los_pagos(payload: dict = Depends(obtener_usuario_desde_token)):
    if payload["rol"] not in ["Admin"]:
        raise JSONResponse(status_code=403, detail="No tienes permiso para ver los pagos")
    
    try:
        pagos = session.query(Pago).all()
        return pagos
    finally:
        session.close()

@pago.get("/pago/mis_pagos")     #para que un alumno vea sus pagos
def ver_mis_pagos(payload: dict = Depends(obtener_usuario_desde_token)):
    if payload["rol"] != "Alumno":
        raise JSONResponse(status_code=403, detail="Solo los alumnos puede ver estos pagos")
    
    try:
        user = session.query(User).filter_by(username=payload["usuario"]).first()
        if user:
            return user.pago
        return JSONResponse(status_code=404, content={"message": "Usuario no encontrado"})
    finally:
        session.close()



















@pago.post("/users/payments")
def show_user_payments(u: NuevoPago, req: Request):  #falta hacer otro modelo e integraro despues del U: 
   has_access = Seguridad.verificar_token(req.headers)
   if "iat" in has_access:
       usuario = session.query(User).filter(User.id == u.user_id).first() 
       if usuario:
           return usuario.pago 
       else:
           return JSONResponse(
               status_code=404,
               content={"success": False, "message": "User not found!"},
           )
   else:
       return JSONResponse(
           status_code=401,
           content=has_access,
       )


@pago.post("/pago ")
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