from fastapi import APIRouter
from models.user import session, InputUser, User, InputLogin


user = APIRouter()


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

@user.post("/users/new")
def crear_usuario(user: InputUser):
   usuNuevo = User(
       user.id,
       user.username,
       user.password,
       user.firstName,
       user.lastName,
   )
   session.add(usuNuevo)
   session.commit()
   return "usuario agregado"


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