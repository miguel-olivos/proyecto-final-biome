from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class VistaSenales(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi("ventana_señales.ui", self)
        
    def obtener_canal_inicio(self):
        return int(self.campocanalinicio.text())

    def obtener_canal_fin(self):
        return int(self.campocanalfin.text())

    def obtener_canal_ruido(self):
        return self.SelCanal.value()

    def obtener_sigma(self):
        return self.SelRuido.value()
    
    def obtener_eje(self):

        if self.radioButtoneje0.isChecked():
            return 0

        elif self.radioButton_eje1.isChecked():
            return 1

        elif self.radioButton_eje2.isChecked():
            return 2
