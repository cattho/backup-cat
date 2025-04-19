import tkinter as tk
from tkinter import filedialog, ttk
import shutil
import os
import threading
import queue

# Cola para comunicación entre hilos
com_queue = queue.Queue()

def check_queue():
    """Actualiza la interfaz desde el hilo principal"""
    while not com_queue.empty():
        try:
            msg = com_queue.get_nowait()
            
            if msg['type'] == 'progress':
                progress_bar['value'] = msg['value']
            elif msg['type'] == 'max':
                progress_bar['maximum'] = msg['value']
            elif msg['type'] == 'success':
                estado_label.config(text="Backup Exitoso", fg="green")
                btn_backup.config(state='normal')
                progress_bar['value'] = progress_bar['maximum']
            elif msg['type'] == 'error':
                estado_label.config(text=msg['text'], fg="red")
                btn_backup.config(state='normal')
            elif msg['type'] == 'count':
                total_files = msg['value']
                progress_bar['maximum'] = total_files
            
        except queue.Empty:
            pass
    
    root.after(100, check_queue)

def copiar_archivos(origen, destino):
    """Función que realiza la copia en segundo plano"""
    try:
        # Contar archivos totales
        total_files = 0
        if os.path.isfile(origen):
            total_files = 1
        else:
            for root, _, files in os.walk(origen):
                total_files += len(files)
        
        com_queue.put({'type': 'count', 'value': total_files})
        
        # Copiar archivos
        if os.path.isfile(origen):
            # Crear directorio de destino si no existe
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            shutil.copy2(origen, destino)
            com_queue.put({'type': 'progress', 'value': 1})
        else:
            contador = 0
            for root, dirs, files in os.walk(origen):
                for file in files:
                    src_path = os.path.join(root, file)
                    dest_path = os.path.join(destino, os.path.relpath(src_path, origen))
                    
                    # Crear directorio si no existe
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    
                    shutil.copy2(src_path, dest_path)
                    contador += 1
                    com_queue.put({'type': 'progress', 'value': contador})
            
            # Copiar directorios vacíos
            for root, dirs, _ in os.walk(origen):
                for dir in dirs:
                    src_dir = os.path.join(root, dir)
                    dest_dir = os.path.join(destino, os.path.relpath(src_dir, origen))
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir, exist_ok=True)
        
        com_queue.put({'type': 'success'})
    
    except Exception as e:
        com_queue.put({'type': 'error', 'text': f"Error: {str(e)}"})

def seleccionar_origen():
    ruta = filedialog.askdirectory()
    if ruta:
        entry_origen.delete(0, tk.END)
        entry_origen.insert(0, ruta)

def seleccionar_destino():
    ruta = filedialog.askdirectory()
    if ruta:
        entry_destino.delete(0, tk.END)
        entry_destino.insert(0, ruta)

def iniciar_backup():
    origen = entry_origen.get()
    destino = entry_destino.get()
    
    if origen and destino:
        btn_backup.config(state='disabled')
        estado_label.config(text="Copiando...", fg="black")
        progress_bar['value'] = 0
        
        # Iniciar hilo de copia
        threading.Thread(
            target=copiar_archivos,
            args=(origen, destino),
            daemon=True
        ).start()
        
        # Iniciar chequeo de cola
        check_queue()
    else:
        estado_label.config(text="Selecciona origen y destino", fg="orange")

# Configuración de la ventana principal
root = tk.Tk()
root.title("El cattho Backup - Con Progreso")

# Widgets para origen
tk.Label(root, text="Carpeta de Origen:").pack(pady=5)
entry_origen = tk.Entry(root, width=50)
entry_origen.pack(pady=5)
tk.Button(root, text="Seleccionar Origen", command=seleccionar_origen).pack(pady=5)

# Widgets para destino
tk.Label(root, text="Carpeta de Destino:").pack(pady=5)
entry_destino = tk.Entry(root, width=50)
entry_destino.pack(pady=5)
tk.Button(root, text="Seleccionar Destino", command=seleccionar_destino).pack(pady=5)

# Barra de progreso
progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate')
progress_bar.pack(pady=10, fill='x', padx=20)

# Botón de inicio
btn_backup = tk.Button(root, text="Iniciar Backup", command=iniciar_backup)
btn_backup.pack(pady=10)

# Etiqueta de estado
estado_label = tk.Label(root, text="", fg="black")
estado_label.pack(pady=5)

root.mainloop()