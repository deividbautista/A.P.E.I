# Codigo sustraido del canal url=('https://youtu.be/FX0lMm_Qj10')
# creditos respectivos al autor y o su equipo de trabajo, "Repositorio=('https://github.com/UskoKruM/flask-login-mysql')"


# -----------------------------------------------------
# Sección donde importaremos Modulos, Instancias y variables, que utilizaresmos.
# -----------------------------------------------------
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required

import re

from config import config

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

from models.entities.User import *

# Para subir archivo tipo foto al servidor
from werkzeug.utils import secure_filename 

# El módulo os en Python proporciona los detalles y la funcionalidad del sistema operativo.
import os 

# Modulo para obtener la ruta o directorio
from os import path 

# -----------------------------------------------------
# Sección donde inicializaremos o definiremos las instancias principales.
# -----------------------------------------------------

# Constructor principal para ejecutar el sistema de información.
app = Flask(__name__)

# Para poder brindar seguridad extra, al usar tokens.
csrf = CSRFProtect()

# Para utilizar sentencias sql
db = MySQL(app)

# Para el control de vistas a usuarios no registrados.
login_manager_app = LoginManager(app)


# Función para poder hacer uso de las instancias de LoginManager.
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


# -----------------------------------------------------
# Sección principal de autentificación de usuario.
# -----------------------------------------------------
# Para definir la ruta y metodos por los que obtendremos los datos del login.
@app.route("/login", methods=["GET", "POST"])

# Función principal de login, que sera el pilar principal de todo nuestro sistema de información.
def login():
    # Este if principal reune el desarrollo principal en el que determinaremos las funcionalidades principales
    # como primero definir si tenemos los datos enviados por metodo POST
    if request.method == "POST":
        # Definir la instancia usuarios, la cual le pasamos los parametros del "NDI" y el "password".
        user = User(
            0, request.form["NDI"], request.form["password"], 0, 0, 0, 0, 0, 0, 0, 0, 0
        )

        # Funcion para comprovar el logged del usuario, osea verificar que es una cuenta existente.
        logged_user = ModelUser.login(db, user)

        # Siguiendo con la misma funcionalidad, tenemos la comprovación de que el usuario esta registrado
        # es certera, se procedera a realizar los siguientes if.
        if logged_user != None:
            # Este if nos comprueba si la contraseña sustraida, esta registrada o no, en la base de datos.
            if logged_user.password:
                login_user(logged_user)
                # En cuyo caso que el metodo de verificación nos comprueve que efectivamente es un usario y contraseña valida
                # se retornara a la vista que desea el usuario.
                return redirect(url_for("home"))
            else:
                # Caso contrario en que el usuario nos brinder una contraseña invalida pasaremos a indicarselo y redirigirnos
                # nuevamente al login principal.

                # Flash es un metodo que utilizamos para dar envio del mesaje a travez de un boton notificando lo indicado.
                flash("Contraseña invalida...")
                # Para dar retorno a nuestra ruta principal.
                return render_template("auth/login.html")
        # Caso en el que no encontremos que es un usuario registrado simplemente le indicaremos lo siguiente.
        else:
            # Usamos nuevamente el metodo para enviar mensaje donde indicamos al usuario que no se ha encontrado su usuario.
            flash("usuario no encontrado...")
            # Para dar retorno a nuestra ruta principal.
            return render_template("auth/login.html")
    # En caso de que el metodo no sea autentificado se realizara lo siguiente.
    else:
        # Para dar retorno a nuestra ruta principal.
        return render_template("auth/login.html")


# -----------------------------------------------------
# Sección para validar extensión del archivo.
# -----------------------------------------------------
def extensiones_validas(filename):
    # Lista de extensiones permitidas para los archivos de imagen
    extensiones_permitidas = {'png', 'jpg', 'jpeg', 'gif', 'svga', 'webp'}

    # Obtener la extensión del archivo
    extension = filename.rsplit('.', 1)[1].lower()

    # Verificar si la extensión está permitida
    if '.' in filename and extension in extensiones_permitidas:
        print("yes")
        return True
    else:
        return False

    

