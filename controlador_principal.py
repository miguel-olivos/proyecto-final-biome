from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMessageBox


class ControladorPrincipal(QObject):

    def __init__(self, vista_tabular, modelo_tabular):
        super().__init__()

        self.vista = vista_tabular
        self.modelo = modelo_tabular

        self.conectar_senales()

    def conectar_senales(self):

        # Vista -> Controlador
        self.vista.archivo_cargado.connect(
            self.cargar_archivo
        )

        self.vista.graficar_columnas.connect(
            self.generar_graficos
        )

        self.vista.hacer_scatter.connect(
            self.generar_scatter
        )

        # Modelo -> Controlador
        self.modelo.datos_cargados.connect(
            self.on_datos_cargados
        )

        self.modelo.error_carga.connect(
            self.vista.mostrar_error
        )

    def cargar_archivo(self, ruta):

        self.modelo.cargar_archivo(ruta)

    def on_datos_cargados(self, datos):

        try:

            columnas = self.modelo.obtener_columnas()

            self.vista.actualizar_columnas(
                columnas
            )

            info, describe = (
                self.modelo.mostrar_info_describe()
            )

            self.vista.mostrar_info_describe(
                info,
                describe
            )

            QMessageBox.information(
                self.vista,
                "Archivo cargado",
                f"Se cargaron {datos.shape[0]} filas y {datos.shape[1]} columnas"
            )

        except Exception as e:

            self.vista.mostrar_error(
                str(e)
            )

    def generar_graficos(self, columnas):

        try:

            datos = self.modelo.graficar_columnas(
                columnas
            )

            self.vista.dibujar_graficos(
                datos
            )

        except Exception as e:

            self.vista.mostrar_error(
                str(e)
            )

    def generar_scatter(self, columna_x, columna_y):

        try:

            datos = self.modelo.scatter_plot(
                columna_x,
                columna_y
            )

            self.vista.mostrar_scatter(
                datos
            )

        except Exception as e:

            self.vista.mostrar_error(
                str(e)
            )