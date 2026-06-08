import numpy as np
from scipy.io import *
import matplotlib 

class senal:
    def __init__(self):
        self.senal3D = None
        self.senal2D = None

    def cargar_mat(self, ruta):

        info = whosmat(ruta)

        nombre_variable = None

        for nombre, shape, tipo in info:

            if len(shape) == 3:
                nombre_variable = nombre
                break

        if nombre_variable is None:
            raise ValueError("No existe una matriz 3D en el archivo.")

        datos = loadmat(ruta)

        self.senal3D = datos[nombre_variable]
        self.convertir_2D()
    
    def convertir_2D(self):
        forma = self.senal3D.shape
        self.senal2D = self.senal3D.reshape(forma[0],forma[1] * forma[2])

    def seleccionar_canales(self, inicio, fin):
        if inicio < 0 or fin >= self.senal2D.shape[0]:
            raise ValueError("Canal fuera de rango")

        if inicio > fin:
            raise ValueError("El canal inicial debe ser menor")
        
        return self.senal2D[inicio:fin+1]
    
    def agregar_ruido(self, canal, sigma):
        
        if canal >= self.senal2D.shape[0]:
            raise ValueError("Canal inválido")

        original = self.senal2D[canal].copy()
        ruido = np.random.normal(0, sigma, original.shape)
        modificada = original + ruido
        return original, modificada
    
    def calcular_estadisticas(self, eje):

        promedio = np.mean(self.senal3D,axis=eje)
        desviacion = np.std(self.senal3D,axis=eje)
        return promedio, desviacion

