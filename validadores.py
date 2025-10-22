import re 

pattern = re.compile(
    r'(?:[/\\])Exportar \d{2}-\d{2}-\d{4} \d{2}-\d{2}-\d{2}'
    r'(?:[/\\])Formato de reproductor de medios'
    r'(?:[/\\])\d{3} - [A-Za-zÁÉÍÓÚáéíóúÑñ ]+'
    r'(?:[/\\])\d{2}_\d{2}_\d{4} \d{2}_\d{2}_\d{2} \(UTC-[0-9]{2}_[0-9]{2}\)\.mkv$'
)

def validar_ruta(directorio):
    """
    Valida todos los archivos .mkv dentro de un directorio.
    Muestra mensajes de error detallados si alguna ruta falla.
    """

    rutas_videos = list(directorio.rglob("*.mkv"))
    if not rutas_videos:
        print("❌ No se encontraron videos .mkv en el directorio.")
        return False

    todo_valido = True

    for ruta_video in rutas_videos:
        ruta_str = str(ruta_video)

        if not ruta_video.exists() or not ruta_video.is_file():
            print(f"❌ ERROR: No existe o no es un archivo: {ruta_video}")
            todo_valido = False
            continue

        if not ruta_str.startswith(str(directorio)):
            print(f"❌ ERROR: El archivo no está dentro del directorio base: {ruta_video}")
            todo_valido = False
            continue

        if not pattern.search(ruta_str):
            print(f"❌ ERROR: La ruta no cumple con el formato esperado: {ruta_video}")
            todo_valido = False

    return todo_valido
