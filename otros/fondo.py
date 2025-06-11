#!/usr/bin/env python3
"""
Convertidor de Fondo de Pantalla para iPhone 13 Pro Max
Convierte cualquier imagen al tamaño perfecto sin deformarla
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from pathlib import Path

class iPhoneWallpaperConverter:
    def __init__(self):
        # Diccionario con resoluciones comunes de celulares
        self.PHONE_RESOLUTIONS = {
            "iPhone 15 Pro Max / 14 Pro Max / 13 Pro Max / 12 Pro Max": (1290, 2796),
            "iPhone 15 Pro / 14 Pro / 13 Pro / 12 Pro": (1179, 2556),
            "iPhone 15 / 14 / 13 / 12": (1170, 2532),
            "iPhone 11 Pro Max / XS Max": (1242, 2688),
            "iPhone 11 Pro / XS / X": (1125, 2436),
            "iPhone 11 / XR": (828, 1792),
            "iPhone 8 Plus / 7 Plus / 6s Plus / 6 Plus": (1080, 1920),
            "iPhone SE (3rd gen) / 8 / 7 / 6s / 6": (750, 1334),
            "Samsung Galaxy S24 Ultra / S23 Ultra / S22 Ultra": (1440, 3120),
            "Samsung Galaxy S24+ / S23+ / S22+": (1440, 3120),
            "Samsung Galaxy S24 / S23 / S22": (1080, 2340),
            "Samsung Galaxy A54 / A53 / A52": (1080, 2400),
            "Samsung Galaxy Note 20 Ultra": (1440, 3088),
            "Google Pixel 8 Pro / 7 Pro / 6 Pro": (1344, 2992),
            "Google Pixel 8 / 7 / 6": (1080, 2400),
            "Google Pixel 8a / 7a / 6a": (1080, 2400),
            "OnePlus 12 / 11 / 10 Pro": (1440, 3216),
            "OnePlus 11 / 10": (1440, 3216),
            "Xiaomi 14 Ultra / 13 Ultra": (1440, 3200),
            "Xiaomi 14 / 13": (1200, 2670),
            "Huawei P60 Pro / P50 Pro": (1440, 2700),
            "Sony Xperia 1 V / 1 IV": (1644, 3840),
            "Resolución HD+ (Gama Media)": (720, 1600),
            "Resolución FHD+ (Premium)": (1080, 2400),
            "Resolución QHD+ (Ultra Premium)": (1440, 3200)
        }
        
        # Configuración inicial (iPhone 13 Pro Max por defecto)
        self.current_resolution_name = "iPhone 15 Pro Max / 14 Pro Max / 13 Pro Max / 12 Pro Max"
        self.TARGET_WIDTH, self.TARGET_HEIGHT = self.PHONE_RESOLUTIONS[self.current_resolution_name]
        self.TARGET_SIZE = (self.TARGET_WIDTH, self.TARGET_HEIGHT)
        
        # Variables
        self.original_image = None
        self.processed_image = None
        self.preview_image = None
        
        # Crear interfaz
        self.setup_gui()
        
    def setup_gui(self):
        """Configurar la interfaz gráfica"""
        self.root = tk.Tk()
        self.root.title("📱 Convertidor Universal de Fondos de Pantalla")
        self.root.geometry("900x1000")
        self.root.configure(bg='#1a1a1a')
        
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'), background='#1a1a1a', foreground='white')
        style.configure('Info.TLabel', font=('Arial', 10), background='#1a1a1a', foreground='#cccccc')
        style.configure('Custom.TButton', font=('Arial', 11, 'bold'))
        
        # Título principal
        title_frame = tk.Frame(self.root, bg='#1a1a1a')
        title_frame.pack(pady=20)
        
        title_label = ttk.Label(title_frame, text="📱 Convertidor Universal de Fondos de Pantalla", 
                               style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Compatible con iPhone, Samsung, Google Pixel, OnePlus y más", 
                                  font=('Arial', 10), background='#1a1a1a', foreground='#4ECDC4')
        subtitle_label.pack(pady=5)
        
        # Selector de resolución
        resolution_frame = tk.Frame(self.root, bg='#2d2d2d', relief='ridge', bd=2)
        resolution_frame.pack(pady=15, padx=20, fill='x')
        
        resolution_title = ttk.Label(resolution_frame, text="📐 Seleccionar Dispositivo y Resolución", 
                                    font=('Arial', 12, 'bold'), background='#2d2d2d', foreground='#FF6B6B')
        resolution_title.pack(pady=10)
        
        # Dropdown para seleccionar resolución
        self.resolution_var = tk.StringVar(value=self.current_resolution_name)
        self.resolution_dropdown = ttk.Combobox(resolution_frame, textvariable=self.resolution_var,
                                               values=list(self.PHONE_RESOLUTIONS.keys()),
                                               state='readonly', width=60, font=('Arial', 9))
        self.resolution_dropdown.pack(pady=5)
        self.resolution_dropdown.bind('<<ComboboxSelected>>', self.on_resolution_change)
        
        # Información técnica actualizable
        info_frame = tk.Frame(self.root, bg='#2d2d2d', relief='ridge', bd=2)
        info_frame.pack(pady=10, padx=20, fill='x')
        
        self.info_title = ttk.Label(info_frame, text="📱 Especificaciones del Dispositivo Seleccionado", 
                              font=('Arial', 12, 'bold'), background='#2d2d2d', foreground='#4ECDC4')
        self.info_title.pack(pady=5)
        
        self.specs_label = ttk.Label(info_frame, text="", 
                                    font=('Arial', 9), background='#2d2d2d', foreground='white',
                                    justify='center')
        self.specs_label.pack(pady=5)
        
        # Actualizar información inicial
        self.update_specs_info()
        
        # Botones principales
        button_frame = tk.Frame(self.root, bg='#1a1a1a')
        button_frame.pack(pady=20)
        
        self.select_btn = tk.Button(button_frame, text="📁 Seleccionar Imagen", 
                                   command=self.select_image,
                                   bg='#4ECDC4', fg='white', font=('Arial', 12, 'bold'),
                                   padx=20, pady=10, relief='flat', cursor='hand2')
        self.select_btn.pack(side='left', padx=10)
        
        self.process_btn = tk.Button(button_frame, text="🔄 Procesar Imagen", 
                                    command=self.process_image,
                                    bg='#FF6B6B', fg='white', font=('Arial', 12, 'bold'),
                                    padx=20, pady=10, relief='flat', cursor='hand2',
                                    state='disabled')
        self.process_btn.pack(side='left', padx=10)
        
        self.save_btn = tk.Button(button_frame, text="💾 Guardar Fondo", 
                                 command=self.save_image,
                                 bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'),
                                 padx=20, pady=10, relief='flat', cursor='hand2',
                                 state='disabled')
        self.save_btn.pack(side='left', padx=5)
        
        self.auto_save_btn = tk.Button(button_frame, text="⚡ Guardar Rápido", 
                                      command=self.auto_save_image,
                                      bg='#9C27B0', fg='white', font=('Arial', 12, 'bold'),
                                      padx=20, pady=10, relief='flat', cursor='hand2',
                                      state='disabled')
        self.auto_save_btn.pack(side='left', padx=5)
        
        # Marco para vista previa
        preview_frame = tk.Frame(self.root, bg='#1a1a1a')
        preview_frame.pack(pady=20, expand=True, fill='both')
        
        # Etiqueta de vista previa
        self.preview_label = ttk.Label(preview_frame, text="Vista previa aparecerá aquí", 
                                      style='Info.TLabel')
        self.preview_label.pack(pady=10)
        
        # Canvas para la imagen
        self.canvas = tk.Canvas(preview_frame, width=250, height=540, 
                               bg='#000000', relief='ridge', bd=3)
        self.canvas.pack()
        
        # Información de estado
        self.status_label = ttk.Label(self.root, text="💡 Selecciona una imagen para comenzar", 
                                     style='Info.TLabel')
        self.status_label.pack(pady=10)
        
        # Información adicional
        help_frame = tk.Frame(self.root, bg='#2d2d2d', relief='ridge', bd=1)
        help_frame.pack(pady=10, padx=20, fill='x')
        
        help_text = ("ℹ️ Tu imagen se ajustará automáticamente manteniendo las proporciones originales.\n"
                    "Los espacios vacíos se rellenarán con negro para un acabado elegante.\n"
                    "Selecciona tu dispositivo arriba para obtener la resolución perfecta.")
        help_label = ttk.Label(help_frame, text=help_text, 
                              font=('Arial', 9), background='#2d2d2d', foreground='#cccccc',
                              justify='center')
        help_label.pack(pady=10)
    
    def on_resolution_change(self, event=None):
        """Cambiar resolución cuando se selecciona un dispositivo diferente"""
        selected_device = self.resolution_var.get()
        if selected_device in self.PHONE_RESOLUTIONS:
            self.current_resolution_name = selected_device
            self.TARGET_WIDTH, self.TARGET_HEIGHT = self.PHONE_RESOLUTIONS[selected_device]
            self.TARGET_SIZE = (self.TARGET_WIDTH, self.TARGET_HEIGHT)
            
            # Actualizar información
            self.update_specs_info()
            
            # Si hay una imagen procesada, reprocesarla con la nueva resolución
            if self.original_image and self.processed_image:
                self.process_image()
            
            self.status_label.config(text=f"📱 Dispositivo cambiado: {selected_device.split('/')[0].strip()}")
    
    def update_specs_info(self):
        """Actualizar la información de especificaciones"""
        # Calcular proporción
        aspect_ratio = round(self.TARGET_WIDTH / self.TARGET_HEIGHT, 3)
        simplified_ratio = self.get_simplified_ratio()
        
        # Calcular PPI aproximado (estimado)
        ppi = self.estimate_ppi()
        
        # Obtener información adicional
        device_info = self.get_device_info()
        
        specs_text = (
            f"Resolución: {self.TARGET_WIDTH} x {self.TARGET_HEIGHT} píxeles\n"
            f"Proporción: {simplified_ratio} ({aspect_ratio})\n"
            f"PPI Estimado: ~{ppi}\n"
            f"Dispositivos: {device_info}"
        )
        
        self.specs_label.config(text=specs_text)
    
    def get_simplified_ratio(self):
        """Calcular proporción simplificada"""
        from math import gcd
        common_divisor = gcd(self.TARGET_WIDTH, self.TARGET_HEIGHT)
        simplified_w = self.TARGET_WIDTH // common_divisor
        simplified_h = self.TARGET_HEIGHT // common_divisor
        return f"{simplified_w}:{simplified_h}"
    
    def estimate_ppi(self):
        """Estimar PPI basado en resolución común"""
        # Tabla de PPI conocidos para diferentes resoluciones
        ppi_table = {
            (1290, 2796): 460,  # iPhone 15 Pro Max
            (1179, 2556): 460,  # iPhone 15 Pro
            (1170, 2532): 460,  # iPhone 15
            (1242, 2688): 458,  # iPhone 11 Pro Max
            (1125, 2436): 458,  # iPhone X/XS/11 Pro
            (828, 1792): 326,   # iPhone 11/XR
            (1080, 1920): 401,  # iPhone Plus
            (750, 1334): 326,   # iPhone 8/7/6
            (1440, 3120): 516,  # Samsung S24 Ultra
            (1080, 2340): 422,  # Samsung S24
            (1080, 2400): 411,  # Pixel/Samsung mid-range
            (1344, 2992): 489,  # Pixel Pro
            (720, 1600): 270,   # HD+ budget phones
        }
        
        return ppi_table.get((self.TARGET_WIDTH, self.TARGET_HEIGHT), "N/A")
    
    def get_device_info(self):
        """Obtener información de dispositivos para la resolución actual"""
        device_name = self.current_resolution_name
        
        # Extraer marca principal
        if "iPhone" in device_name:
            return "📱 Apple iPhone Series"
        elif "Samsung" in device_name:
            return "📱 Samsung Galaxy Series"
        elif "Pixel" in device_name:
            return "📱 Google Pixel Series"
        elif "OnePlus" in device_name:
            return "📱 OnePlus Series"
        elif "Xiaomi" in device_name:
            return "📱 Xiaomi Series"
        elif "Huawei" in device_name:
            return "📱 Huawei Series"
        elif "Sony" in device_name:
            return "📱 Sony Xperia Series"
        elif "HD+" in device_name:
            return "📱 Gama Media (Varios fabricantes)"
        elif "FHD+" in device_name:
            return "📱 Gama Alta (Varios fabricantes)"
        elif "QHD+" in device_name:
            return "📱 Gama Ultra Premium (Varios fabricantes)"
        else:
            return "📱 Múltiples dispositivos"
    
    def select_image(self):
        """Seleccionar imagen del archivo"""
        filetypes = [
            ("Imágenes", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
            ("JPEG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("Todos los archivos", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=filetypes
        )
        
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.status_label.config(text=f"✅ Imagen cargada: {os.path.basename(file_path)}")
                self.process_btn.config(state='normal')
                
                # Mostrar información de la imagen original
                width, height = self.original_image.size
                aspect_ratio = round(width / height, 2)
                self.preview_label.config(text=f"Imagen original: {width}x{height} px (ratio: {aspect_ratio})")
                
                # Resetear botones de guardado
                self.save_btn.config(state='disabled')
                self.auto_save_btn.config(state='disabled')
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{str(e)}")
                self.status_label.config(text="❌ Error al cargar la imagen")
    
    def process_image(self):
        """Procesar la imagen para iPhone 13 Pro Max"""
        if not self.original_image:
            return
        
        try:
            # Crear canvas negro del tamaño objetivo
            processed = Image.new('RGB', self.TARGET_SIZE, (0, 0, 0))
            
            # Calcular dimensiones manteniendo proporción
            original_width, original_height = self.original_image.size
            original_aspect = original_width / original_height
            target_aspect = self.TARGET_WIDTH / self.TARGET_HEIGHT
            
            if original_aspect > target_aspect:
                # Imagen más ancha - ajustar por altura
                new_height = self.TARGET_HEIGHT
                new_width = int(new_height * original_aspect)
            else:
                # Imagen más alta - ajustar por ancho
                new_width = self.TARGET_WIDTH
                new_height = int(new_width / original_aspect)
            
            # Redimensionar imagen manteniendo calidad
            resized = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Calcular posición para centrar
            x = (self.TARGET_WIDTH - new_width) // 2
            y = (self.TARGET_HEIGHT - new_height) // 2
            
            # Pegar imagen centrada en canvas negro
            processed.paste(resized, (x, y))
            
            self.processed_image = processed
            
            # Crear vista previa para mostrar
            self.create_preview()
            
            self.status_label.config(text="✅ Imagen procesada correctamente")
            self.save_btn.config(state='normal')
            self.auto_save_btn.config(state='normal')
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar la imagen:\n{str(e)}")
            self.status_label.config(text="❌ Error al procesar la imagen")
    
    def create_preview(self):
        """Crear vista previa en el canvas"""
        if not self.processed_image:
            return
        
        # Crear una versión pequeña para vista previa (manteniendo proporción)
        preview_width = 250
        preview_height = int(preview_width * (self.TARGET_HEIGHT / self.TARGET_WIDTH))
        
        preview = self.processed_image.resize((preview_width, preview_height), Image.Resampling.LANCZOS)
        self.preview_image = ImageTk.PhotoImage(preview)
        
        # Limpiar canvas y mostrar imagen
        self.canvas.delete("all")
        self.canvas.config(width=preview_width, height=preview_height)
        self.canvas.create_image(preview_width//2, preview_height//2, 
                                image=self.preview_image)
        
        self.preview_label.config(text=f"Vista previa: {self.TARGET_WIDTH}x{self.TARGET_HEIGHT} px | {self.current_resolution_name.split('/')[0].strip()}")
    
    def save_image(self):
        """Guardar la imagen procesada"""
        if not self.processed_image:
            return
        
        # Crear directorio de salida si no existe
        output_dir = self.get_output_directory()
        output_dir.mkdir(exist_ok=True)
        
        # Sugerir nombre de archivo con dispositivo
        device_short = self.current_resolution_name.split('/')[0].strip().replace(' ', '-')
        default_name = f"fondo-{device_short}-{self.get_timestamp()}.jpg"
        default_path = output_dir / default_name
        
        # Preguntar al usuario dónde guardar
        file_path = filedialog.asksaveasfilename(
            title="Guardar fondo de pantalla",
            defaultextension=".jpg",
            initialname=default_name,
            initialdir=str(output_dir),
            filetypes=[
                ("JPEG", "*.jpg"),
                ("PNG", "*.png"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Guardar con alta calidad
                if file_path.lower().endswith('.png'):
                    self.processed_image.save(file_path, 'PNG', optimize=True)
                else:
                    self.processed_image.save(file_path, 'JPEG', quality=95, optimize=True)
                
                self.status_label.config(text=f"✅ Guardado: {os.path.basename(file_path)}")
                
                # Mostrar mensaje de éxito con ubicación
                full_path = os.path.abspath(file_path)
                messagebox.showinfo("Éxito", 
                    f"¡Fondo de pantalla guardado exitosamente!\n\n"
                    f"📁 Ubicación: {full_path}\n"
                    f"📄 Archivo: {os.path.basename(file_path)}\n"
                    f"📐 Resolución: {self.TARGET_WIDTH}x{self.TARGET_HEIGHT}\n\n"
                    f"💡 Ahora puedes usar esta imagen como fondo de pantalla en tu iPhone 13 Pro Max.")
                
                # Opción para abrir la carpeta
                if messagebox.askyesno("Abrir carpeta", "¿Quieres abrir la carpeta donde se guardó?"):
                    self.open_file_location(file_path)
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar la imagen:\n{str(e)}")
                self.status_label.config(text="❌ Error al guardar la imagen")
    
    def get_output_directory(self):
        """Obtener directorio de salida predeterminado"""
        # Crear carpeta en el escritorio del usuario
        desktop = Path.home() / "Desktop"
        if desktop.exists():
            return desktop / "Fondos Celulares"
        
        # Si no hay escritorio, usar carpeta de documentos
        docs = Path.home() / "Documents"
        if docs.exists():
            return docs / "Fondos Celulares"
        
        # Como último recurso, usar directorio actual
        return Path.cwd() / "Fondos Celulares"
    
    def open_file_location(self, file_path):
        """Abrir la ubicación del archivo guardado"""
        try:
            import subprocess
            import platform
            
            system = platform.system()
            if system == "Windows":
                subprocess.run(f'explorer /select,"{file_path}"', shell=True)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", "-R", file_path])
            elif system == "Linux":
                subprocess.run(["xdg-open", os.path.dirname(file_path)])
        except Exception as e:
            print(f"No se pudo abrir la ubicación: {e}")
    
    def auto_save_image(self):
        """Guardar automáticamente en la carpeta predeterminada"""
        if not self.processed_image:
            return
        
        try:
            # Crear directorio de salida
            output_dir = self.get_output_directory()
            output_dir.mkdir(exist_ok=True)
            
            # Generar nombre único con dispositivo
            device_short = self.current_resolution_name.split('/')[0].strip().replace(' ', '-')
            filename = f"fondo-{device_short}-{self.get_timestamp()}.jpg"
            file_path = output_dir / filename
            
            # Guardar imagen
            self.processed_image.save(file_path, 'JPEG', quality=95, optimize=True)
            
            self.status_label.config(text=f"✅ Guardado automáticamente: {filename}")
            
            # Mostrar mensaje de éxito
            messagebox.showinfo("Guardado Automático", 
                f"¡Imagen guardada automáticamente!\n\n"
                f"📁 Carpeta: {output_dir}\n"
                f"📄 Archivo: {filename}\n"
                f"📐 Resolución: {self.TARGET_WIDTH}x{self.TARGET_HEIGHT}\n\n"
                f"¿Quieres abrir la carpeta?")
            
            # Abrir carpeta automáticamente
            self.open_file_location(str(file_path))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar automáticamente:\n{str(e)}")
            self.status_label.config(text="❌ Error en guardado automático")
    
    def get_timestamp(self):
        """Generar timestamp para nombre único"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    try:
        app = iPhoneWallpaperConverter()
        app.run()
    except ImportError as e:
        print("Error: Faltan dependencias requeridas.")
        print("Instala las dependencias con:")
        print("pip install pillow")
        print(f"\nDetalle del error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()