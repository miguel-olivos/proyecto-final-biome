import numpy as np
import math
import cv2
from PyQt5 import QtWidgets
from modelo_imagenes_medicas import ModeloDicom, ModeloProcesamiento
from vista_imagenes_medicas import VistaDicom


class ControladorDicom:
    def __init__(self, vista):
        self.vista = vista
        self.modelo_dicom = None
        self.modelo_procesamiento = ModeloProcesamiento()
        
        self.imagen_actual = None
        self.imagen_normalizada = None
        self.imagen_segmentada = None
        self.imagen_morfologia = None
        
        self.corte_axial_actual = 0
        
        self.conectar_senales()
    
    def conectar_senales(self):
        self.vista.senal_cargar_dicom.connect(self.cargar_dicom)
        self.vista.senal_convertir_nifti.connect(self.convertir_nifti)
        self.vista.senal_guardar_csv.connect(self.guardar_csv)
        self.vista.senal_aplicar_zoom.connect(self.aplicar_zoom)
        self.vista.senal_segmentar.connect(self.segmentar)
        self.vista.senal_morfologia.connect(self.aplicar_morfologia)
        self.vista.senal_cambiar_corte_axial.connect(self.cambiar_corte_axial)
        self.vista.senal_cambiar_corte_sagital.connect(self.cambiar_corte_sagital)
        self.vista.senal_cambiar_corte_coronal.connect(self.cambiar_corte_coronal)
        self.vista.senal_volver_menu.connect(self.volver_menu)
    
    def cargar_dicom(self, ruta):
        try:
            self.modelo_dicom = ModeloDicom(ruta)
            datos = self.modelo_dicom.sacar_info()
            self.vista.mostrar_metadatos(datos)
            
            num_cortes_axiales = self.modelo_dicom.obtener_numero_cortes_axiales()
            num_cortes_sagitales = self.modelo_dicom.obtener_numero_cortes_sagitales()
            num_cortes_coronales = self.modelo_dicom.obtener_numero_cortes_coronales()
            
            print(f"Cortes axiales: {num_cortes_axiales}")
            print(f"Cortes sagitales: {num_cortes_sagitales}")
            print(f"Cortes coronales: {num_cortes_coronales}")
            
            if num_cortes_axiales > 0:
                self.vista.configurar_sliders(num_cortes_axiales, num_cortes_sagitales, num_cortes_coronales)
                
                # Mostrar el primer corte axial (índice 0)
                self.corte_axial_actual = 0
                self.cambiar_corte_axial(0)
                
                if num_cortes_sagitales > 0:
                    self.cambiar_corte_sagital(num_cortes_sagitales // 2)
                if num_cortes_coronales > 0:
                    self.cambiar_corte_coronal(num_cortes_coronales // 2)
                
                self.vista.mostrar_mensaje("Exito", f"DICOM cargado. {num_cortes_axiales} cortes disponibles.")
            else:
                self.vista.mostrar_error("Error", "El archivo DICOM no contiene cortes validos")
            
        except Exception as e:
            self.vista.mostrar_error("Error", f"No se pudo cargar:\n{str(e)}")
    
    def convertir_nifti(self, nombre):
        if not self.verificar_dicom_cargado():
            return
        try:
            mensaje = self.modelo_dicom.convertir_nifti(nombre)
            self.vista.mostrar_mensaje("Exito", mensaje)
        except Exception as e:
            self.vista.mostrar_error("Error", str(e))
    
    def guardar_csv(self, nombre):
        if not self.verificar_dicom_cargado():
            return
        try:
            self.modelo_dicom.guardar_info_csv(nombre)
            self.vista.mostrar_mensaje("Exito", f"Datos guardados en {nombre}")
        except Exception as e:
            self.vista.mostrar_error("Error", f"No se pudieron guardar los datos:\n{str(e)}")
    
    def aplicar_zoom(self, nombre, x, y, w, h):
        if not self.verificar_dicom_cargado():
            return
        
        if self.imagen_normalizada is None:
            self.vista.mostrar_error("Error", "Primero debe cargar una imagen")
            return
        
        try:
            recorte, zoom = self.modelo_procesamiento.hacer_zoom(
                self.imagen_normalizada, x, y, w, h
            )
            
            if recorte is not None and zoom is not None:
                original_pixmap = self.modelo_procesamiento.array_a_qpixmap(self.imagen_normalizada)
                zoom_pixmap = self.modelo_procesamiento.array_a_qpixmap(zoom)
                self.vista.mostrar_resultado_zoom(original_pixmap, zoom_pixmap)
                self.vista.mostrar_mensaje("Exito", "Zoom aplicado")
            else:
                self.vista.mostrar_error("Error", "No se pudo aplicar el zoom")
        except Exception as e:
            self.vista.mostrar_error("Error", f"Error al aplicar zoom:\n{str(e)}")
    
    def segmentar(self, nombre, tipo_binarizacion):
        if not self.verificar_dicom_cargado():
            return
        
        if self.imagen_normalizada is None:
            self.vista.mostrar_error("Error", "Primero debe cargar una imagen")
            return
        
        try:
            self.imagen_segmentada = self.modelo_procesamiento.segmentar(
                self.imagen_normalizada, tipo_binarizacion
            )
            if self.imagen_segmentada is not None:
                pixmap = self.modelo_procesamiento.array_a_qpixmap(self.imagen_segmentada)
                self.vista.mostrar_imagen_segmentada(pixmap)
                self.vista.mostrar_mensaje("Exito", "Segmentacion aplicada")
            else:
                self.vista.mostrar_error("Error", "No se pudo segmentar")
        except Exception as e:
            self.vista.mostrar_error("Error", f"Error al segmentar:\n{str(e)}")
    
    def aplicar_morfologia(self, nombre, tipo, kernel_size):
        if not self.verificar_dicom_cargado():
            return
        
        if self.imagen_segmentada is None:
            self.vista.mostrar_error("Error", "Primero debe aplicar segmentacion")
            return
        
        try:
            self.imagen_morfologia = self.modelo_procesamiento.morfologia(
                self.imagen_segmentada, tipo, kernel_size
            )
            if self.imagen_morfologia is not None:
                pixmap = self.modelo_procesamiento.array_a_qpixmap(self.imagen_morfologia)
                self.vista.mostrar_imagen_morfologia(pixmap)
                self.vista.mostrar_mensaje("Exito", f"Morfologia ({tipo}) aplicada")
            else:
                self.vista.mostrar_error("Error", "No se pudo aplicar morfologia")
        except Exception as e:
            self.vista.mostrar_error("Error", f"Error al aplicar morfologia:\n{str(e)}")
    
    def cambiar_corte_axial(self, indice):
        if not self.verificar_dicom_cargado():
            return
        
        try:
            print(f"Cambiando a corte axial: {indice}")
            
            self.corte_axial_actual = indice
            
            img = self.modelo_dicom.obtener_corte_axial(indice)
            
            if img is None:
                self.vista.mostrar_error("Error", f"No se pudo obtener el corte {indice}")
                return
            
            if len(img.shape) == 3:
                img = img[:, :, 0]
            
            self.imagen_actual = img
            self.imagen_normalizada = self.modelo_procesamiento.normalizar(img)
            
            if self.imagen_normalizada is not None:
                pixmap = self.modelo_procesamiento.array_a_qpixmap(self.imagen_normalizada)
                if pixmap is not None:
                    num_cortes = self.modelo_dicom.obtener_numero_cortes_axiales()
                    self.vista.mostrar_imagen_axial(pixmap, num_cortes, indice)
                    self.vista.mostrar_imagen_normalizada(pixmap)
                    
                    self.imagen_segmentada = None
                    self.imagen_morfologia = None
                    self.vista.limpiar_resultados()
            else:
                self.vista.mostrar_error("Error", "No se pudo normalizar la imagen")
                    
        except Exception as e:
            print(f"Error en corte axial: {e}")
            import traceback
            traceback.print_exc()
            self.vista.mostrar_error("Error", f"Error al cargar el corte:\n{str(e)}")
    
    def cambiar_corte_sagital(self, indice):
        if not self.verificar_dicom_cargado():
            return
        
        try:
            print(f"Cambiando a corte sagital: {indice}")
            
            img = self.modelo_dicom.obtener_corte_sagital(indice)
            if img is not None:
                img_normalizada = self.modelo_procesamiento.normalizar(img)
                if img_normalizada is not None:
                    pixmap = self.modelo_procesamiento.array_a_qpixmap(img_normalizada)
                    if pixmap is not None:
                        self.vista.mostrar_imagen_sagital(pixmap)
        except Exception as e:
            print(f"Error en corte sagital: {e}")
    
    def cambiar_corte_coronal(self, indice):
        if not self.verificar_dicom_cargado():
            return
        
        try:
            print(f"Cambiando a corte coronal: {indice}")
            
            img = self.modelo_dicom.obtener_corte_coronal(indice)
            if img is not None:
                img_normalizada = self.modelo_procesamiento.normalizar(img)
                if img_normalizada is not None:
                    pixmap = self.modelo_procesamiento.array_a_qpixmap(img_normalizada)
                    if pixmap is not None:
                        self.vista.mostrar_imagen_coronal(pixmap)
        except Exception as e:
            print(f"Error en corte coronal: {e}")
    
    def volver_menu(self):
        respuesta = QtWidgets.QMessageBox.question(
            self.vista,
            "Confirmar",
            "Desea volver al menu principal?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if respuesta == QtWidgets.QMessageBox.Yes:
            self.vista.close()
    
    def verificar_dicom_cargado(self):
        if self.modelo_dicom is None:
            self.vista.mostrar_error("Error", "No hay archivo DICOM cargado")
            return False
        if self.modelo_dicom.matriz3D is None:
            self.vista.mostrar_error("Error", "La matriz 3D no esta disponible")
            return False
        if len(self.modelo_dicom.matriz3D) == 0:
            self.vista.mostrar_error("Error", "El archivo DICOM no contiene datos")
            return False
        return True