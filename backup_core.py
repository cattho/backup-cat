import os
import shutil


def verificar_espacio(origen, destino):
    """Verifica si hay suficiente espacio en disco para el backup."""
    try:
        espacio_necesario = 0
        if os.path.isfile(origen):
            espacio_necesario = os.path.getsize(origen)
        else:
            for raiz, _, archivos in os.walk(origen):
                for archivo in archivos:
                    ruta_completa = os.path.join(raiz, archivo)
                    espacio_necesario += os.path.getsize(ruta_completa)

        # Obtener espacio libre en el disco de destino
        ruta_destino_abs = os.path.abspath(destino)
        # Buscamos el directorio padre existente más cercano por si el destino aún no se crea
        while not os.path.exists(ruta_destino_abs):
            ruta_destino_abs = os.path.dirname(ruta_destino_abs)

        _, _, espacio_libre = shutil.disk_usage(ruta_destino_abs)

        if espacio_necesario > espacio_libre:
            return False, (f"Espacio insuficiente. Se necesitan "
                           f"{espacio_necesario/1024/1024:.2f} MB, "
                           f"pero solo hay {espacio_libre/1024/1024:.2f} MB libres.")
        return True, ""
    except Exception as e:
        return False, f"Error al verificar espacio en disco: {str(e)}"


def contar_archivos(origen):
    """Cuenta el total de archivos a copiar."""
    if os.path.isfile(origen):
        return 1
    total = 0
    for _, _, files in os.walk(origen):
        total += len(files)
    return total


def ejecutar_copia(origen, destino, queue_comunicacion):
    """Realiza la copia de archivos enviando reportes a la cola."""
    try:
        exito, mensaje = verificar_espacio(origen, destino)
        if not exito:
            queue_comunicacion.put({'type': 'error', 'text': mensaje})
            return

        total_files = contar_archivos(origen)
        queue_comunicacion.put({'type': 'count', 'value': total_files})

        if os.path.isfile(origen):
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            shutil.copy2(origen, destino)
            queue_comunicacion.put({'type': 'progress', 'value': 1})
        else:
            contador = 0
            # 1. Copiar archivos y crear directorios implícitamente
            for root, _, files in os.walk(origen):
                for file in files:
                    src_path = os.path.join(root, file)
                    dest_path = os.path.join(
                        destino, os.path.relpath(src_path, origen))

                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                    try:
                        shutil.copy2(src_path, dest_path)
                        contador += 1
                        queue_comunicacion.put(
                            {'type': 'progress', 'value': contador})
                    except Exception as e:
                        queue_comunicacion.put(
                            {'type': 'error', 'text': f"Error al copiar {file}: {str(e)}"})
                        continue

            # 2. Replicar directorios vacíos que se hayan quedado por fuera
            for root, dirs, _ in os.walk(origen):
                for dir in dirs:
                    src_dir = os.path.join(root, dir)
                    dest_dir = os.path.join(
                        destino, os.path.relpath(src_dir, origen))
                    if not os.path.exists(dest_dir):
                        try:
                            os.makedirs(dest_dir, exist_ok=True)
                        except Exception:
                            pass  # Evitamos romper el flujo por un directorio vacío incompleto

        queue_comunicacion.put({'type': 'success'})

    except Exception as e:
        queue_comunicacion.put(
            {'type': 'error', 'text': f"Error inesperado: {str(e)}"})