# -----------------------------------------------------
# Sección principal de actualización de usuario.
# -----------------------------------------------------
@app.route("/edit", methods=["POST"])
# Definimos la función "update", para poder ejecutar las distintas actividades que se realizara en este modulo.
def update():
    # Presentamos el bloque try, el cual pasara a ejecutar dos tipos de funciones, la primera sera en el caso
    # de que el usuario desee actualizar la foto de perfil, y la segunda función es para actualizar los datos 
    # regulares del usuario.
    try:
        # Definimos la condicional "if", con la cual se iniciara si optiene información de un formulario. 
        # por metodo 'POST'
        archivo = request.files['archivo']
        if request.method == 'POST':
            # La siguiente condicional se inicializara si encuentra un archivo en el boton del nombre "archivo" de tipo "file".
            if(request.files['archivo'] and extensiones_validas(archivo.filename)):
                # Definimos el parametro que utilizaremos en la consulta para guardar el nombre del archivo subido.
                NumDoc          = request.form['NDI']
                # Definimos el nombre del archivo.
                nombreArchivo   = NumDoc
                # Definimos la variable que almacenara lo enviado por el formulario.
                file            = request.files['archivo']
                # Definimos la variable que almacenara el nombre del archivo obtenido desde el path.
                basepath        = path.dirname (__file__)
                # Definimos el tipo de extensión que utilizaremos, en este caso "jpg".
                extension           = ('.jpg')
                # Definimos la vaariable que almacenara el núevo nombre asignado para la imagen.
                nuevoNombreFile     = nombreArchivo + extension
        
                # En la siguiente linea de cofigo se da el proceso para almacenar el archivo, definiendo el 
                # archivo, la ruta y el nuevo nombre del archivo.
                upload_path = path.join (basepath, 'static/img/avatars', nuevoNombreFile) 
                # Con la variable file y el metodo save para poder alamcenar el archivo, con los parametros que definimos anteriormente.
                file.save(upload_path)

                # Definimos cursor con la conexión de la base de datos para poder realizar la consulta.
                cursor = db.connection.cursor()
                # Veremos la siguiente consulta de tipo UPDATE, en el que le pasamos los parametros para insertar los datos que deseamos actualizar.
                sql="""UPDATE users SET Nombre_img = '{1}'  WHERE NDI = {0}"""
                # Definimos la variable atr con los parametros para realizar la consulta de manera dinamica.
                Atr = (NumDoc, nuevoNombreFile)
                # Usamos el execute para poder realizar la consulta anteriormente mostrada.
                cursor.execute(sql.format(Atr[0],Atr[1]))
                # cursor.execute(sql)
                db.connection.commit()
                print(archivo.filename)
            else:
                typeAlert = 0
                massage = "Archivo invalido 😢"
                return render_template('profile/profile.html', typeAlert=typeAlert, massage=massage)
        #-----------------------------------------------------------------------------------------------------------------------------------
           
        # Definimos todos los paremtros que recolectamos del formulario, y definimos una variable para utilizar 
        # los datos en la consulta posterior de MySql.
        nombre= request.form['fullname']
        direccion= request.form['Direccion']
        Telefono = request.form['Telefono']
        Empresa = request.form['Empresa']
        Cargo = request.form['Cargo']
        Area = request.form['Area']
        Fecha_nacimiento = request.form['FDN']
        NumDoc = request.form['NDI']
        Email = request.form['Email']

        # Definimos un array llamado datos para poder utilizar las vriables anteriormente definidas.
        datos = (nombre, direccion, Telefono, Empresa, Cargo, Area, Fecha_nacimiento, NumDoc, Email)

        # Definimos cursor con la conexión de la base de datos para poder realizar la consulta.
        cursor = db.connection.cursor()
        # Veremos la siguiente consulta de tipo UPDATE, en el que le pasamos los parametros para insertar los datos que deseamos actualizar.
        sql="""UPDATE users SET fullname = '{0}', Direccion = '{1}', Telefono= '{2}', Empresa= '{3}', Cargo= '{4}', 
                Area_locativa= '{5}', Fecha_nacimiento = '{6}', NDI= '{7}', Email= '{8}' WHERE NDI = {7}"""
        # Usamos el execute para poder realizar la consulta anteriormente mostrada.
        cursor.execute(sql.format(datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],datos[6],datos[7],datos[8]))
        # sql = "UPDATE user SET fullname = 'mandragora' WHERE id = 1 "
        # cursor.execute(sql)
        db.connection.commit()

        typeAlert = 1
        massage = "Se actualizo correctamente 🥳"
        return render_template('profile/profile.html', typeAlert=typeAlert, massage=massage)
    except Exception as ex:
         raise Exception(ex)
    

# -----------------------------------------------------
# Apartado de las rutas principales con sus respectivas caracteristicas.
# -----------------------------------------------------


# Para incializar el sistema de información con la ruta indicada.
@app.route("/")
def index():
    return redirect(url_for("login"))


# -----------------------------------------------------
# Ruta de login principal
@app.route("/logout")
# Utilizamos esta función para cerrar sesión del usuario y volver a login principal
# osea que para dirigirnos a la ruta del login, reflejaremos el cerrar sesión del usuario.
def logout():
    logout_user()
    return redirect(url_for("login"))


# -----------------------------------------------------
# Ruta de home donde nos llevara a la hora de realizar la verificación de usuario.
@app.route("/home")
# Utilizamos el metodo de login_required para proteger esta ruta y exigir que se inicie sesión
# de manera obligatoria para acceder a esta, y no poder hacerlo encontrando la ruta.
@login_required
def home():
    return render_template("home.html")


# -----------------------------------------------------
# Ruta de home donde nos llevara a la hora de realizar la verificación de usuario.
@app.route("/profile")
# Utilizamos el metodo de login_required para proteger esta ruta y exigir que se inicie sesión
# de manera obligatoria para acceder a esta, y no poder hacerlo encontrando la ruta.
@login_required
def profile():
    return render_template("profile/profile.html")


# -----------------------------------------------------
# Ruta de home donde nos llevara a la hora de realizar la verificación de usuario.
@app.route("/help")
# Utilizamos el metodo de login_required para proteger esta ruta y exigir que se inicie sesión
# de manera obligatoria para acceder a esta, y no poder hacerlo encontrando la ruta.
@login_required
def help():
    return render_template("help/help.html")


# -----------------------------------------------------
# Apartado de las funciones de los errores
# -----------------------------------------------------


# Error en el que el usuario quiere acceder a una ruta que posee el "Login_requeried"
# el cual lo redigira a la ruta login principal.
def status_401(error):
    return redirect(url_for("login"))


# Error en el que el usuario intenta accesar a una ruta invalida o incorrecta.
def status_404(error):
    return "<h1>Pagina no encontrada :(...<h1/>", 404


# -----------------------------------------------------
# Apartado de inicialización del proyecto.
# -----------------------------------------------------
if __name__ == "__main__":
    app.config.from_object(config["development"])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
