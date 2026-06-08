import os
print(os.getcwd())


from Modelo import senal
from Vistas import VistaSenales
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap

import matplotlib.pyplot as plt


class Controlador:

    def __init__(self):

        self.modelo = senal()
        self.vista = VistaSenales()

        self.vista.botoncargararchivomat.clicked.connect(
            self.cargar_archivo
        )

        self.vista.botonmostrarcanales.clicked.connect(
            self.mostrar_canales
        )

        self.vista.botonagregar.clicked.connect(
            self.agregar_ruido
        )

        self.vista.botoncalcularygrafi.clicked.connect(
            self.calcular_estadisticas
        )

        # Ajustar imágenes a los QLabel
        self.vista.canalesseleccionado.setScaledContents(True)

        self.vista.canaloriginal.setScaledContents(True)
        self.vista.canalruido.setScaledContents(True)

        self.vista.canaloriginal_3.setScaledContents(True)
        self.vista.canalruido_3.setScaledContents(True)

        self.vista.show()

    def cargar_archivo(self):

        ruta, _ = QFileDialog.getOpenFileName(self.vista, "Abrir archivo MAT", "", "MAT (*.mat)")

        if ruta:

            try:

                self.modelo.cargar_mat(ruta)

                QMessageBox.information(
                    self.vista,
                    "Correcto",
                    "Archivo cargado exitosamente"
                )

            except Exception as e:

                QMessageBox.critical(
                    self.vista,
                    "Error",
                    str(e)
                )

    def mostrar_canales(self):

        try:

            inicio = self.vista.obtener_canal_inicio()
            fin = self.vista.obtener_canal_fin()

            canales = self.modelo.seleccionar_canales(
                inicio,
                fin
            )

            plt.figure(figsize=(8,4))

            for canal in canales:
                plt.plot(canal)

            plt.title("Canales seleccionados")
            plt.xlabel("Muestras")
            plt.ylabel("Amplitud")

            plt.tight_layout()
            plt.savefig("canales.png")
            plt.close()

            self.vista.canalesseleccionado.setPixmap(
                QPixmap("canales.png")
            )

        except Exception as e:

            QMessageBox.critical(
                self.vista,
                "Error",
                str(e)
            )

    def agregar_ruido(self):

        try:

            canal = self.vista.obtener_canal_ruido()
            sigma = self.vista.obtener_sigma()

            original, modificada = (
                self.modelo.agregar_ruido(
                    canal,
                    sigma
                )
            )

            # ORIGINAL

            plt.figure(figsize=(6,3))
            plt.plot(original)

            plt.title("Canal original")
            plt.xlabel("Muestras")
            plt.ylabel("Amplitud")

            plt.tight_layout()
            plt.savefig("original.png")
            plt.close()

            self.vista.canaloriginal.setPixmap(
                QPixmap("original.png")
            )

            # CON RUIDO

            plt.figure(figsize=(6,3))
            plt.plot(modificada)

            plt.title("Canal con ruido")
            plt.xlabel("Muestras")
            plt.ylabel("Amplitud")

            plt.tight_layout()
            plt.savefig("ruido.png")
            plt.close()

            self.vista.canalruido.setPixmap(
                QPixmap("ruido.png")
            )

        except Exception as e:

            QMessageBox.critical(
                self.vista,
                "Error",
                str(e)
            )

    def calcular_estadisticas(self):

        try:

            eje = self.vista.obtener_eje()

            promedio, desviacion = (
                self.modelo.calcular_estadisticas(
                    eje
                )
            )

            # PROMEDIO

            plt.figure(figsize=(6,3))

            plt.plot(
                promedio.flatten()
            )

            plt.title("Promedio")
            plt.xlabel("Índice")

            plt.tight_layout()
            plt.savefig("promedio.png")
            plt.close()

            self.vista.canaloriginal_3.setPixmap(
                QPixmap("promedio.png")
            )

            # DESVIACIÓN

            plt.figure(figsize=(6,3))

            plt.plot(
                desviacion.flatten()
            )

            plt.title("Desviación estándar")
            plt.xlabel("Índice")

            plt.tight_layout()
            plt.savefig("desviacion.png")
            plt.close()

            self.vista.canalruido_3.setPixmap(
                QPixmap("desviacion.png")
            )

        except Exception as e:

            QMessageBox.critical(
                self.vista,
                "Error",
                str(e)
            )