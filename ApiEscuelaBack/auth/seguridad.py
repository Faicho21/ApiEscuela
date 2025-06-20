import datetime, pytz, jwt
from fastapi import Header, HTTPException

class Seguridad:
    secret = "tu_clave_secreta"
    
    @classmethod
    def hoy(cls):
        return datetime.datetime.now(pytz.timezone("America/Buenos_Aires")) # Método para obtener la fecha y hora actual en Buenos Aires

    @classmethod
    def generar_token(cls, authUser): # Método para generar un token JWT
        payload = {
            "iat": cls.hoy(),
            "usuario": authUser.username,
            "rol": authUser.userdetail.type,
            "exp": cls.hoy() + datetime.timedelta(minutes=480)  # 48 horas de validez
        }
        token = jwt.encode(payload, cls.secret, algorithm="HS256")
        return token

    @classmethod
    def verificar_token(cls, header):
        if header["authorization"] :
            token = header["authorization"].split(" ")[1]
            try:
                payload = jwt.decode(token, cls.secret, algorithms=["HS256"])
                return payload
            except jwt.ExpiredSignatureError:
                return {"success": False, "message": "Token expirado"}
            except jwt.InvalidTokenError:
                return {"success": False, "message": "Token inválido"}
            except jwt.DecodeError:
                return {"success": False, "message": "Error al decodificar el token"}
            except Exception as e:
                return {"success": False, "message": "Token: error desconocido"}
            
def obtener_usuario_desde_token(authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    payload = Seguridad.verificar_token({"authorization": f"Bearer {token}"})
    if isinstance(payload, dict) and payload.get("success") is False:
        raise HTTPException(status_code=401, detail=payload["message"])
    return payload  # contiene usuario, rol, etc.