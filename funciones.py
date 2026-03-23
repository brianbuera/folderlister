from pathlib import Path
import shutil
from mensajes import *
from datetime import datetime


def obtener_camaras(directorio: Path):
    diccionario_videos = []
    rutas_videos = obtenerVideosOrdenados(directorio)

    for idx, dir in enumerate(rutas_videos,1):
        a_eliminar = dir.parent.parent.parent
        nuevo_nombre = directorio / f"{str(idx).zfill(2)} - {dir.parent.name}"
        if not nuevo_nombre.exists():
            if not (a_eliminar.is_dir() or a_eliminar == directorio):
                return False
            info_videos = obtenerInfo(idx ,dir , nuevo_nombre, a_eliminar)
            diccionario_videos.append(info_videos)
    return diccionario_videos  


def detalles(diccionario : dict):
    print(f"Orden:  {diccionario["orden"]}")
    print(f"Ruta inicial: {diccionario["Ruta_inicial"]}")
    print(f"Nueva ruta del directorio: {diccionario["nueva_ruta"]}")
    print(f"Hora y fecha: {diccionario["hora_fecha"].strftime("%H:%M:%S %Y-%m-%d")}")
    print("Se eliminará: ", {diccionario["para_eliminar"]},"\n")

#Recibe como parametros un id, direccion del video, nueva_direccion, direccion_a_eliminar
def obtenerInfo(idx : int,dir : Path, nuevo_nombre : Path, a_eliminar : Path):
    fecha_hora = obtenerHorario(dir.name)
    return {"orden" : idx,
            "Ruta_inicial" : dir.parent,
            "nueva_ruta" : nuevo_nombre,
            "hora_fecha" : fecha_hora,
            "para_eliminar": a_eliminar}

#funcion para obtener las rutas de los videos enumerados por horarios
def obtenerVideosOrdenados(directorio: Path):
    rutas = []
    for dir in directorio.rglob("*.mkv"):
        rutas.append(dir)
    return ordenarmiento_rapido(rutas)


#Obtiene por parametro el nombre de un video en (ejemplo: 29_10_2025 14_31_20 (UTC-03_00).mp4)
#Devuelve un datetime a partir del nombre del video
def obtenerHorario(video):
    fecha_hora = video.split(" (")[0]
    dt = datetime.strptime(fecha_hora, "%d_%m_%Y %H_%M_%S") 
    return dt
    
#Ordena una lista de rutas de videos de menor a mayor por horario
def ordenarmiento_rapido(arr):
    if len(arr) <= 1:
        return arr
    pivot = obtenerHorario(arr[len(arr) // 2].name)
    left = [x for x in arr if obtenerHorario(x.name) < pivot]
    middle = [x for x in arr if obtenerHorario(x.name) == pivot]
    right = [x for x in arr if obtenerHorario(x.name) > pivot]
    return ordenarmiento_rapido(left) + middle + ordenarmiento_rapido(right)