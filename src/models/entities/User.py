#-----------------------------------------------------
# Sección donde importaremos Modulos, Instancias y variables, que utilizaresmos.
#-----------------------------------------------------
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

# --------------------------------------------------------------------------------------
# Definimos la clase user, con los parametros de userMixin, para autentificar al usuario.
class User(UserMixin):
    # Utilizamos el metodo __init__, para poder instanciar la función de manera rapida y facil.

    # Esta función nos brinda la recopilación de los atributos del usuario.
    def __init__(self, id, NDI, Contraseña, Nombre_completo, Direccion, Telefono, Empresa, Cargo, Area_locativa, Email, Fecha_nacimiento, Rol, Nombre_img  = "" ) -> None:
        #  Direccion, Telefono, Empresa, Cargo, Area_locativa, Email, Fecha_nacimiento.
        self.id = id
        self.NDI = NDI
        self.Contraseña = Contraseña
        self.Nombre_completo = Nombre_completo
        self.Direccion = Direccion
        self.Telefono = Telefono
        self.Empresa = Empresa
        self.Cargo = Cargo
        self.Area_locativa = Area_locativa
        self.Email = Email
        self.Fecha_nacimiento = Fecha_nacimiento
        self.Rol = Rol
        self.Nombre_img = Nombre_img

    # Para realizar la verificación y comprovación del hash.
    @classmethod
    def check_password(self, hashed_password, Contraseña):
        return check_password_hash(hashed_password, Contraseña)
# --------------------------------------------------------------------------------------

# print(generate_password_hash("12345"))
# pbkdf2:sha256:600000$PKyNFkIhaLNxRkg3$eef35b3a10abd6667d3edac1e3b759ae55052b2344cc3a40e7b7b1bffc1a3618
# pbkdf2:sha256:600000$RmJkvDljtnXNGrSM$8c36155079b871e820f0d70c83458edaacaa9535fca958fcfb3fbfb0639ffeba