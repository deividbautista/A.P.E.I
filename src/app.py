# Importar las librerias principales para la función del aplicativo.
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_socketio import SocketIO
from flask_mysqldb import MySQL
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

import re

# El módulo os en Python proporciona los detalles y la funcionalidad del sistema operativo.
import os 

# Modulo para obtener la ruta o directorio
from os import path 

# -----------------------------------------------------------------------------------------
# Apartado para importar modulos del paquete / directorio models.
# -----------------------------------------------------------------------------------------

# Conexión base de datos:
from database import config

# Models:
from models.ModelUser import ModelUser, datosUsuarios

from models.ModelGeneral import extensiones_validas

from models.ModelProcess import datos_proceso, deleteP, deleteR, editP, deleteAsignados, generate_pdf, addPosts, toRegisterM

# Entities:
from models.entities.User import User

from models.entities.User import *

# -----------------------------------------------------------------------------------------
# Fin apartado para importar modulos del paquete / directorio models.
# -----------------------------------------------------------------------------------------


# Constructor principal para ejecutar el sistema de información.
app = Flask(__name__)

# Para poder brindar seguridad extra, al usar tokens.
csrf = CSRFProtect()

# Para utilizar sentencias sql
Database = MySQL(app)

# Para el control de vistas a usuarios no registrados.
login_manager_app = LoginManager(app)

# Para inicializar el "socketio", que nos permite realizar comunicación a tiempo real.
socketio = SocketIO(app, cors_allowed_origins="*")
    
# Función para poder hacer uso de las instancias de LoginManager.
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(Database, id)


# -----------------------------------------------------
# Apartado de las rutas principales con sus respectivas caracteristicas.
# -----------------------------------------------------

