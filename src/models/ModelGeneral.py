
from random import sample

# --------------------------------------------------------------------------------------
# Sección para generar un cadenas o valores aleatorios.

# Definimos la función denominada "idAleatorio", la cual nos retornara un número
# generado al azar, dentro de los valores 1 al 9, con una extención o longitud de 9 digitos o 9 caracteres.
def idAleatorio():
    # Caracteres que puede poseer el int aleatorio.
    id_aleatorio = "123456789"
    # Logintud determinada para el int aleatorio.
    longitud = 9
    # Utilizamos la función upper para combertir los caracteres en mayuscula.
    secuencia = id_aleatorio.upper()
    # Definimos la variable "resultado_aleatorio", que con la función sample
    # y los parametros de secuencia y longitud, generamos el int aleatorio.
    resultado_aleatorio = sample(secuencia, longitud)
    # Volvemos a definir a la varibale "id_aleatorio", pero esta vez le
    # insertamos el valor optenido de "resultado_aleatorio".
    id_aleatorio = "".join(resultado_aleatorio)
    # Finalmente retornamos de nuestra función el resultado con el valor aleatorio.
    return id_aleatorio
# --------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------
# Sección para validar extensión de archivos img.
def extensiones_validas(filename):
    # Lista de extensiones permitidas para los archivos de imagen
    extensiones_permitidas = {"png", "jpg", "jpeg", "gif", "svga", "webp"}

    # Obtener la extensión del archivo
    extension = filename.rsplit(".", 1)[1].lower()

    # Verificar si la extensión está permitida
    if "." in filename and extension in extensiones_permitidas:
        return True
    else:
        return False
# --------------------------------------------------------------------------------------




