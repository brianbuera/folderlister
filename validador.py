import re


pattern = re.compile(
    r'^.*[\\/]'                                  # cualquier ruta previa
    r'Exportar \d{1,2}-\d{1,2}-\d{4} \d{2}-\d{2}-\d{2}'
    r'[\\/]Formato de reproductor de medios'
    r'[\\/][^\\/]+'                              # carpeta de cámara
    r'[\\/]\d{1,2}_\d{1,2}_\d{4} '               # fecha del archivo
    r'\d{2}_\d{2}_\d{2} '
    r'\(UTC-[0-9]{2}_[0-9]{2}\)'
    r'\.(mkv|mp4)$'
)




def validar_recien_exportados(directorio):

    rutas = list(directorio.iterdir())
    rutas_videos = list(directorio.rglob("*.mkv"))

    if len(rutas) != len(rutas_videos):
        return "❌ Uno o varios directorios no tienen video"

    if not rutas_videos:
        return "❌ No se encontraron videos .mkv en el directorio."
    
    todo_valido = ""

    for ruta_video in rutas_videos:
        ruta_str = str(ruta_video).replace("\\", "/")  # 🔧 NORMALIZACIÓN IMPORTANTE

        print(ruta_str)

        if not ruta_video.exists() or not ruta_video.is_file():
            todo_valido = f"❌ ERROR: No existe o no es un archivo: {ruta_video}"
            print(todo_valido)
            continue

        if not ruta_str.startswith(str(directorio).replace("\\", "/")):
            todo_valido = f"❌ ERROR: El archivo no está dentro del directorio base: {ruta_video}"
            print(todo_valido)
            continue

        if not pattern.search(ruta_str):
            todo_valido = f"❌ ERROR: La ruta no cumple con el formato esperado: {ruta_video}"
            print(todo_valido)

    return todo_valido




