
# Sección donde importaremos Modulos, Instancias y variables, que utilizaresmos.
from .entities.User import *

# --------------------------------------------------------------------------------------
# Sección de la clase principal donde realizaremos las consultas requeridas.
class ModelUser():
    # Usamos el decorador siguiente para poder utilizar las propiedades a la hora de llamarlas en el archivo"app".
    @classmethod

    # definimos login con los parametros necesarios para realizar la consulta pertinente.
    def login(self,Database,user):
        # Presentamos el bloque try, el cual pasara a ejecutar la sentencia "SQL".
        try:
            # Definimos cursor para la sentencia SQL, la cual obtendremos todos los datos del usuario.
            cursor=Database.connection.cursor()
            sql="""SELECT id_usuarios, NDI, Contraseña FROM usuarios
                    WHERE NDI = '{}' """.format(user.NDI)    
            cursor.execute(sql)
            row=cursor.fetchone()

            # Aqui tenemos la condicional if con la que determinamos, si la variable row no esta vacia
            # se realizara lo siguiente.
            if row != None:
                # Definimos arrow como una lista en la posición indicada, que corresponde a los atributos
                # del usuario, anteriormente consultados.
                user=User(row[0],row[1],User.check_password(row[2],user.Contraseña),0,0,0,0,0,0,0,0,0,0)
                # Para retornar la lista con los datos.
                return user
            else:
                # En caso de no cumplirse la condición, no se retornara ningún valor.
                return None
        except Exception as ex:
            raise Exception(ex)
        
    # Usamos el decorador siguiente para poder utilizar las propiedades a la hora de llamarlas en el archivo"app".
    @classmethod
    def get_by_id(self,Database,id_usuarios):
        # Presentamos el bloque try, el cual pasara a ejecutar la sentencia "SQL".
        try:
            # Definimos cursor, para realizar la siguiente consulta, donde sustraeremos el id del usuario.
            cursor=Database.connection.cursor()
            sql="""SELECT id_usuarios, NDI, Nombre_completo, Direccion, Telefono, Empresa, Cargo, Area_locativa, Email, Fecha_nacimiento, Rol, Nombre_img FROM usuarios
                    WHERE id_usuarios = '{}' """.format(id_usuarios)    
            cursor.execute(sql)
            # Especificamos el metodo feetchone, el cual nos permite manetener la difeerencia y conservación 
            # de las mayusculas y minusculas.
            row=cursor.fetchone()

            # De igual manera para este bloque, se debe determinar la condicional que pondra en analisis 
            # el array con los datos del usuario.
            if row != None:
                return User(row[0],row[1],None,row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11])
            else:
                return None
        # se utiliza except para dar fin al bloqué.
        except Exception as ex:
            raise Exception(ex)
# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------    
# Obtener nombre de todos los usuarios registrados para poder asignarlos.

# Definimos la función que retornara los datos de los usuarios.
def datosUsuarios(Database):
    cursor = Database.connection.cursor()
    cursor.execute("""
                SELECT u.id_usuarios, u.Nombre_completo, u.NDI, u.Direccion, u.Telefono, u.Empresa, u.Cargo, u.Area_locativa, u.Email, u.Fecha_nacimiento, u.Rol, GROUP_CONCAT(a.id_proceso) as id_procesos
                FROM usuarios u
                INNER JOIN asignaciones a
                ON u.id_usuarios = a.id_usuarios
                GROUP BY u.id_usuarios;
                """)
    myresult = cursor.fetchall()
    # Convertir los datos a diccionario.
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()  
    # Almacenamos los datos o contenido obtenido de la consulta en la variable dataUser.
    dataUser=insertObject  
    # Retorna la variable dataUser.
    return dataUser
# --------------------------------------------------------------------------------------

def deleteU(Database, idU):
    dato = (idU)
    cursor = Database.connection.cursor()
    sql ="DELETE FROM usuarios WHERE id_usuarios= {}"
    cursor.execute(sql.format(dato))
    Database.connection.commit()
# --------------------------------------------------------------------------------------