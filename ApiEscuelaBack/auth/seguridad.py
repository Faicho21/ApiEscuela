import datetime, pytz, jwt
from models.user import User
from fastapi import Header
from fastapi.responses import JSONResponse


class Seguridad:
   secret = "pepito"


   @classmethod
   def hoy(cls):
       return datetime.datetime.now(pytz.timezone("America/Buenos_Aires"))




   @classmethod
   def generar_token(cls, authUser: User): 
       
       payload = {
           "iat": cls.hoy(),
           "username": authUser.username,
           "user_id": authUser.id,
           "user_role": authUser.userdetail.type,
           "exp": cls.hoy() + datetime.timedelta(minutes=480),
       }
       try:
           return jwt.encode(payload, cls.secret, algorithm="HS256")
       except Exception as e:
              print(f"Error generating token: {e}")
              return None
  


   @classmethod
   def verificar_token(cls, headers):
       if headers["authorization"]:
           try:
               tkn = headers["authorization"].split(" ")[1]
               payload = jwt.decode(tkn, cls.secret, algorithms=["HS256"])
               return payload
           except jwt.ExpiredSignatureError:
               return {"success": False, "message": "Token expired!"}
           except jwt.InvalidSignatureError:
               return {"success": False, "message": "Token: signature error!"}
           except jwt.DecodeError as e:
               return {"success": False, "message": "Invalid token!"}
           except Exception as e:
               return {"success": False, "message": "Token: unknown error!"}
       else:
           return {"success": False, "message": "Authorization header missing!"}
       
def obtener_usuario_desde_token(authorization: str = Header(...)):
   token = authorization.split(" ")[1]
   payload = Seguridad.verificar_token({"authorization": f"Bearer {token}"})
   if isinstance(payload, dict) and payload.get("success") is False:
       return JSONResponse(status_code=401, content=payload)
   
   return payload

