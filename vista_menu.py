from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
import os


class VistaMenu(QMainWindow):
 
    senal_imagenes = pyqtSignal()
    senal_senales = pyqtSignal()
    senal_datos = pyqtSignal()
    senal_cerrar_sesion = pyqtSignal()
 
    def __init__(self):
        super().__init__()
        
        ruta_ui = os.path.join(os.path.dirname(__file__), 'interfaz', 'ventana_menu.ui')
        uic.loadUi(ruta_ui, self)
        
        if hasattr(self, 'imagenesm_menu'):
            self.imagenesm_menu.clicked.connect(self.senal_imagenes.emit)
        
        if hasattr(self, 'senales_menu'):
            self.senales_menu.clicked.connect(self.senal_senales.emit)
        
        if hasattr(self, 'datosc_menu'):
            self.datosc_menu.clicked.connect(self.senal_datos.emit)
        
        if hasattr(self, 'cerrars_menu'):
            try:
                self.cerrars_menu.clicked.disconnect()
            except:
                pass
            self.cerrars_menu.clicked.connect(self.senal_cerrar_sesion.emit)
        
        self.setWindowTitle("BioMed - Menú Principal")
    
    def set_nombre_usuario(self, nombre):
        if hasattr(self, 'textoBienvenido_menu'):
            self.textoBienvenido_menu.setText(f"Bienvenido, {nombre}")
    
    def mostrar_mensaje(self, titulo, mensaje):
        QMessageBox.information(self, titulo, mensaje)
    
    def mostrar_error(self, titulo, error):
        QMessageBox.critical(self, titulo, error)