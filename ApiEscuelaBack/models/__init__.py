from config.db import engine, Base
from models.user import User, UserDetail, Materia
from models.carrera import Carrera
from models.pago import Pago

# Crear todas las tablas en el orden correcto
def init_db():
    Base.metadata.create_all(bind=engine) 