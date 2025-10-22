from tkinter import filedialog
from pathlib import Path
from enumerador import enumerar
from mensajes import *

if __name__ == "__main__":
    directorio = filedialog.askdirectory()
    if directorio:
        enumerar(Path(directorio))
    else:
       show_error(NO_SELECCIONADO)