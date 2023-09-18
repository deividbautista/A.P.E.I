# Apartado en el que se importan todos los modulos necesarios para el proyecto.
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import date, timedelta, datetime
from xhtml2pdf import pisa
from tempfile import TemporaryFile
from random import sample

import os
import io

import database as db

from flask import Flask, render_template, Response, request


# En este apartado realizamos la configuración de las rutas en flask.
template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

# En este apartado inicializamos la configuración de la ruta.
app = Flask(__name__, template_folder = template_dir)

# Definimos la función denominada "idAleatorio", la cual nos retornara un numero 
# generado al azar, dentro de los valores 1 al 9, con una extención o longitud de 9 digitos o 9 caracteres
def idAleatorio():
    # Caracteres que puede poseer el int aleatorio.
    id_aleatorio = "123456789"
    # Logintud determinada para el int aleatorio.
    longitud         = 9
    # Utilizamos la función upper para combertir los caracteres en mayuscula.
    secuencia        = id_aleatorio.upper()
    # Definimos la variable "resultado_aleatorio", que con la función sample 
    # y los parametros de secuencia y longitud, generamos el int aleatorio.
    resultado_aleatorio  = sample(secuencia, longitud)
    # Volvemos a definir a la varibale "id_aleatorio", pero esta vez le 
    # insertamos el valor optenido de "resultado_aleatorio". 
    id_aleatorio     = "".join(resultado_aleatorio)
    # Finalmente retornamos de nuestra función el resultado con el valor aleatorio.
    return id_aleatorio
# --------------------------------------------------------------------------------------

# Definimos la función que retornara los datos de los usuarios.
def datosUsuarios():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM users")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario.
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()  
    #Almacenamos los datos o contenido obtenido de la consulta en la variable dataUser.
    dataUser=insertObject  
    #Retorna la variable dataUser
    return dataUser
# --------------------------------------------------------------------------------------

