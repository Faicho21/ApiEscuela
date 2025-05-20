from fastapi import FastAPI
from routes.user import user, userDetail, materia
from routes.pago import pago
from fastapi.middleware.cors import CORSMiddleware


api_escu = FastAPI()


api_escu.include_router(user)
api_escu.include_router(userDetail)
api_escu.include_router(materia)
api_escu.include_router(pago)

# Middleware para permitir CORS

api_escu.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["GET", "POST", "PUT", "DELETE"],
   allow_headers=["*"],
)