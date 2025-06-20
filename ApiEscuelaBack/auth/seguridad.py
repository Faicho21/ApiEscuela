import datetime, pytz, jwt

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
            "rol": authUser.rol,
            "nombre": authUser.firstName,
            "exp": cls.hoy() + datetime.timedelta(minutes=480)  # 48 horas de validez
        }
        token = jwt.encode(payload, cls.secret, algorithm="HS256")
        return token

    @classmethod
    def verificar_token(token):
        try:
            payload = jwt.decode(token, Seguridad.secret, algorithms=["HS256"])
            return payload["usuario"]
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
