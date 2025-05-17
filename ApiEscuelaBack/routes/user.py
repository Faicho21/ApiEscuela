from fastapi import APIRouter
from models.user import session, InputUser, User, InputLogin, UserDetail, InputUserDetail
from fastapi.responses import JSONResponse
from psycopg2 import IntegrityError

user = APIRouter()
userDetail = APIRouter()

@user.get("/")
def welcome():
   return "Bienvenido!!"


@user.get("/users/all")
def get_users():
   try:
       return session.query(User).all()
   except Exception as ex:
       print(ex)


@user.get("/users/login/{n}")
def get_users_id(n: str):
   try:
       return session.query(User).filter(User.username == n).first()
   except Exception as ex:
       return ex

@user.post("/users/register")
def crear_usuario(user: InputUser):
   try:
       # Si el usuario cumple con la validación, y no hay errores, lo agregamos.
       if validate_username(user.username): 
           usuNuevo = User(user.username, user.password)
           session.add(usuNuevo)
           session.commit()
           return "usuario agregado"
       else:
           return "el usuario ya existe"
   except IntegrityError as e:
       # Suponiendo que el mje de error contiene "username" para el campo duplicado
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
       print("Error inesperado:", e)
       return JSONResponse(
           status_code=500, content={"detail": "Error al agregar usuario"}
       )



@user.post("/users/loginUser")
def login_post(user: InputLogin):
   try:
       usu = User(0, user.username, user.password, "", "")
       res = session.query(User).filter(User.username == usu.username).first()
       if not res:
          return None
       if res.password == usu.password:
           return res
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

#endregion de userDetail