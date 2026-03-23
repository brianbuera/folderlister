from funciones import obtener_camaras
from mensajes import *
from interfaz import ListaDeCamaras
from seleccionar_directorio import seleccionar_directorio

if __name__ == "__main__":
    directorio =  seleccionar_directorio()
    if not directorio:
        exit()
    directorios_camaras = obtener_camaras(directorio)
    app = ListaDeCamaras(directorios_camaras)
    app.geometry("600x400")
    app.attributes('-topmost',True)
    app.mainloop()
    

