import pandas as pd
import numpy as np

from PyQt5.QtCore import QObject, pyqtSignal


class ModeloTabular(QObject):

    datos_cargados = pyqtSignal(object)
    error_carga = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.datos = None

    def cargar_archivo(self, ruta):

        try:

            if ruta.endswith(".csv"):
                self.datos = pd.read_csv(ruta)

            elif ruta.endswith(".xlsx") or ruta.endswith(".xls"):
                self.datos = pd.read_excel(ruta)

            else:
                raise Exception("Formato no soportado")

            self.datos_cargados.emit(self.datos)

        except Exception as e:

            self.error_carga.emit(str(e))

    def obtener_columnas(self):

        if self.datos is None:
            return []

        return list(self.datos.columns)

    def mostrar_info_describe(self):

        if self.datos is None:
            return [], []

        numericas = self.datos.select_dtypes(
            include=np.number
        )

        describe = []

        for col in numericas.columns:

            describe.append({
                "Columna": col,
                "media": numericas[col].mean(),
                "std": numericas[col].std(),
                "min": numericas[col].min(),
                "max": numericas[col].max()
            })

        info = {
            "filas": self.datos.shape[0],
            "columnas": self.datos.shape[1]
        }

        return info, describe

    def graficar_columnas(self, columnas):

        if self.datos is None:
            return None

        resultado = {}

        for col in columnas:

            if col not in self.datos.columns:
                continue

            serie = pd.to_numeric(
                self.datos[col],
                errors="coerce"
            ).dropna()

            resultado[col] = {
                "x": np.arange(len(serie)),
                "y": serie.values,
                "media": serie.mean()
            }

        return resultado

    def scatter_plot(self, col_x, col_y):

        if self.datos is None:
            return None

        datos = self.datos[[col_x, col_y]].copy()

        datos[col_x] = pd.to_numeric(
            datos[col_x],
            errors="coerce"
        )

        datos[col_y] = pd.to_numeric(
            datos[col_y],
            errors="coerce"
        )

        datos = datos.dropna()

        if len(datos) == 0:

            return {
                "x": [],
                "y": [],
                "correlacion": 0
            }

        correlacion = datos[col_x].corr(
            datos[col_y]
        )

        return {
            "x": datos[col_x].values,
            "y": datos[col_y].values,
            "correlacion": correlacion
        }