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
<<<<<<< HEAD
            "rol"
=======
            "rol": authUser.rol,
            "nombre": authUser.firstName,
>>>>>>> 69f95d5dc9afdc708356947d9caf60b368a31db0
            "exp": cls.hoy() + datetime.timedelta(minutes=480)  # 48 horas de validez
        }
        token = jwt.encode(payload, cls.secret, algorithm="HS256")
        return token

    @classmethod
<<<<<<< HEAD
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
=======
    def verificar_token(token):
        try:
            payload = jwt.decode(token, Seguridad.secret, algorithms=["HS256"])
            return payload["usuario"]
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
>>>>>>> 69f95d5dc9afdc708356947d9caf60b368a31db0
