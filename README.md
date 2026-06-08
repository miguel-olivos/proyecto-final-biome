Integrantes 
Miguel Angel Olivos Gomez
Jose Pablo Pulgarin Martinez
Sara Estrada Quintero (la mona)
Ana Kateryn Aristizabal Giraldo

# Manual de Usuario - BioMed
Sistema de Análisis Biomédico
¿Qué es BioMed?
Leer archivos dicom, csv, mat y tener un sistema para analizar estos adecuadamente.
No es perfecto, pero hace lo que tiene que hacer (más o menos).

Cómo abrir el programa
Abres la terminal donde tienes el proyecto

Escribes python main.py

Presionas Enter

Si todo sale bien, te sale una ventana con un menú. Si se ve chueco o los botones están desordenados, no te preocupes, es normal. En unos computadores se ve bonito y en otros parece que se hubiera desarmado. Depende de la pantalla, la resolución, la fase de la luna, quién sabe.

El Menú Principal
Tiene tres botones grandes:

Imágenes médicas - Para ver rayos X, TAC, etc.

Señales - Para ver gráficas de señales biomédicas

Datos clínicos - Para ver tablas de pacientes

Abajo hay un botón para cerrar sesión.

Problema conocido: Si le das a "Volver al menú" dentro de cualquier módulo, se cierra todo. No es que vuelva, es que se va. Hay que volver a ejecutar el programa. Lo sabemos, no está corregido.

Módulo de Imágenes Médicas
Cómo usarlo
Le das a "Cargar DICOM"

Buscas un archivo .dcm (de esos de rayos X o TAC)

Lo abres

Qué puedes hacer
Ver cortes: Hay tres sliders:

Corte axial (el que debería funcionar pero a veces no)

Corte sagital (sí funciona)

Corte coronal (sí funciona)

El axial está medio tieso, no siempre se mueve como debería. Los otros dos sí van bien.

Zoom: Seleccionas un área y le das al botón. Te muestra la parte ampliada.

Segmentación: Le das a "Segmentar" y la imagen se vuelve blanco y negro según el umbral que elijas.

Morfología: Puedes aplicar cosas como apertura, cierre, erosión, dilatación. Cambias el tamaño del kernel y le das a "Aplicar".

Guardar: Puedes convertir el DICOM a NIFTI (que en realidad es un .npy) o guardar los datos en CSV.

Problemas conocidos
El slider axial se queda quieto a veces, no quiere moverse

El botón "Volver al menú" cierra todo el programa

En algunos DICOM los cortes sagital y coronal se ven raros

Módulo de Señales
Cómo usarlo
Le das a "Cargar archivo MAT"

Buscas un .mat con una matriz 3D

Lo abres

Qué puedes hacer
Ver canales: Seleccionas un rango de canales (inicio a fin) y te muestra las gráficas.

Agregar ruido: Tomas un canal, le agregas ruido gaussiano con un sigma que tú eliges. Te muestra el canal original y el con ruido.

Calcular estadísticas: Escoges un eje (0, 1 o 2) y te calcula el promedio y la desviación estándar.

Problemas conocidos
Las gráficas se sobreponen una encima de otra si le das varias veces

Con muchos datos la gráfica se ve fea, muy apretada

El botón "Volver al menú" tampoco funciona (se cierra todo)

Módulo de Datos Clínicos
Cómo usarlo
Le das a "Cargar archivo"

Buscas un CSV o Excel

Lo abres

Qué puedes hacer
Ver estadísticas: Se carga una tabla con la media, desviación, mínimo y máximo de cada columna numérica.

Comparar columnas: Seleccionas mínimo 4 columnas y te genera gráficos de línea para compararlas.

Ver correlación: Escoges una columna para X y otra para Y (diferentes), te hace un gráfico de dispersión y te dice la correlación.

Problemas conocidos
El botón "Volver al menú" también cierra todo (es un problema general)





# Observaciones#

En teoria deberia de funcionarnos el login pero ocurrieron cositas 
y las bases de datos no nos funcionaron y pablo que era nuestra unica esperanza se le tosto el computador
pero bueno, el menu


Se ejecuta er main.py 
le abre un menu que enserio si se veo no se porque es, porque en unos computadores se ve re lindo y en otros queda chueco

tiene 3 opciones:
Imagenes mediccas 

se elige un archivo dicom de los que uno tenga
se puede cambiar la vista en todos los cortes en teoria, pero en el axial... pues bueno tieso
tiene la opcion de hacer zomm segun los cortes que se selecciono, tambien esta la parte de "binarizarlo"
ademas permite hacer el cambio de formato de la imagen dicom a NIFTI y csv

PROBLEMA, VOLVER AL MENU CIERRA TODO ;-;

senales
Se selecciona el .mat sin muchas complicaciones, pero la verdad el problema ocurre en la visualizacion como que se sobrepongan varias graficas una sobre otra
se toman muchos datos y queda algo "fea" la grafica
no nos funciono el volver al menu ;-;

Datos clinicos
Muestra los csv en datos donde se da la opcion para ccomparar con respecto a otras, la verdad esta parte si nos quedo mucho mejor
 pero no vuelve al menu ;-;

