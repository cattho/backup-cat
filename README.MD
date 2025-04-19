Versión: 1.0 (Inicial)

Descripción:

"Mi Aplicación de Backup" es una herramienta gráfica simple desarrollada en Python utilizando la biblioteca Tkinter para facilitar la creación de copias de seguridad de carpetas en sistemas Windows. Utiliza el comando xcopy de Windows para realizar la copia de archivos y directorios.

Requisitos del Sistema:

Sistema operativo Windows (ya que utiliza el comando xcopy).
Python 3.x instalado.
Instrucciones de Uso:

Ejecutar la aplicación:

Guarda el código Python en un archivo con extensión .py (por ejemplo, backup_app.py).
Haz doble clic en el archivo para ejecutar la aplicación (si Python está correctamente asociado con la extensión .py) o ábrela desde la línea de comandos utilizando python backup_app.py.
Seleccionar la carpeta de origen:

En la ventana de la aplicación, localiza la sección "Carpeta de Origen:".
Haz clic en el botón "Seleccionar Origen".
Se abrirá un diálogo para que puedas navegar por tu sistema de archivos y seleccionar la carpeta que deseas respaldar.
Una vez que selecciones una carpeta y hagas clic en "Aceptar" (o equivalente), la ruta de la carpeta aparecerá en el campo de texto junto al botón.
Seleccionar la carpeta de destino:

En la ventana de la aplicación, localiza la sección "Carpeta de Destino:".
Haz clic en el botón "Seleccionar Destino".
Se abrirá un diálogo para que puedas navegar por tu sistema de archivos y seleccionar la carpeta donde deseas guardar la copia de seguridad.
Una vez que selecciones una carpeta y hagas clic en "Aceptar" (o equivalente), la ruta de la carpeta aparecerá en el campo de texto junto al botón.
Iniciar el proceso de backup:

Después de haber seleccionado tanto la carpeta de origen como la de destino, haz clic en el botón "Iniciar Backup".
La aplicación ejecutará el comando xcopy en segundo plano para copiar los archivos y directorios desde la origen al destino.
Se mostrará un mensaje en la consola (donde ejecutaste el script) indicando el progreso o los errores del comando xcopy.
La etiqueta de estado en la parte inferior de la ventana de la aplicación se actualizará para indicar si el backup fue "Exitoso" (en color verde) o si hubo un "Error en el Backup" (en color rojo). Si no se seleccionaron las rutas, mostrará "Por favor, selecciona origen y destino" (en color naranja).
Opciones de xcopy Utilizadas (en esta versión):

El comando xcopy se ejecuta con las siguientes opciones:

/E: Copia directorios y subdirectorios, incluyendo los que estén vacíos.
/H: Copia archivos ocultos y de sistema.
/C: Continúa la operación de copia aunque ocurran errores.
/I: Si el destino no existe y se están copiando más de un archivo o directorio, asume que el destino es un directorio.
Nota: Esta es una versión inicial y las opciones de xcopy están predefinidas en el código. En futuras versiones, se podría añadir la posibilidad de que el usuario configure estas opciones a través de la interfaz gráfica.

Posibles Mejoras Futuras:

Añadir opciones para que el usuario configure las opciones de xcopy (por ejemplo, copiar solo archivos modificados, eliminar archivos en el destino que no estén en el origen, etc.).
Mostrar una barra de progreso durante el backup.
Implementar registro de logs para guardar un historial de los backups.
Permitir guardar configuraciones de backup para facilitar tareas repetitivas.
Añadir validaciones para asegurar que las rutas ingresadas sean válidas.
Desarrollador: Juan Sebastian Giraldo Varon

Fecha: 18/04/2025
