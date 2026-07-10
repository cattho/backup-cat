import tkinter as tk
from tkinter import filedialog, ttk, messagebox, font as tkfont
import threading
import queue
import os

# Importaciones locales
import config
import backup_core


class CatthoBackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("El cattho Backup - Copia de Seguridad")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.com_queue = queue.Queue()

        self.configurar_estilos()
        self.crear_interfaz()

    def configurar_estilos(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configurar fuentes
        self.title_font = tkfont.Font(
            family=config.FONT_FAMILIA, size=14, weight="bold")
        self.label_font = tkfont.Font(family=config.FONT_FAMILIA, size=10)
        self.button_font = tkfont.Font(family=config.FONT_FAMILIA, size=10)

        # Estilos de componentes
        self.style.configure('TFrame', background=config.COLOR_FONDO)
        self.style.configure('TLabel', background=config.COLOR_FONDO,
                             foreground=config.COLOR_TEXTO, font=self.label_font)
        self.style.configure('TButton', font=self.button_font, padding=6,
                             background=config.COLOR_SECUNDARIO, foreground='white')
        self.style.map('TButton', background=[
                       ('active', '#2980b9')], foreground=[('active', 'white')])
        self.style.configure('TEntry', fieldbackground='white',
                             foreground=config.COLOR_TEXTO, padding=5)
        self.style.configure('TProgressbar', thickness=20,
                             troughcolor=config.COLOR_FONDO, background=config.COLOR_SECUNDARIO)

    def crear_interfaz(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        ttk.Label(main_frame, text="Backup de Archivos", font=self.title_font,
                  foreground=config.COLOR_PRIMARIO).pack(pady=(0, 20))

        # Origen
        frame_origen = ttk.Frame(main_frame)
        frame_origen.pack(fill=tk.X, pady=10)
        ttk.Label(frame_origen, text="Carpeta de Origen:").pack(
            anchor=tk.W, pady=(0, 5))
        self.entry_origen = ttk.Entry(frame_origen)
        self.entry_origen.pack(side=tk.LEFT, fill=tk.X,
                               expand=True, padx=(0, 10))
        ttk.Button(frame_origen, text="Examinar...",
                   command=self.seleccionar_origen).pack(side=tk.RIGHT)

        # Destino
        frame_destino = ttk.Frame(main_frame)
        frame_destino.pack(fill=tk.X, pady=10)
        ttk.Label(frame_destino, text="Carpeta de Destino:").pack(
            anchor=tk.W, pady=(0, 5))
        self.entry_destino = ttk.Entry(frame_destino)
        self.entry_destino.pack(side=tk.LEFT, fill=tk.X,
                                expand=True, padx=(0, 10))
        ttk.Button(frame_destino, text="Examinar...",
                   command=self.seleccionar_destino).pack(side=tk.RIGHT)

        # Progreso
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=20)
        ttk.Label(progress_frame, text="Progreso:").pack(
            anchor=tk.W, pady=(0, 5))
        self.progress_bar = ttk.Progressbar(
            progress_frame, orient='horizontal', mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))

        # Botón Iniciar
        self.btn_backup = ttk.Button(
            main_frame, text="Iniciar Backup", command=self.iniciar_backup)
        self.btn_backup.pack(ipadx=20, ipady=8, pady=10)

        # Estado
        self.estado_label = ttk.Label(
            main_frame, text="Listo para comenzar", font=self.button_font)
        self.estado_label.pack(pady=10)

    def seleccionar_origen(self):
        ruta = filedialog.askdirectory()
        if ruta:
            self.entry_origen.delete(0, tk.END)
            self.entry_origen.insert(0, ruta)

    def seleccionar_destino(self):
        ruta = filedialog.askdirectory()
        if ruta:
            self.entry_destino.delete(0, tk.END)
            self.entry_destino.insert(0, ruta)

    def check_queue(self):
        while not self.com_queue.empty():
            try:
                msg = self.com_queue.get_nowait()
                if msg['type'] == 'progress':
                    self.progress_bar['value'] = msg['value']
                elif msg['type'] == 'count':
                    self.progress_bar['maximum'] = msg['value']
                elif msg['type'] == 'success':
                    self.estado_label.config(
                        text="¡Backup completado con éxito!", foreground=config.COLOR_EXITO)
                    self.btn_backup.config(state='normal')
                    self.progress_bar['value'] = self.progress_bar['maximum']
                elif msg['type'] == 'error':
                    self.estado_label.config(
                        text=msg['text'], foreground=config.COLOR_ERROR)
                    self.btn_backup.config(state='normal')
                    messagebox.showerror("Error", msg['text'])
            except queue.Empty:
                pass
        self.root.after(100, self.check_queue)

    def iniciar_backup(self):
        origen = self.entry_origen.get()
        destino = self.entry_destino.get()

        if not origen or not destino:
            self.estado_label.config(
                text="Por favor, selecciona las carpetas", foreground=config.COLOR_ADVERTENCIA)
            return

        if not os.path.exists(origen):
            self.estado_label.config(
                text="La ruta de origen no existe", foreground=config.COLOR_ERROR)
            return

        self.btn_backup.config(state='disabled')
        self.estado_label.config(
            text="Copiando archivos...", foreground=config.COLOR_TEXTO)
        self.progress_bar['value'] = 0

        # Lanzar hilo secundario usando el core modularizado
        threading.Thread(
            target=backup_core.ejecutar_copia,
            args=(origen, destino, self.com_queue),
            daemon=True
        ).start()

        self.check_queue()


if __name__ == "__main__":
    root = tk.Tk()
    app = CatthoBackupApp(root)
    root.mainloop()
