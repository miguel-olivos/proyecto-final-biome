from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
import os


class VistaDicom(QtWidgets.QMainWindow):
    senal_cargar_dicom = pyqtSignal(str)
    senal_convertir_nifti = pyqtSignal(str)
    senal_guardar_csv = pyqtSignal(str)
    senal_aplicar_zoom = pyqtSignal(str, int, int, int, int)
    senal_segmentar = pyqtSignal(str, str)
    senal_morfologia = pyqtSignal(str, str, int)
    senal_cambiar_corte_axial = pyqtSignal(int)
    senal_cambiar_corte_sagital = pyqtSignal(int)
    senal_cambiar_corte_coronal = pyqtSignal(int)
    senal_volver_menu = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        uic.loadUi("ventana_imagenes_medicas.ui", self)
        self.conectar_signales_ui()
    
    def conectar_signales_ui(self):
        self.botoncargar_DICOM.clicked.connect(self.on_cargar_dicom)
        self.botonconvertir_NIFTI.clicked.connect(self.on_convertir_nifti)
        self.botonGdatos_CSV.clicked.connect(self.on_guardar_csv)
        self.botonzoom_img.clicked.connect(self.on_aplicar_zoom)
        self.botonsegmentar_img.clicked.connect(self.on_segmentar)
        self.botonaplicar_img.clicked.connect(self.on_morfologia)
        self.slidercorteaxial_img.valueChanged.connect(self.on_corte_axial_changed)
        self.slidercortesagital_img.valueChanged.connect(self.on_corte_sagital_changed)
        self.slidercortecoronal_img.valueChanged.connect(self.on_corte_coronal_changed)
        self.botonvolver_img.clicked.connect(self.on_volver_menu)
    
    def on_cargar_dicom(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Abrir DICOM", "", "DICOM Files (*.dcm)")
        if ruta:
            self.senal_cargar_dicom.emit(ruta)
    
    def on_convertir_nifti(self):
        nombre = self.camponombrei_img.text().strip()
        if not nombre:
            nombre = "imagen_convertida"
        self.senal_convertir_nifti.emit(nombre)
    
    def on_guardar_csv(self):
        self.senal_guardar_csv.emit("info_dicom.csv")
    
    def on_aplicar_zoom(self):
        nombre = self.camponombrei_img.text().strip()
        self.senal_aplicar_zoom.emit(nombre, 50, 50, 100, 100)
    
    def on_segmentar(self):
        tipo = self.combobinarizacion_img.currentText()
        self.senal_segmentar.emit("segmentada", tipo)
    
    def on_morfologia(self):
        tipo = self.combomorfologia_img.currentText()
        kernel = self.spinkernel_img.value()
        if kernel % 2 == 0:
            kernel += 1
        self.senal_morfologia.emit("morfo", tipo, kernel)
    
    def on_corte_axial_changed(self, valor):
        self.senal_cambiar_corte_axial.emit(valor)
    
    def on_corte_sagital_changed(self, valor):
        self.senal_cambiar_corte_sagital.emit(valor)
    
    def on_corte_coronal_changed(self, valor):
        self.senal_cambiar_corte_coronal.emit(valor)
    
    def on_volver_menu(self):
        self.senal_volver_menu.emit()
    
    def mostrar_metadatos(self, datos):
        self.tablametadatos_img.setItem(0, 0, QTableWidgetItem(str(datos.get("FechaEstudio", "N/A"))))
        self.tablametadatos_img.setItem(1, 0, QTableWidgetItem(str(datos.get("HoraEstudio", "N/A"))))
        self.tablametadatos_img.setItem(2, 0, QTableWidgetItem(str(datos.get("Modalidad", "N/A"))))
        self.tablametadatos_img.setItem(3, 0, QTableWidgetItem(str(datos.get("Descripcion", "N/A"))))
        self.tablametadatos_img.setItem(4, 0, QTableWidgetItem(str(datos.get("HoraSerie", "N/A"))))
        self.tablametadatos_img.setItem(5, 0, QTableWidgetItem(str(datos.get("Duracion", "N/A"))))
        self.tablametadatos_img.setItem(6, 0, QTableWidgetItem(str(datos.get("Fabricante", "N/A"))))
    
    def mostrar_imagen_axial(self, pixmap, num_cortes, corte_actual):
        if pixmap is not None:
            self.imagencorteaxial_img.setPixmap(pixmap)
            self.slidercorteaxial_img.setMaximum(num_cortes - 1)
            self.slidercorteaxial_img.setValue(corte_actual)
    
    def mostrar_imagen_sagital(self, pixmap):
        if pixmap is not None:
            self.imagencortesagital_img.setPixmap(pixmap.scaled(161, 151))
    
    def mostrar_imagen_coronal(self, pixmap):
        if pixmap is not None:
            self.imagencortecoronal_img.setPixmap(pixmap.scaled(161, 151))
    
    def mostrar_resultado_zoom(self, original_pixmap, zoom_pixmap):
        if original_pixmap is not None:
            self.imagenoriginal.setPixmap(original_pixmap.scaled(131, 151))
        if zoom_pixmap is not None:
            self.regionrecortada.setPixmap(zoom_pixmap.scaled(131, 151))
    
    def mostrar_imagen_normalizada(self, pixmap):
        if pixmap is not None:
            self.imagennormalizada.setPixmap(pixmap.scaled(131, 151))
    
    def mostrar_imagen_segmentada(self, pixmap):
        if pixmap is not None:
            self.imgsegmentada.setPixmap(pixmap.scaled(131, 151))
    
    def mostrar_imagen_morfologia(self, pixmap):
        if pixmap is not None:
            self.imgtransformacionmorfo.setPixmap(pixmap.scaled(131, 151))
    
    def limpiar_resultados(self):
        self.imagenoriginal.setText("IMAGEN ORIGINAL")
        self.regionrecortada.setText("REGION RECORTADA")
        self.imagennormalizada.setText("NORMALIZADA UINT8")
        self.imgsegmentada.setText("SEGMENTACION")
        self.imgtransformacionmorfo.setText("MORFOLOGIA")
    
    def mostrar_mensaje(self, titulo, mensaje):
        QtWidgets.QMessageBox.information(self, titulo, mensaje)
    
    def mostrar_error(self, titulo, error):
        QtWidgets.QMessageBox.critical(self, titulo, error)
    
    def configurar_sliders(self, num_cortes_axiales, num_cortes_sagitales, num_cortes_coronales):
        self.slidercorteaxial_img.setMaximum(max(0, num_cortes_axiales - 1))
        self.slidercortesagital_img.setMaximum(max(0, num_cortes_sagitales - 1))
        self.slidercortecoronal_img.setMaximum(max(0, num_cortes_coronales - 1))