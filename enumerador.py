from pathlib import Path
import shutil
from mensajes import *
from validadores import validar_ruta
from datetime import datetime


def enumerar(directorio: Path):
    eliminados = []

    if not any(directorio.iterdir()):
        show_error(VACIO)
        return
 
    if not validar_ruta(directorio):
        show_error(NO_CUMPLE_REQUISTOS)
        return
    
    rutas_videos = obtenerRutasVideos(directorio)

    for idx, dir in enumerate(rutas_videos):
        carpeta= dir.parent
        eliminar = carpeta.parent.parent
        nuevo_nombre = directorio / f"{str(idx+1).zfill(2)} - {carpeta.name}"
        
        if not nuevo_nombre.exists():
            print(f"Movido a: {nuevo_nombre}\{obtenerHorario(dir.name).strftime("%H:%M %Y-%m-%d")}")
        if eliminar.is_dir() and eliminar.parent == directorio:
            eliminados.append(eliminar)
    print("\nLista de directorios a eliminar:") 
    for e in eliminados:
        print(e)
    show_info("Exito","Los directorios se han enumerado correctamente")  

        
def obtenerRutasVideos(directorio: Path):
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