def datos_proceso():
    cursor = db.database.cursor()
    query = """
    SELECT p.*, GROUP_CONCAT(u.id) AS id_usuario, GROUP_CONCAT(u.fullname) AS nombre_usuario
    FROM procesos p
    LEFT JOIN asignaciones a ON p.id_proceso = a.id_proceso
    LEFT JOIN users u ON a.id = u.id
    GROUP BY p.id_proceso
    ORDER BY p.fecha_creacion DESC;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    dataUser = datosUsuarios()

    # Procesa los resultados para formar una estructura de datos más adecuada
    processed_data = []
    for row in data:
        proceso = {
            "id_proceso": row[0],  # Usar el índice numérico correspondiente
            "Titulo": row[1],      # Usar el índice numérico correspondiente
            "Descripcion": row[2], # Usar el índice numérico correspondiente
            "fecha_inicio": row[3], # Usar el índice numérico correspondiente
            "fecha_limite": row[4], # Usar el índice numérico correspondiente
            "nombre_usuario": row[9].split(",") if row[9] is not None else [],
            "id_usuario": row[8].split(",") if row[8] is not None else [],
        }
        # # Lista de claves que deseas formatear
        # claves_a_formatear = ["fecha_inicio", "fecha_limite"]

        # # Formatea las fechas especificadas en "DD/MM/AA"
        # for key in claves_a_formatear:
        #     fecha = proceso.get(key)  # Obtiene el valor de la clave (si existe)
        #     if fecha:
        #         proceso[key] = fecha.strftime("%d/%m/%y")

        # En la siguiente linea se utiliza el metodo "append", para agregar los
        # elementos a la lista de proceso que se renderizara en el archivo template html.
        processed_data.append(proceso)    
    # Retornamos finalmente los datos del proceso.
    return processed_data
# --------------------------------------------------------------------------------------

# Tenemos la ruta principal donde se visualizaran los procesos almacenados en la BD.
@app.route("/")
def home():
    umbral_maximo_dias = 30
    processed_data = datos_proceso()
    dataUser = datosUsuarios()
    for processed in processed_data:
        # Se realiza la operación para la diferencia entre los dias, utilizando la biblioteca datetime.
        diferencia = processed["fecha_limite"] - processed["fecha_inicio"]
        progreso = 1.0 - min(diferencia.days / umbral_maximo_dias, 1.0)

        if progreso <= 0:
            progreso = 0.03
            # Redondear el valor de progreso a un número entero
        processed["diferencia_dias"] = diferencia.days
        processed["progreso"] = round(progreso * 100)
    return render_template("index.html", data=processed_data, datosU=dataUser)
# --------------------------------------------------------------------------------------

# Ruta para guardar usuarios en la Base de datos.
@app.route('/proceso', methods=['POST'])
def addUser():
    Titulo = request.form['Titulo']
    Descripcion = request.form['Descripcion']
    FechaIn = request.form['fecha_I']
    Fechali = request.form['fecha_L']
    id_proceso = idAleatorio()
    asignados = request.form.getlist('usuarios_seleccionados')

    if Titulo and Descripcion:
        cursor = db.database.cursor()
        sql = "INSERT INTO procesos (id_proceso, Titulo, Descripcion, Fecha_inicio, Fecha_terminación) VALUES (%s, %s, %s, %s, %s)"
        data = (id_proceso, Titulo, Descripcion, FechaIn, Fechali)
        cursor.execute(sql, data)
        db.database.commit()

    if len (asignados) > 0:
        for Numid in asignados:
            cursor = db.database.cursor()
            sql = "INSERT INTO asignaciones (id, id_proceso) VALUES (%s, %s)"
            data = (Numid, id_proceso)
            cursor.execute(sql, data)
            db.database.commit()
    return redirect(url_for('home'))
# --------------------------------------------------------------------------------------

# Ruta para eliminar los procesos registrados en la base de datos.
@app.route('/delete/<string:idP>')
def delete(idP):
    dato = (idP)
    cursor = db.database.cursor()
    sql ="DELETE FROM procesos WHERE id_proceso= {}"
    cursor.execute(sql.format(dato))
    db.database.commit()
    return redirect(url_for('home'))
# --------------------------------------------------------------------------------------

# Ruta para eliminar las asignaciones en los procesos registrados en la base de datos.
@app.route('/deleteAsignacion', methods=['POST'])
def deleteAsignados():
    data = request.json
    idU = data.get("id_asignado")
    idP = data.get("id_proceso")

    cursor = db.database.cursor()
    sql = """DELETE FROM asignaciones
             WHERE id = %s AND id_proceso = %s"""
             
    cursor.execute(sql, (idU, idP))
    db.database.commit()
    return jsonify({"status": "success", "message": idP})
# --------------------------------------------------------------------------------------

# Ruta para realizar la actualización de los datos de los procesos.
@app.route('/edit/<string:id_proceso>', methods=['POST'])
def edit(id_proceso):
    Titulo = request.form['Titulo']
    Descripcion = request.form['Descripcion']

    if Titulo and Descripcion:
        cursor = db.database.cursor()
        sql="""UPDATE procesos SET Titulo = '{0}', Descripcion = '{1}' WHERE id_proceso = {2}"""
        # Usamos el execute para poder realizar la consulta anteriormente mostrada.
        data = (Titulo, Descripcion, id_proceso)
        cursor.execute(sql.format(data[0],data[1],data[2]))
        db.database.commit()
        
    return redirect(url_for('home'))
# --------------------------------------------------------------------------------------

# Función para verificar si la extensión del archivo es compatible.
def extensiones_validas(filename):
    # Lista de extensiones permitidas para los archivos de imagen "PERMITIDOS".
    extensiones_permitidas = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # Obtener la extensión del archivo que se desea evaluar si se encuentra entre los parametros.
    # Esto funciona al definir una variable de llamada estension, la cual obtendra como valor el str
    # que se obtiene al separar el nombre del archivo por el separador de ".", y desplazando el valor
    # de la cadena creada al final, donde se encontrara la extensión, osea se obtiene la cadena de texto
    # despues del punto ".".
    extension = filename.rsplit('.', 1)[1].lower()

    # Verificar si la extensión está permitida.
    if '.' in filename and extension in extensiones_permitidas:
        # Retornar verdadero si el resultado es positivo.
        return True
    else:
        # Reetornar falso si el resultado es negativo.
        return False
# --------------------------------------------------------------------------------------

# Ruta principal para la construcción del pdf.
@app.route('/generar_pdf', methods=['GET', 'POST'])
def generate_pdf():
    if request.method == 'POST':
        # Captura los datos del formulario
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        imagen = request.files['archivo']

        # Condicional donde utilizaremos la funcion de extensiones_validas, para evaluar si el archivo esta permitido o no.
        if(request.files['archivo'] and extensiones_validas(imagen.filename)):
            # Crea un archivo temporal para guardar la imagen
            with TemporaryFile(delete=False) as tmp_file:
                imagen.save(tmp_file)

            # Obtén la ruta del archivo temporal
            ruta_temporal = tmp_file.name
        else:
            # En caso de no tener un archivo permitido se retornara el mensaje de error.
            return "archivo invalido"         
           
        # Renderiza la plantilla HTML y reemplaza los marcadores de posición con datos
        rendered_template = render_template('plantillas para pdf/example.html', titulo=titulo, descripcion=descripcion, imagen=ruta_temporal)
        
        # Combina el contenido HTML y los estilos CSS
        css_file = open('E:/documentación etapa productiva -_-/Proyecto_APEI/GENERAR-PDF/Metodo con xhtml2pdf/src/static/css/style.css', 'r').read()
        html_content = f"{rendered_template}\n<style>{css_file}</style>"
        
        # Crea un objeto de tipo BytesIO para almacenar el PDF generado
        pdf_buffer = io.BytesIO()
        
        # Genera el PDF a partir del contenido HTML con estilos CSS
        pisa.CreatePDF(src=html_content, dest=pdf_buffer)
        
        # Mueve el puntero al inicio del objeto BytesIO
        pdf_buffer.seek(0)
        
        # Crea un objeto Response para enviar el PDF al navegador
        response = Response(pdf_buffer.read(), content_type='application/pdf')
        
        # Agrega el encabezado para la descarga del PDF
        response.headers['Content-Disposition'] = 'inline; filename=mi_pdf.pdf'
        
        # Ruta completa de guardado (puedes cambiarla según tus necesidades)
        ruta_de_guardado = 'F:\documentacion Etapa pr0ductiva -_-\Proyecto_APEI\Generador de procesos\Metodo-3.1\src\static\pdf\123456789.pdf'

        # Guarda el archivo PDF con el nombre generado automáticamente
        with open(ruta_de_guardado, 'wb') as pdf_file:
            pdf_file.write(pdf_buffer.getvalue())
        
        # Retorna la petición http, entregando el resultado, osea la visualización del pdf construido.  
        return response
    else:
        # Si no se envió el formulario, muestra un mensaje
        mensaje = "No se encontraron datos, por lo que no es posible generar el PDF correctamente."
        return mensaje
# --------------------------------------------------------------------------------------

# Condicional para dar inicialización al proyecto.
if __name__ == '__main__':   
    app.run(debug=True, port=3040)


