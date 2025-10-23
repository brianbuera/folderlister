from pathlib import Path
import shutil
from mensajes import *
from validadores import validar_ruta
from datetime import datetime


def enumerar(directorio: Path):
    
    eliminados = []
    rutas_videos = obtenerVideosOrdenados(directorio)

    for idx, dir in enumerate(rutas_videos):
        carpeta= dir.parent
        eliminar = carpeta.parent.parent
        nuevo_nombre = directorio / f"{str(idx+1).zfill(2)} - {carpeta.name}"
        
        if not nuevo_nombre.exists():
            detalles(idx, dir, nuevo_nombre)
            #carpeta.rename(nuevo_nombre)
        if eliminar.is_dir() and eliminar.parent == directorio:
            eliminados.append(eliminar)

    return True  

def detalles(idx : int,dir : Path, nuevo_nombre : Path):
    fecha_hora = obtenerHorario(dir.name).strftime("%H:%M %Y-%m-%d")
    print(f"Directorio numero {idx+1}")
    print(f"Ruta inicial: {str(dir)}")
    print(f"Nuevo nombre: {str(nuevo_nombre)} - Hora y fecha: {fecha_hora}")
    print(f"Nueva ruta del directorio: {str(nuevo_nombre)}")
    print("")


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