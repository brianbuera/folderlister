from pathlib import Path
import shutil
from mensajes import *
from validadores import validar_ruta
from datetime import datetime


def obtener_camaras(directorio: Path):
    
    diccionario_videos = []
    rutas_videos = obtenerVideosOrdenados(directorio)

    for idx, dir in enumerate(rutas_videos):
        a_eliminar = dir.parent.parent.parent
        nuevo_nombre = directorio / f"{str(idx+1).zfill(2)} - {dir.parent.name}"
        
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





def obtenerInfo(idx : int,dir : Path, nuevo_nombre : Path, a_eliminar : Path):
    fecha_hora = obtenerHorario(dir.name)
    return {"orden" : idx+1,
            "Ruta_inicial" : dir.parent,
            "nueva_ruta" : nuevo_nombre,
            "hora_fecha" : fecha_hora,
            "para_eliminar": a_eliminar}

def obtenerVideosOrdenados(directorio: Path):
    rutas = []
    for dir in directorio.rglob("*.mkv"):
        rutas.append(dir)
    return quicksort_videos(rutas)


def obtenerHorario(video):
    fecha_hora = video.split(" (")[0]
    dt = datetime.strptime(fecha_hora, "%d_%m_%Y %H_%M_%S")
    return dt
    

def quicksort_videos(arr):
    """
    """
    if len(arr) <= 1:
        return arr
    pivot = obtenerHorario(arr[len(arr) // 2].name)
    left = [x for x in arr if obtenerHorario(x.name) < pivot]
    middle = [x for x in arr if obtenerHorario(x.name) == pivot]
    right = [x for x in arr if obtenerHorario(x.name) > pivot]
    return quicksort_videos(left) + middle + quicksort_videos(right)