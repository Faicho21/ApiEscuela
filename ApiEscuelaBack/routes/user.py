from fastapi import APIRouter
from models.user import session, InputUser, User, InputLogin, UserDetail, InputUserDetail,ImputMateria,Materia
from fastapi.responses import JSONResponse
from psycopg2 import IntegrityError
from sqlalchemy.orm import (
   joinedload,
)

user = APIRouter()
userDetail = APIRouter()
materia = APIRouter()


@materia.post("/RMateria")
def ingresar_materia(materia: ImputMateria):
    try:
        new_materia = Materia(materia.nombre, materia.estado,materia.user_id,materia.career_id)
        session.add(new_materia)
        session.commit()
        return "materia agregada"
    except Exception as e:
       session.rollback()
       print("Error inesperado:", e)
       return JSONResponse(
           status_code=500, content={"detail": "Error al agregar materia"}
       )
    finally:
       session.close()

@materia.get("/misMaterias")
def consultar_materias():
    try:
        materias = session.query(Materia).options(joinedload(Materia.usuario)).all()
        ver_materias = []
        for materia in materias:
            ver_materia = {
                "id": materia.id,
                "nombre": materia.nombre,
                "estado": materia.estado,
                "user_id": materia.user_id,
                "career_id": materia.career_id,
            }
            ver_materias.append(ver_materia)
        return JSONResponse(status_code=200, content=ver_materias)
    except Exception as e:
        print("Error al obtener materias:", e)
        return JSONResponse(
            status_code=500, content={"detail": "Error al obtener materias"}
        )

@user.get("/users/all")
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



@user.post("/users/loginUser")
def login_post(user: InputLogin):
   try:
       usu = User(user.username, user.password)
       res = session.query(User).filter(User.username == usu.username).first()
       if not res:
          return None
       if res.password == usu.password:
         data = session.query(UserDetail).filter(res.id_userdetail == UserDetail.id).first()
         #trae de la tabla todos los detalles de usuario que coincida con el id
         return data
       else:
           return None
   except Exception as e:
       print(e)


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


#region de userDetail
@userDetail.get("/userdetail/all")
def get_userDetails():
   try:
       return session.query(UserDetail).all()
   except Exception as e:
       print(e)


@userDetail.post("/userdetail/add")
def add_usuarDetail(userDet: InputUserDetail):
   usuNuevo = UserDetail(
   userDet.dni, userDet.firstName, userDet.lastName, userDet.type,           userDet.email
   )
   session.add(usuNuevo)
   session.commit()
   return "usuario detail agregado"

#endregion de userDetail