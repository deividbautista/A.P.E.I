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
def deleteP(idP, Database):
    dato = (idP)
    cursor = Database.connection.cursor()
    sql ="DELETE FROM procesos WHERE id_proceso= {}"
    cursor.execute(sql.format(dato))
    Database.connection.commit()