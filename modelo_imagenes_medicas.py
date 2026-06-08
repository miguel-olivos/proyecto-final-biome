import numpy as np
import pydicom
import pandas as pd
import cv2
import math
from PyQt5.QtGui import QPixmap, QImage

class ModeloDicom:
    def __init__(self, ruta=None):
        self.dicom = None
        self.matriz3D = None
        self.ruta_actual = None
        if ruta:
            self.cargar_dicom(ruta)
    
    def cargar_dicom(self, ruta):
        self.dicom = pydicom.dcmread(ruta)
        pixel_array = self.dicom.pixel_array
        
        print(f"Pixel array original - Forma: {pixel_array.shape}, Dimensiones: {len(pixel_array.shape)}")
        
        self.matriz3D = self._procesar_pixel_array(pixel_array)
        
        return True
    
    def _procesar_pixel_array(self, pixel_array):
        if len(pixel_array.shape) == 3:
            print("Formato 3D detectado - Multiples cortes")
            return pixel_array
        elif len(pixel_array.shape) == 2:
            print("Formato 2D detectado - Un solo corte")
            return pixel_array.reshape(1, pixel_array.shape[0], pixel_array.shape[1])
        elif len(pixel_array.shape) == 1:
            print("Formato 1D detectado - Convirtiendo a 2D...")
            size = len(pixel_array)
            posibles_tamanos = [512, 256, 128, 64, 32, 16, 8]
            
            for lado in posibles_tamanos:
                if size == lado * lado:
                    imagen_2d = pixel_array.reshape(lado, lado)
                    print(f"  Convertido a {lado}x{lado}")
                    return imagen_2d.reshape(1, lado, lado)
            
            factores = []
            for i in range(1, int(math.sqrt(size)) + 1):
                if size % i == 0:
                    factores.append((i, size // i))
            
            if factores:
                alto, ancho = factores[-1]
                imagen_2d = pixel_array.reshape(alto, ancho)
                print(f"  Convertido a {alto}x{ancho}")
                return imagen_2d.reshape(1, alto, ancho)
            
            lado = int(math.ceil(math.sqrt(size)))
            imagen_2d = np.zeros((lado, lado), dtype=pixel_array.dtype)
            imagen_2d[:size] = pixel_array
            print(f"  Padding a {lado}x{lado}")
            return imagen_2d.reshape(1, lado, lado)
        elif len(pixel_array.shape) == 0:
            print("Formato 0D detectado - Un solo pixel")
            return np.array([[[pixel_array]]])
        else:
            print(f"Formato desconocido: {pixel_array.shape}")
            return np.zeros((1, 100, 100), dtype=np.uint8)
    
    def sacar_info(self):
        datos = {
            "FechaEstudio": getattr(self.dicom, "StudyDate", "N/A"),
            "HoraEstudio": getattr(self.dicom, "StudyTime", "N/A"),
            "Modalidad": getattr(self.dicom, "Modality", "N/A"),
            "Descripcion": getattr(self.dicom, "StudyDescription", "N/A"),
            "HoraSerie": getattr(self.dicom, "SeriesTime", "N/A"),
            "Fabricante": getattr(self.dicom, "Manufacturer", "N/A")
        }
        try:
            if datos["HoraEstudio"] != "N/A" and datos["HoraSerie"] != "N/A":
                hora_estudio = int(datos["HoraEstudio"][:6])
                hora_serie = int(datos["HoraSerie"][:6])
                datos["Duracion"] = abs(hora_serie - hora_estudio)
            else:
                datos["Duracion"] = "N/A"
        except:
            datos["Duracion"] = "N/A"
        return datos
    
    def guardar_info_csv(self, nombre="info_dicom.csv"):
        df = pd.DataFrame([self.sacar_info()])
        df.to_csv(nombre, index=False)
    
    def convertir_nifti(self, nombre="imagen_convertida"):
        try:
            np.save(f"{nombre}.npy", self.matriz3D)
            return f"Guardado como {nombre}.npy"
        except Exception as e:
            raise Exception(f"Error al convertir: {str(e)}")
    
    def obtener_corte_axial(self, indice):
        if self.matriz3D is not None and indice < len(self.matriz3D):
            corte = self.matriz3D[indice]
            if len(corte.shape) == 3:
                corte = corte[:, :, 0]
            return corte
        return None
    
    def obtener_corte_sagital(self, indice):
        if self.matriz3D is not None and len(self.matriz3D.shape) == 3:
            if indice < self.matriz3D.shape[1]:
                return self.matriz3D[:, indice, :]
        return None
    
    def obtener_corte_coronal(self, indice):
        if self.matriz3D is not None and len(self.matriz3D.shape) == 3:
            if indice < self.matriz3D.shape[2]:
                return self.matriz3D[:, :, indice]
        return None
    
    def obtener_numero_cortes_axiales(self):
        return len(self.matriz3D) if self.matriz3D is not None else 0
    
    def obtener_numero_cortes_sagitales(self):
        if self.matriz3D is not None and len(self.matriz3D.shape) == 3:
            return self.matriz3D.shape[1]
        return 0
    
    def obtener_numero_cortes_coronales(self):
        if self.matriz3D is not None and len(self.matriz3D.shape) == 3:
            return self.matriz3D.shape[2]
        return 0


class ModeloProcesamiento:
    @staticmethod
    def normalizar(img):
        if img is None:
            return None
        
        if len(img.shape) == 3:
            img = img[:, :, 0]
        elif len(img.shape) == 1:
            size = len(img)
            lado = int(math.sqrt(size))
            if lado * lado == size:
                img = img.reshape(lado, lado)
            else:
                for i in range(1, int(math.sqrt(size)) + 1):
                    if size % i == 0:
                        img = img.reshape(i, size // i)
                        break
                else:
                    return None
        elif len(img.shape) == 0:
            return None
        
        if len(img.shape) != 2:
            return None
        
        img_min = np.min(img)
        img_max = np.max(img)
        
        if img_max - img_min == 0:
            return np.zeros_like(img, dtype=np.uint8)
        
        img_norm = (img - img_min) / (img_max - img_min) * 255
        return img_norm.astype(np.uint8)
    
    @staticmethod
    def hacer_zoom(img, x=50, y=50, w=100, h=100):
        if img is None:
            return None, None
        
        if len(img.shape) == 3:
            img = img[:, :, 0]
        elif len(img.shape) == 1:
            return None, None
        
        if len(img.shape) != 2:
            return None, None
        
        h_img, w_img = img.shape
        
        if h_img == 0 or w_img == 0:
            return None, None
        
        x = max(0, min(x, w_img - 1))
        y = max(0, min(y, h_img - 1))
        w = min(w, w_img - x)
        h = min(h, h_img - y)
        
        if w <= 0 or h <= 0:
            return None, None
        
        recorte = img[y:y+h, x:x+w]
        if recorte.size > 0:
            recorte_resize = cv2.resize(recorte, (200, 200))
            return recorte, recorte_resize
        return None, None
    
    @staticmethod
    def segmentar(img, tipo_binarizacion):
        if img is None:
            return None
        
        if len(img.shape) == 3:
            img = img[:, :, 0]
        elif len(img.shape) == 1:
            return None
        
        tipos = {
            "Binario": cv2.THRESH_BINARY,
            "Binario invertido": cv2.THRESH_BINARY_INV,
            "Truncado": cv2.THRESH_TRUNC,
            "Tozero": cv2.THRESH_TOZERO,
            "Tozero invertido": cv2.THRESH_TOZERO_INV
        }
        
        tipo = tipos.get(tipo_binarizacion, cv2.THRESH_BINARY)
        _, binaria = cv2.threshold(img, 127, 255, tipo)
        return binaria
    
    @staticmethod
    def morfologia(img, tipo="Apertura", kernel_size=3):
        if img is None:
            return None
        
        if len(img.shape) == 3:
            img = img[:, :, 0]
        elif len(img.shape) == 1:
            return None
        
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        
        if tipo == "Erosion":
            return cv2.erode(img, kernel, iterations=1)
        elif tipo == "Dilatacion":
            return cv2.dilate(img, kernel, iterations=1)
        elif tipo == "Apertura":
            return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        elif tipo == "Cierre":
            return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        elif tipo == "Gradiente":
            return cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
        
        return img
    
    @staticmethod
    def array_a_qpixmap(img_array):
        if img_array is None:
            return None
        
        if img_array.dtype != np.uint8:
            img_array = ModeloProcesamiento.normalizar(img_array)
        
        if img_array is None:
            return None
        
        if len(img_array.shape) == 3:
            img_array = img_array[:, :, 0]
        elif len(img_array.shape) == 1:
            return None
        
        if img_array.size == 0:
            return None
        
        h, w = img_array.shape
        
        if h <= 0 or w <= 0:
            return None
        
        bytes_per_line = w
        q_img = QImage(img_array.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
        return QPixmap.fromImage(q_img)