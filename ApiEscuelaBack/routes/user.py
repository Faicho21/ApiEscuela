from fastapi import APIRouter, Request
from models.user import (
    session,
    InputUser,
    User,
    InputLogin,
    UserDetail,
    InputUserDetail,
)
from fastapi.responses import JSONResponse
from psycopg2 import IntegrityError
from auth.seguridad import Seguridad
from sqlalchemy.orm import (
    joinedload, load_only,
)

user = APIRouter()
userDetail = APIRouter()


@user.get("/users/all") # Ruta protegida con token
def obtener_usuarios(req: Request):
   has_access = Seguridad.verificar_token(req.headers)
   if "iat" in has_access:
       usuarios = session.query(User).options(load_only(User.username), joinedload(User.userdetail)).all()
       return usuarios
   else:
       return JSONResponse(
           status_code=401,
           content=has_access,
       )


@user.post("/users/register")
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


@user.get("/")
def welcome():
    return "Bienvenido!!"


@user.get("/users/login/{n}")
def get_users_id(n: str):
    try:
        return session.query(User).filter(User.username == n).first()
    except Exception as ex:
        return ex


@user.post("/users/login")
def login_user(us: InputLogin):
    try:
        user = session.query(User).filter(User.username == us.username).first()
        if user and user.password == us.password:
            token = Seguridad.generar_token(user)
            res = {
                "status": "success",
                "token": token,
                "user": user.userdetail,
                "message": "User logged in successfully!",
            }
            return res

        else:
            res = {"message": "Invalid username or password"}
            return JSONResponse(status_code=401, content=res)
    except Exception as ex:
        print("Error ---->> ", ex)
    finally:
        session.close()

@user.post("/users/login")
def login_user(us: InputLogin):
   try:
       user = session.query(User).filter(User.username == us.username).first()
       if user and user.password == us.password:
           token = Seguridad.generar_token(user)
           res = {"status": "success",
                   "token": token,
                   "user": user.userdetail,
                   "message":"User logged in successfully!"}
           return res
       
       else:
           res = {"message": "Invalid username or password"}
           return JSONResponse(status_code=401, content=res)
   except Exception as ex:
       print("Error ---->> ", ex)
   finally:
       session.close()

@user.post("/users/loginUser")
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
           authDat = Seguridad.generar_token(user) # Genera el token de autenticación
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
    
@user.get("/users/all/NOSOTROS")
def obtener_usuario_detalle(req: Request):
    try:
        has_access = Seguridad.verificar_token(req.headers)
        if "iat" in has_access:
            usuarios = session.query(User).options(joinedload(User.userdetail)).all()
            usuarios_con_detalles = []  # Convierte los usuarios en una lista de diccionarios
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
            else:
                return JSONResponse(status_code=403, content=has_access)
    except Exception as e:
        print("Error al obtener usuarios:", e)
        return JSONResponse(
            status_code=500, content={"detail": "Error al obtener usuarios"}
        )



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
