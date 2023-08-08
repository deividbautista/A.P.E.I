# A.P.E.I
Proyecto enfocado en solventar las necesidades de la empresa telcore, el cual se basa en un sistema administrador de procesos de entrega o instalación de la empresa telcore.

## Requisitos previos
* Python [python download](https://www.python.org/downloads/release/python-31010/)
---

```sh
# Otorgar permisos a windows en caso de ser solicitados
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process    
```
```sh
# Crear entorno virtual
virtualenv env   
```
```sh
# Activar entorno virtual para instalar dependencias
env/Scripts/activate 
```
```sh
# Instalar las dependencias que necesitaremos en este proyecto
pip install -r requirements.txt 
```
```sh
# Para correr el proyecto
python src/app.py 
```
