import os
import random
import json
from datetime import datetime, timedelta

# Clase para manejar fechas
class Fecha:
    def __init__(self, dia=None, mes=None, anio=None):
        if dia is None or mes is None or anio is None:
            hoy = datetime.now()
            self.dia = hoy.day
            self.mes = hoy.month
            self.anio = hoy.year
        else:
            self.dia = dia
            self.mes = mes
            self.anio = anio

    def __str__(self):
        return f"{self.dia:02d}/{self.mes:02d}/{self.anio}"

    def __add__(self, dias):
        fecha = datetime(self.anio, self.mes, self.dia) + timedelta(days=dias)
        return Fecha(fecha.day, fecha.month, fecha.year)

    def __eq__(self, otra_fecha):
        return self.dia == otra_fecha.dia and self.mes == otra_fecha.mes and self.anio == otra_fecha.anio

    def calcular_diferencia(self, otra_fecha):
        fecha_actual = datetime(self.anio, self.mes, self.dia)
        otra_fecha_dt = datetime(otra_fecha.anio, otra_fecha.mes, otra_fecha.dia)
        diferencia = abs((otra_fecha_dt - fecha_actual).days)
        return diferencia

# Clase para datos de alumnos
class Alumno(dict):
    def __init__(self, nombre, dni, fecha_ingreso, carrera):
        super().__init__(Nombre=nombre, DNI=dni, FechaIngreso=fecha_ingreso, Carrera=carrera)

    def cambiar_datos(self, **kwargs):
        for clave, valor in kwargs.items():
            if clave in self:
                self[clave] = valor

    def calcular_antiguedad(self):
        fecha_ingreso = self["FechaIngreso"]
        fecha_actual = Fecha()
        antiguedad_anios = fecha_ingreso.calcular_diferencia(fecha_actual) // 365
        return antiguedad_anios

    def __str__(self):
        return f"Nombre: {self['Nombre']}, DNI: {self['DNI']}, Fecha de Ingreso: {self['FechaIngreso']}, Carrera: {self['Carrera']}"

    def __eq__(self, otro_alumno):
        return self["DNI"] == otro_alumno["DNI"]

# Clase para nodos de la lista doblemente enlazada
class Nodo:
    def __init__(self, dato=None):
        self.dato = dato
        self.siguiente = None
        self.anterior = None

# Clase para la lista doblemente enlazada de alumnos
class ListaDoblementeEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def insertar_al_final(self, dato):
        nuevo_nodo = Nodo(dato)
        if not self.cabeza:
            self.cabeza = self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.cola
            self.cola = nuevo_nodo

    def __iter__(self):
        self.actual = self.cabeza
        return self

    def __next__(self):
        if not self.actual:
            raise StopIteration
        dato = self.actual.dato
        self.actual = self.actual.siguiente
        return dato

    def cargar_lista_ejemplo(self, num_alumnos=5):
        nombres = ["Juan", "María", "Pedro", "Ana", "Luis"]
        carreras = ["Ingeniería", "Medicina", "Derecho", "Arquitectura", "Economía"]
        
        for _ in range(num_alumnos):
            nombre = random.choice(nombres)
            dni = random.randint(10000000, 99999999)
            fecha_ingreso = Fecha(random.randint(1, 28), random.randint(1, 12), random.randint(2000, 2023))
            carrera = random.choice(carreras)
            alumno = Alumno(nombre, dni, fecha_ingreso, carrera)
            self.insertar_al_final(alumno)

    def ordenar_por_fecha_ingreso(self):
        if not self.cabeza or not self.cabeza.siguiente:
            return

        nodo_actual = self.cabeza.siguiente
        while nodo_actual:
            clave = nodo_actual
            mover_nodo = nodo_actual.anterior

            while mover_nodo and clave.dato["FechaIngreso"].calcular_diferencia(Fecha(1, 1, 2000)) < mover_nodo.dato["FechaIngreso"].calcular_diferencia(Fecha(1, 1, 2000)):
                mover_nodo = mover_nodo.anterior

            siguiente_nodo = clave.siguiente

            if clave.anterior:
                clave.anterior.siguiente = clave.siguiente
            if clave.siguiente:
                clave.siguiente.anterior = clave.anterior

            if not mover_nodo:
                clave.siguiente = self.cabeza
                self.cabeza.anterior = clave
                self.cabeza = clave
                clave.anterior = None
            else:
                clave.siguiente = mover_nodo.siguiente
                clave.anterior = mover_nodo
                if mover_nodo.siguiente:
                    mover_nodo.siguiente.anterior = clave
                mover_nodo.siguiente = clave
                if clave.siguiente is None:
                    self.cola = clave

            nodo_actual = siguiente_nodo

# Función para crear un directorio, guardar la lista de alumnos en un archivo JSON y mover el directorio
def crear_guardar_lista_alumnos(directorio):
    if not os.path.exists(directorio):
        os.makedirs(directorio)

    lista_alumnos = ListaDoblementeEnlazada()
    lista_alumnos.cargar_lista_ejemplo(5)

    archivo = os.path.join(directorio, 'lista_alumnos.json')
    with open(archivo, 'w') as f:
        for alumno in lista_alumnos:
            json.dump(alumno, f, default=lambda x: x.__dict__)
            f.write('\n')
    
    return archivo

# Función para mover un directorio a una nueva ruta y borrar el archivo y el directorio
def mover_borrar_directorio_archivo(directorio_origen, directorio_destino):
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
    os.replace(directorio_origen, directorio_destino)

    archivo = os.path.join(directorio_destino, 'lista_alumnos.json')
    os.remove(archivo)
    os.rmdir(directorio_destino)

# Función principal para el ejemplo y uso de la lista doblemente enlazada de alumnos
def main():
    directorio_origen = './lista_alumnos_origen'
    directorio_destino = './lista_alumnos_destino'

    try:
        archivo_guardado = crear_guardar_lista_alumnos(directorio_origen)
        print(f"Se ha guardado la lista de alumnos en: {archivo_guardado}")

        mover_borrar_directorio_archivo(directorio_origen, directorio_destino)
        print(f"El directorio se ha movido a: {directorio_destino}, y los archivos/directorios han sido eliminados.")
    
    except Exception as e:
        print(f"Se ha producido un error: {e}")

    lista_alumnos = ListaDoblementeEnlazada()
    lista_alumnos.cargar_lista_ejemplo(5)

    print("\nLista de alumnos antes de ordenar:")
    for alumno in lista_alumnos:
        print(alumno)

    lista_alumnos.ordenar_por_fecha_ingreso()

    print("\nLista de alumnos después de ordenar por fecha de ingreso:")
    for alumno in lista_alumnos:
        print(alumno)

if __name__ == "__main__":
    main()




