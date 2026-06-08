import sys
import os
from PyQt5.QtWidgets import QMessageBox

from vista_menu import VistaMenu
from modelo_menu import ModeloMenu


class ControladorMenu:

    def __init__(self, usuario_data=None):
        self.modelo = ModeloMenu()
        if usuario_data:
            self.modelo.set_usuario(usuario_data)

        self.vista_menu = VistaMenu()
        
        if usuario_data:
            nombre = usuario_data.get('nombre_completo') or usuario_data.get('usuario', 'Usuario')
            self.vista_menu.set_nombre_usuario(nombre)
        
        self.vista_menu.show()

        self.controlador_imagenes = None
        self.controlador_senales = None
        self.controlador_datos = None

        self.vista_menu.senal_imagenes.connect(self.abrir_imagenes)
        self.vista_menu.senal_senales.connect(self.abrir_senales)
        self.vista_menu.senal_datos.connect(self.abrir_datos)
        self.vista_menu.senal_cerrar_sesion.connect(self.cerrar_sesion)

    def abrir_imagenes(self):
        try:
            from vista_imagenes_medicas import VistaDicom
            from controlador_imagenes_medicas import ControladorDicom

            vista = VistaDicom()
            self.controlador_imagenes = ControladorDicom(vista)
            vista.show()
            self.vista_menu.hide()
        except Exception as e:
            self.vista_menu.mostrar_error("Error", f"No se pudo abrir el módulo de imágenes:\n{str(e)}")

    def abrir_senales(self):
        try:
            from Controlador import Controlador
            self.controlador_senales = Controlador()
            self.vista_menu.hide()
        except Exception as e:
            self.vista_menu.mostrar_error("Error", f"No se pudo abrir el módulo de señales:\n{str(e)}")

    def abrir_datos(self):
        try:
            from controlador_principal import ControladorPrincipal
            from vista import VistaTabular
            from modelo_tabular import ModeloTabular

            vista = VistaTabular()
            modelo = ModeloTabular()
            self.controlador_datos = ControladorPrincipal(vista, modelo)
            vista.show()
            self.vista_menu.hide()
        except Exception as e:
            self.vista_menu.mostrar_error("Error", f"No se pudo abrir el módulo de datos:\n{str(e)}")

    def cerrar_sesion(self):
        respuesta = QMessageBox.question(
            self.vista_menu, 
            "Confirmar", 
            "¿Está seguro que desea cerrar sesión?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            if self.controlador_imagenes:
                try:
                    self.controlador_imagenes.vista.close()
                except:
                    pass
            if self.controlador_senales:
                try:
                    self.controlador_senales.vista.close()
                except:
                    pass
            if self.controlador_datos:
                try:
                    self.controlador_datos.vista.close()
                except:
                    pass
            
            self.vista_menu.close()