# -----------------------------------------------------
# Apartado de las clases que se utilizara para la estructuración del formulario.
# -----------------------------------------------------
class LoginForm(FlaskForm):
    NDI = StringField('Número de documento', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')


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


# -----------------------------------------------------------------------------------------
# Sección principal de control de posts / procesos.
# -----------------------------------------------------------------------------------------
# Ruta que renderiza la vista de los procesos.
@app.route("/posts")
# Utilizamos el metodo de login_required para proteger esta ruta y exigir que se inicie sesión
# de manera obligatoria para acceder a esta, y no poder hacerlo encontrando la ruta.
@login_required
def posts():    

    dataUser = datosUsuarios(Database)
    processed_data = datos_proceso(Database)
    fecha_actual = datetime.now().date()
    umbral_maximo_dias = 15

    for processed in processed_data:
        # Se realiza la operación para la diferencia entre los dias, utilizando la biblioteca datetime.
        diferencia = processed["fecha_limite"] - fecha_actual
        progreso = 1.0 - min(diferencia.days / umbral_maximo_dias, 1.0)

        if progreso <= 0:
            progreso = 0.03
            # Redondear el valor de progreso a un número entero
        processed["diferencia_dias"] = diferencia.days
        processed["progreso"] = round(progreso * 100)

        if processed["diferencia_dias"] <= 0:

            if 'id_usuarios' in processed:
                for id_usuarios in processed['id_usuario']:
                    mensaje = f"El proceso de {processed['Titulo']} ha expirado. Por favor, actualice el proceso o contacte al administrador para más detalles."
                    data = (id_usuarios, processed["id_proceso"], mensaje, datetime.now(), 0 )

            toRegisterM(Database, data)

            # Enviar notificación a través de SocketIO
            socketio.emit('notificacion', {'mensaje': 'El proceso ha expirado.'})

    return render_template("task posts/task posts.html", data=processed_data, datosU=dataUser)
# ------------------------------------------------------

# ------------------------------------------------------
@app.route('/addPosts', methods=['POST'])
def añadirP():
    # Definimos las variables con los valores obtenidos en el formulario.
    Titulo = request.form['Titulo']
    Descripcion = request.form['Descripcion']
    FechaIn = request.form['fecha_I']
    Fechali = request.form['fecha_L']
    NivelImportancia = request.form['select']
    asignados = request.form.getlist('usuarios_seleccionados')
    Estado_proceso = 1

    addPosts(Database, Titulo, Descripcion, FechaIn, Fechali, NivelImportancia, asignados, Estado_proceso)

    return redirect(url_for('posts'))
# ------------------------------------------------------

# ------------------------------------------------------
# Ruta para eliminar los procesos registrados en la base de datos.
@app.route('/deleteProcess/<string:idP>')
def eliminarP(idP):
    deleteP(Database, idP)
    return redirect(url_for('posts'))
# ------------------------------------------------------


# ------------------------------------------------------
# Ruta para eliminar el reporte generado.
@app.route('/deleteReport/<string:idP>')
def eliminarR(idP):
    deleteR(Database, idP)
    return redirect(url_for('posts'))
# ------------------------------------------------------


# ------------------------------------------------------
# Ruta para editar los atributos insertados del proceso seleccionado.
@app.route('/edit/<string:id_proceso>', methods=['POST'])
def editarP(id_proceso):

    Titulo =            request.form['Titulo']
    Descripcion =       request.form['Descripcion']
    asignados =         request.form.getlist('usuarios_seleccionados_2')
    NivelImportancia =  request.form['selectI']
    Estado_proceso =    request.form['selectP']

    if Titulo and Descripcion:
        data = (Titulo, Descripcion, NivelImportancia, Estado_proceso, id_proceso)
        editP(Database, data, asignados)

    return redirect(url_for('posts'))
# ------------------------------------------------------


# ------------------------------------------------------
# Ruta para eliminar asigandos en un proceso.
@app.route('/deleteAsignacion', methods=['POST'])
@csrf.exempt
def eliminarAsignados():
    data = request.json
    idU = data.get("id_asignado")
    idP = data.get("id_proceso")

    deleteAsignados(Database, idU, idP)
    return jsonify({"status": "success", "message": idP})
# ------------------------------------------------------


# ------------------------------------------------------
# Ruta para generar reporte en pdf.
@app.route('/generar_reporte', methods=['GET', 'POST'])
def generar_reporte():
    if request.method == 'POST':
        # Captura los datos del formulario.
        id_proceso       = request.form.get('idProceso')
        titulo           = request.form['titulo']
        descripcion      = request.form['descripcion']
        imagen_file      = request.files['archivo']
        Estado_proceso   = request.form['EstadoProceso']

        # Variable que guarda el valor de la extensión deseada para aplicar.
        nombrepdf        = id_proceso + '.pdf'

        data = (Estado_proceso, nombrepdf, id_proceso)
        generate_pdf(Database, data, imagen_file, titulo, descripcion)

    return redirect(url_for('posts'))
# ------------------------------------------------------

# -----------------------------------------------------------------------------------------
# Sección principal de autentificación de usuario.
# -----------------------------------------------------------------------------------------
# Para definir la ruta y metodos por los que obtendremos los datos del login.
@app.route("/login", methods=["GET", "POST"])
# Función principal de login, que sera el pilar principal de todo nuestro sistema de información.
def login():
    # Este if principal reune el desarrollo principal en el que determinaremos las funcionalidades principales
    # como primero definir si tenemos los datos enviados por metodo POST
    form = LoginForm()
    if form.validate_on_submit():
        # Definir la instancia usuarios, la cual le pasamos los parametros del "NDI" y el "password".
        user = User(
            0, request.form["NDI"], request.form["password"], 0, 0, 0, 0, 0, 0, 0, 0, 0
        )

        # Funcion para comprovar el logged del usuario, osea verificar que es una cuenta existente.
        logged_user = ModelUser.login(Database, user)

        # Siguiendo con la misma funcionalidad, tenemos la comprovación de que el usuario esta registrado
        # es certera, se procedera a realizar los siguientes if.
        if logged_user != None:
            # Este if nos comprueba si la contraseña sustraida, esta registrada o no, en la base de datos.
            if logged_user.Contraseña:
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
                return redirect(request.url)
        # Caso en el que no encontremos que es un usuario registrado simplemente le indicaremos lo siguiente.
        else:
            # Usamos nuevamente el metodo para enviar mensaje donde indicamos al usuario que no se ha encontrado su usuario.
            flash("usuario no encontrado...")
            # Para dar retorno a nuestra ruta principal.
            return redirect(request.url)
    # En caso de que el metodo no sea autentificado se realizara lo siguiente.
    else:
        # Para dar retorno a nuestra ruta principal.
        return render_template("auth/login.html")
# ------------------------------------------------------


# ------------------------------------------------------
@app.route("/editProfile", methods=["POST"])
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
            if archivo.filename != '':
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
                    cursor = Database.connection.cursor()
                    # Veremos la siguiente consulta de tipo UPDATE, en el que le pasamos los parametros para insertar los datos que deseamos actualizar.
                    sql="""UPDATE users SET Nombre_img = '{1}'  WHERE NDI = {0}"""
                    # Definimos la variable atr con los parametros para realizar la consulta de manera dinamica.
                    Atr = (NumDoc, nuevoNombreFile)
                    # Usamos el execute para poder realizar la consulta anteriormente mostrada.
                    cursor.execute(sql.format(Atr[0],Atr[1]))
                    # cursor.execute(sql)
                    Database.connection.commit()
                    print(archivo.filename)
                else:
                    flash ("Archivo invalido😢", "error")
                    return redirect("profile")
        #------------------------------------------------------------------------------------------------------
           
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
        cursor = Database.connection.cursor()
        # Veremos la siguiente consulta de tipo UPDATE, en el que le pasamos los parametros para insertar los datos que deseamos actualizar.
        sql="""UPDATE usuarios SET Nombre_completo = '{0}', Direccion = '{1}', Telefono= '{2}', Empresa= '{3}', Cargo= '{4}', 
                Area_locativa= '{5}', Fecha_nacimiento = '{6}', NDI= '{7}', Email= '{8}' WHERE NDI = {7}"""
        # Usamos el execute para poder realizar la consulta anteriormente mostrada.
        cursor.execute(sql.format(datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],datos[6],datos[7],datos[8]))
        # sql = "UPDATE user SET fullname = 'mandragora' WHERE id = 1 "
        # cursor.execute(sql)
        Database.connection.commit()

        flash("Se actualizó correctamente🥳","success")
        return redirect("profile")
    except Exception as ex:
         raise Exception(ex)
# ------------------------------------------------------


# -----------------------------------------------------------------------------------------
# Apartado de las funciones de los errores.
# -----------------------------------------------------------------------------------------
# Error en el que el usuario quiere acceder a una ruta que posee el "Login_requeried"
# el cual lo redigira a la ruta login principal.
def status_401(error):
    return redirect(url_for("login"))


# Error en el que el usuario intenta accesar a una ruta invalida o incorrecta.
def status_404(error):
    return "<h1>Pagina no encontrada :(...<h1/>", 404
# ------------------------------------------------------


# -----------------------------------------------------------------------------------------
# Apartado de inicialización del proyecto.
# -----------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.config.from_object(config["development"])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True, port=5050)


