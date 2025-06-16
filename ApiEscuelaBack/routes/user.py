from fastapi import APIRouter, Request
from auth.security import Security
from models.user import (session,InputUser,User,InputLogin,UserDetail,InputUserDetail,)
from models.pivote_user_carrera import PivoteUserCareer, InputUserAddCareer
from fastapi.responses import JSONResponse
from psycopg2 import IntegrityError
from sqlalchemy.orm import (
    joinedload,
)

user = APIRouter()
userDetail = APIRouter()


@user.get("/")
def welcome():
    return "Bienvenido!!"


@user.get("/users/all")
def obtener_usuarios(req: Request):
    has_access = Security.verify_token(req.headers)
    if "iat" in has_access:
        usuarios = session.query(User).all()
        return usuarios
    else:
        return JSONResponse(
            status_code=401,
            content=has_access,
        )

@user.post("/users/login")
def login_post(userIn: InputLogin):
    try:
        user = session.query(User).filter(User.username == userIn.username).first()
        if not user.password == userIn.password:
            return JSONResponse(
                status_code=401,
                content={
                    "success": False,
                    "message": "Usuario y/o password incorrectos!",
                },
            )
        else:
            authDat = Security.generate_token(user)  # Genera el token de autenticación
            if not authDat:
                return JSONResponse(
                    status_code=401,
                    content={
                        "success": False,
                        "message": "Error de generación de token!",
                    },
                )
            else:
                return JSONResponse(
                    status_code=200, content={"success": True, "token": authDat}
                )

    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Error interno del servidor",
            },
        )

@user.get("/users/allNOSOTROS")
def obtener_usuario_detalle():
    try:
        # Carga los detalles del usuario con unión
        usuarios = session.query(User).options(joinedload(User.userdetail)).all()
        # Convierte los usuarios en una lista de diccionarios
        usuarios_con_detalles = []
        for usuario in usuarios:
            usuario_con_detalle = {
                "id": usuario.id,
                "username": usuario.username,
                "dni": usuario.userdetail.dni,
                "first_Name": usuario.userdetail.firstName,
                "last_Name": usuario.userdetail.lastName,
                "type": usuario.userdetail.type,
                "email": usuario.userdetail.email,
            }
            usuarios_con_detalles.append(usuario_con_detalle)

        return JSONResponse(status_code=200, content=usuarios_con_detalles)
    except Exception as e:
        print("Error al obtener usuarios:", e)
        return JSONResponse(
            status_code=500, content={"detail": "Error al obtener usuarios"}
        )


@user.post("/users/register")  #para registrar los usuarios con datos completos 
def crear_usuario(user: InputUser):
    try:
        if validate_username(user.username):
            if validate_email(user.email):
                newUser = User(
                    user.username,
                    user.password,
                )
                newUserDetail = UserDetail(
                    user.dni, user.firstname, user.lastname, user.type, user.email
                )
                newUser.userdetail = newUserDetail
                session.add(newUser)
                session.commit()
                return "Usuario agregado"
            else:
                return "El email ya existe"
        else:
            return "el usuario ya existe"
    except IntegrityError as e:
        # Suponiendo que el msj de error contiene "username" para el campo duplicado
        if "username" in str(e):
            return JSONResponse(
                status_code=400, content={"detail": "Username ya existe"}
            )
        else:
            # Maneja otros errores de integridad
            print("Error de integridad inesperado:", e)
            return JSONResponse(
                status_code=500, content={"detail": "Error al agregar usuario"}
            )
    except Exception as e:
        session.rollback()
        print("Error inesperado:", e)
        return JSONResponse(
            status_code=500, content={"detail": "Error al agregar usuario"}
        )
    finally:
        session.close()


@user.post("/user/addcareer")
def addCareer(ins: InputUserAddCareer):
    try:
        newInsc = PivoteUserCareer(ins.id_user, ins.id_career)
        session.add(newInsc)
        session.commit()
        res = f"{newInsc.user.userdetail.firstName} {newInsc.user.userdetail.lastName} se ha inscripto a la carrera {newInsc.career.name}"
        print(res)
        return res
    except Exception as ex:
        session.rollback()
        print("Error al inscribir al alumno:", ex)
        import traceback

        traceback.print_exc()
    finally:
        session.close()


def validate_username(value):
    existing_user = session.query(User).filter(User.username == value).first()
    session.close()
    if existing_user:
        return None
        ##raise ValueError("Username already exists")
    else:
        return value

def validate_email(value):
    existing_email = session.query(UserDetail).filter(UserDetail.email == value).first()
    session.close()
    if existing_email:
        ##raise ValueError("Email already exists")
        return None
    else:
        return value


# region de userDetail
@userDetail.get("/userdetail/all")
def get_userDetails():
    try:
        return session.query(UserDetail).all()
    except Exception as e:
        print(e)


@userDetail.post("/userdetail/add")
def add_usuarDetail(userDet: InputUserDetail):
    usuNuevo = UserDetail(
        userDet.dni, userDet.firstName, userDet.lastName, userDet.type, userDet.email
    )

    session.add(usuNuevo)
    session.commit()
    return "usuario detail agregado"
# endregion de userDetail


# Region PREGUNTAR A MARIANO SI VAN


@user.post("/users/loginUser")
def login_post(user: InputLogin):
    try:
        usu = User(user.username, user.password)
        res = session.query(User).filter(User.username == usu.username).first()
        if not res:
            return None
        if res.password == usu.password:
            data = (
                session.query(UserDetail)
                .filter(res.id_userdetail == UserDetail.id)
                .first()
            )
            # trae de la tabla todos los detalles de usuario que coincida con el id
            return data
        else:
            return None
    except Exception as e:
        print(e)


# endregion PREGUNTAR A MARIANO SI VAN
