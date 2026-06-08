import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QFileDialog,
    QMessageBox,
    QVBoxLayout,
    QTableWidgetItem
)

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class VistaTabular(QMainWindow):

    archivo_cargado = pyqtSignal(str)
    graficar_columnas = pyqtSignal(list)
    hacer_scatter = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        
        uic.loadUi("ventana_datos.ui", self)

        self.inicializar_grafico_scatter()
        self.conectar_botones()

    def inicializar_grafico_scatter(self):

        self.figura = plt.figure(figsize=(8, 4))
        self.canvas = FigureCanvasQTAgg(self.figura)

        layout = QVBoxLayout()

        self.framecomparacion_datos.setLayout(layout)
        layout.addWidget(self.canvas)

        self.graficocomparacion_datos.hide()

    def conectar_botones(self):

        self.botoncargararchivoCSV.clicked.connect(
            self.seleccionar_archivo
        )

        self.botonvergrafi.clicked.connect(
            self.obtener_columnas_seleccionadas
        )

        self.botongraficar.clicked.connect(
            self.obtener_scatter
        )

    def seleccionar_archivo(self):

        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo",
            "",
            "CSV (*.csv);;Excel (*.xlsx *.xls)"
        )

        if ruta:
            self.archivo_cargado.emit(ruta)

    def actualizar_columnas(self, columnas):

        self.listacolumnas.clear()

        self.comboejex.clear()
        self.comboejey.clear()

        for columna in columnas:

            self.listacolumnas.addItem(columna)

            self.comboejex.addItem(columna)
            self.comboejey.addItem(columna)

    def obtener_columnas_seleccionadas(self):

        columnas = []

        for item in self.listacolumnas.selectedItems():
            columnas.append(item.text())

        if len(columnas) < 4:

            QMessageBox.warning(
                self,
                "Advertencia",
                "Debe seleccionar mínimo 4 columnas"
            )

            return

        self.graficar_columnas.emit(
            columnas[:4]
        )

    def obtener_scatter(self):

        x = self.comboejex.currentText()
        y = self.comboejey.currentText()

        if x == y:

            QMessageBox.warning(
                self,
                "Advertencia",
                "Seleccione columnas diferentes"
            )

            return

        self.hacer_scatter.emit(
            x,
            y
        )

    def dibujar_graficos(self, datos):

        frames = [
            self.framegrafico1,
            self.framegrafico2,
            self.framegrafico3,
            self.framegrafico4
        ]

        for frame in frames:

            if frame.layout() is None:
                frame.setLayout(QVBoxLayout())

            while frame.layout().count():

                item = frame.layout().takeAt(0)

                if item.widget():
                    item.widget().deleteLater()

        for i, (columna, info) in enumerate(datos.items()):

            figura = plt.figure(figsize=(3, 2))

            canvas = FigureCanvasQTAgg(figura)

            ax = figura.add_subplot(111)

            ax.plot(
                info["x"],
                info["y"]
            )

            ax.set_title(columna)

            figura.tight_layout()

            frames[i].layout().addWidget(canvas)

    def mostrar_scatter(self, datos):

        self.figura.clear()

        ax = self.figura.add_subplot(111)

        ax.scatter(
            datos["x"],
            datos["y"]
        )

        ax.set_title(
            f"Correlación = {datos['correlacion']:.3f}"
        )

        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        ax.grid(True)

        self.canvas.draw()

    def mostrar_info_describe(self, info, describe):

        self.tabladatosarchivo.setRowCount(
            len(describe)
        )

        for fila, dato in enumerate(describe):

            self.tabladatosarchivo.setItem(
                fila,
                0,
                QTableWidgetItem(
                    str(dato["Columna"])
                )
            )

            self.tabladatosarchivo.setItem(
                fila,
                1,
                QTableWidgetItem("Numérico")
            )

            self.tabladatosarchivo.setItem(
                fila,
                2,
                QTableWidgetItem(
                    f"{dato['media']:.2f}"
                )
            )

            self.tabladatosarchivo.setItem(
                fila,
                3,
                QTableWidgetItem(
                    f"{dato['std']:.2f}"
                )
            )

            self.tabladatosarchivo.setItem(
                fila,
                4,
                QTableWidgetItem(
                    f"{dato['min']:.2f}"
                )
            )

            self.tabladatosarchivo.setItem(
                fila,
                5,
                QTableWidgetItem(
                    f"{dato['max']:.2f}"
                )
            )

    def mostrar_error(self, mensaje):

        QMessageBox.critical(
            self,
            "Error",
            mensaje
        )