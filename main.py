from tkinter import filedialog
from pathlib import Path
from enumerador import enumerar
from mensajes import *
from validadores import validar_ruta



if __name__ == "__main__":

    directorio : Path = Path(filedialog.askdirectory())

    if not directorio:
        show_error(NO_SELECCIONADO)
        exit()       

    if not any(directorio.iterdir()):
        show_error(VACIO)
        exit()
    
    if not validar_ruta(directorio):
        show_error(NO_CUMPLE_REQUISTOS)
        exit()
    
    enumerar(directorio)

