from config.db import engine, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel

class User(Base):

   __tablename__ = "usuarios"  # nombre de la tabla en la base de datos


   id = Column("id", Integer, primary_key=True)
   username = Column("username", String)
   password = Column("password", String)
   id_userdetail = Column(Integer, ForeignKey("userdetails.id"))
   userdetail = relationship("UserDetail", backref="user", uselist=False)

   def __init__(self,username,password):
       self.username = username
       self.password = password


class UserDetail(Base):

   __tablename__ = "userdetails"

   id = Column("id", Integer, primary_key=True)
   dni = Column("dni", Integer)
   firstName = Column("firstName", String)
   lastName = Column("lastName", String)
   type = Column("type", String)
   email = Column("email", String(80), nullable=False, unique=True)


   def __init__(self, dni, firstName, lastName, type, email):
       self.dni = dni
       self.firstName = firstName
       self.lastName = lastName
       self.type = type
       self.email = email


class InputUser(BaseModel):
   username: str
   password: str
   email: str
   dni: int
   firstname: str
   lastname: str
   type: str
   
class InputLogin(BaseModel):
    username: str
    password: str


class InputUserDetail(BaseModel):
   dni: int
   firstName: str
   lastName: str
   type: str
   email: str

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


# creo una clase tipo sessionmaker
Session = sessionmaker(bind=engine)


# instancio un objeto que apunte a cada clase Session
session = Session()