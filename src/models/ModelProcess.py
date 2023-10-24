
# Importar las dependencias necesarias para la correcta función de las funciones.
from models.ModelGeneral import extensiones_validas, idAleatorio

from flask import jsonify
from xhtml2pdf import pisa
from flask import render_template
from tempfile import TemporaryFile

import io
import os

# --------------------------------------------------------------------------------------
# Definimos la función "datos_proceso", la cual nos retornara todos los valores hallados en los registros de la base de datos.
def datos_proceso(Database):
    cursor = Database.connection.cursor()
    query = """
    SELECT p.*, GROUP_CONCAT(u.id_usuarios) AS id_usuario, GROUP_CONCAT(u.Nombre_completo) AS nombre_usuario
    FROM procesos p
    LEFT JOIN asignaciones a ON p.id_proceso = a.id_proceso
    LEFT JOIN usuarios u ON a.id_usuarios = u.id_usuarios
    GROUP BY p.id_proceso
    ORDER BY p.fecha_creacion DESC;
    """
    cursor.execute(query)
    data = cursor.fetchall()

    # Procesa los resultados para formar una estructura de datos más adecuada
    processed_data = []
    for row in data:
        proceso = {
            "id_proceso": row[0],        # Usar el índice numérico correspondiente
            "Titulo": row[1],            # Usar el índice numérico correspondiente
            "Descripcion": row[2],       # Usar el índice numérico correspondiente
            "fecha_inicio": row[3],      # Usar el índice numérico correspondiente
            "fecha_limite": row[4],      # Usar el índice numérico correspondiente
            "ReporteGenerado": row[6],   # Usar el índice numérico correspondiente
            "estado_proceso": row[7],    # Usar el índice numérico correspondiente
            "Nivel_importancia": row[8], # Usar el índice numérico correspondiente
            "nombre_usuario": row[10].split(",") if row[10] is not None else [],
            "id_usuario": [int(id) for id in row[9].split(",")] if row[9] is not None else [],
        }
        # En la siguiente linea se utiliza el metodo "append", para agregar los
        # elementos a la lista de proceso que se renderizara en el archivo template html.
        processed_data.append(proceso)    

    cursor.close()  # Cierra el cursor aquí

    # Retornamos finalmente los datos de los procesos.
    return processed_data
# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
def addPosts(Database, Titulo, Descripcion, FechaIn, Fechali, NivelImportancia, asignados, Estado_proceso):

    id_proceso = idAleatorio()
    NivelImportancia = int(NivelImportancia)

    if Titulo and Descripcion:
        cursor = Database.connection.cursor()
        sql = "INSERT INTO procesos (id_proceso, Titulo, Descripcion, Fecha_inicio, Fecha_terminación, Nivel_importancia, Estado_proceso) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data = (id_proceso, Titulo, Descripcion, FechaIn, Fechali, NivelImportancia, Estado_proceso)
        cursor.execute(sql, data)
        Database.connection.commit()

    if len (asignados) > 0:
        for Numid in asignados:
            cursor = Database.connection.cursor()
            sql = "INSERT INTO asignaciones (id_usuarios, id_proceso) VALUES (%s, %s)"
            data = (Numid, id_proceso)
            cursor.execute(sql, data)
            Database.connection.commit()
# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
def toRegisterN(Database, data):
    cursor = Database.connection.cursor()
    sql = "INSERT INTO notificacion (id_usuarios, id_proceso, mensaje, fecha, leido) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, data)
    Database.connection.commit()
    cursor.close()
# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
def notificacion_no_enviada(Database, id_proceso):
    cursor = Database.connection.cursor()
    sql = "SELECT COUNT(*) FROM notificacion WHERE id_proceso = %s AND leido = 0"
    cursor.execute(sql, (id_proceso,))
    result = cursor.fetchone()[0]
    cursor.close()
    return result == 0  # Devuelve True si no hay notificaciones no leídas, de lo contrario, devuelve False
# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
def marcar_notificacion_enviada(Database, id_proceso):
    cursor = Database.connection.cursor()
    sql = "UPDATE notificacion SET leido = 1 WHERE id_proceso = %s"
    cursor.execute(sql, (id_proceso,))
    Database.connection.commit()
    cursor.close()
# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
def deleteP(Database, idP):
    dato = (idP)
    cursor = Database.connection.cursor()
    sql ="DELETE FROM procesos WHERE id_proceso= {}"
    cursor.execute(sql.format(dato))
    Database.connection.commit()
# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
def deleteR(Database, idP):
    # Obtenemos la id del proceso el cual nos ayudara a realizar la consulta necesaria.
    dato = (idP)
    
    # Definimos los valores necesarios para la eliminación del archivo.
    Nombre = idP + '.pdf'
    Ruta_Archivo = 'E:\\documentación etapa productiva -_-\\Proyecto_APEI\\Integración_modulos\\primer_intentoTnT\\src\\static\\pdf\\' + Nombre

    # Sentencia try que ejecuta el bloque para eliminar el archivo. 
    try:
        # Proceso para eliminar el registro del reporte en la base de datos.
        cursor = Database.connection.cursor()
        sql ="UPDATE procesos SET ReporteGenerado = '' WHERE id_proceso = {}"
        cursor.execute(sql.format(dato))
        Database.connection.commit()

        # Eliminar el archivo por el metodo "os.remove".
        os.remove(Ruta_Archivo)
        # Imprimimos en la consola el mensaje de afirmación de eliminación.
        print(f"El archivo se ha borrado correctamente.")
    except FileNotFoundError:
        # Excepción en caso de no encontrar el archivo.
        print(f"El archivo {Ruta_Archivo} no se encontró.")
    except Exception as e:
        # Excepción en caso de un error a la hora de eliminar el archivo.
        print(f"Error al intentar borrar el archivo: {e}")
# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
def editP(Database, data, asignados):
    # En este apartado se realizara la actualización de los datos del proceso.
    cursor = Database.connection.cursor()
    sql="""UPDATE procesos SET Titulo = '{0}', Descripcion = '{1}', Nivel_importancia = '{2}',
    Estado_proceso = '{3}'  WHERE id_proceso = {4}""" 
    # Usamos el execute para poder realizar la consulta anteriormente mostrada.
    datos = data
    cursor.execute(sql.format(datos[0],datos[1],datos[2],datos[3],datos[4]))
    Database.connection.commit()

    # En este apartado se realizara la actualización de asignaciones del proceso.
    if len (asignados) > 0:
        for idAsigandos in asignados:
            cursor = Database.connection.cursor()
            sql = "INSERT INTO asignaciones (id_usuarios, id_proceso) VALUES (%s, %s)"
            id_proceso = datos[4]
            data = ( idAsigandos, id_proceso)
            cursor.execute(sql, data)
            Database.connection.commit()
# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
def deleteAsignados(Database, idU, idP):
    
    cursor = Database.connection.cursor()
    sql = """DELETE FROM asignaciones
             WHERE id_usuarios = %s AND id_proceso = %s"""
     
    cursor.execute(sql, (idU, idP))
    Database.connection.commit()

    return jsonify({"status": "success", "message": idP})
# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
def generate_pdf(Database, data, imagen_file, titulo, descripcion):

    # Condicional donde utilizaremos la funcion de extensiones_validas, para evaluar si el archivo esta permitido o no.
    if(extensiones_validas(imagen_file.filename)):
        # Crea un archivo temporal para guardar la imagen
        with TemporaryFile(delete=False) as tmp_file:
            imagen_file.save(tmp_file)
        # Obtén la ruta del archivo temporal
        ruta_temporal = tmp_file.name
    else:
        # En caso de no tener un archivo permitido se retornara el mensaje de error.
        return "archivo invalido"         
           
    # Renderiza la plantilla HTML y reemplaza los marcadores de posición con los datos.
    rendered_template = render_template('template of report/template_of_report.html', titulo=titulo, descripcion=descripcion, imagen=ruta_temporal)
        
    # Combina el contenido HTML y los estilos CSS.
    css_file = open('E:/documentación etapa productiva -_-/Proyecto_APEI/GENERAR-PDF/Metodo con xhtml2pdf/src/static/css/style.css', 'r').read()
    html_content = f"{rendered_template}\n<style>{css_file}</style>"
        
    # Crea un objeto de tipo BytesIO para almacenar el PDF generado.
    pdf_buffer = io.BytesIO()
        
    # Genera el PDF a partir del contenido HTML con estilos CSS.
    pisa.CreatePDF(src=html_content, dest=pdf_buffer)
        
    # Mueve el puntero al inicio del objeto BytesIO.
    pdf_buffer.seek(0)
        
    # Crea un objeto Response para enviar el PDF al navegador
    # response = Response(pdf_buffer.read(), content_type='application/pdf')
        
    # Agrega el encabezado para la descarga del PDF
    # response.headers['Content-Disposition'] = 'inline; filename=mi_pdf.pdf'
        
    # Ruta completa de guardado (puedes cambiarla según tus necesidades), para con la empresa
    # ruta_de_guardado = 'E:\\documentación etapa productiva -_-\\Proyecto_APEI\\Integración_modulos\\primer_intentoTnT\\src\\static\\pdf\\' + data[1]
    # Ruta completa de guardado (puedes cambiarla según tus necesidades), para el hogar
    ruta_de_guardado = 'C:\\Users\\Infinity Tech\\Desktop\\Projects\\APEI\\A.P.E.I\\src\\static\\pdf\\' + data[1]

    # Guarda el archivo PDF con el nombre generado automáticamente.
    with open(ruta_de_guardado, 'wb') as pdf_file:
        pdf_file.write(pdf_buffer.getvalue())

    # Realizamos la actualización en la base de datos de la construcción del reporte.
    if data:
        cursor = Database.connection.cursor()
        sql = "UPDATE procesos SET Estado_proceso = %s, ReporteGenerado = %s WHERE id_proceso = %s "
        cursor.execute(sql, data)
        Database.connection.commit()      
# --------------------------------------------------------------------------------------
