from tkinter import filedialog
from pathlib import Path
from enumerador import obtener_camaras
from mensajes import *
from validadores import validar_ruta
from tabla import ReorderableTreeview

if __name__ == "__main__":

    directorio : Path = Path(filedialog.askdirectory())

    if not directorio != Path("."):
        show_error(NO_SELECCIONADO)
        exit()       

    if not any(directorio.iterdir()):
        show_error(VACIO)
        exit()
    
    if not validar_ruta(directorio):
        show_error(NO_CUMPLE_REQUISTOS)
        exit()
    
    nuevos_directorios = obtener_camaras(directorio)

    print(bool(nuevos_directorios))


    app = ReorderableTreeview(nuevos_directorios)
    
    app.mainloop()
    

