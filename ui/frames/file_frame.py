import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Callable, Optional
import pandas as pd

from core.file_manager import FileManager
from config.constants import SUPPORTED_FORMATS

class FileFrame(ttk.Frame):
    """Frame para gestión de archivos Excel."""
    
    def __init__(self, parent, file_manager: FileManager, 
                 on_source_loaded: Callable, on_base_loaded: Callable):
        super().__init__(parent)
        self.file_manager = file_manager
        self.on_source_loaded = on_source_loaded
        self.on_base_loaded = on_base_loaded
        
        self.source_file_var = tk.StringVar()
        self.base_file_var = tk.StringVar()
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Crear widgets del frame."""
        # Título
        title_label = ttk.Label(self, text="Gestión de Archivos Excel", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(10, 20))
        
        # Frame principal con dos columnas
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=20)
        
        # Columna izquierda - Archivo fuente
        self._create_source_section(main_frame)
        
        # Separador
        separator = ttk.Separator(main_frame, orient='vertical')
        separator.pack(side='left', fill='y', padx=20)
        
        # Columna derecha - Archivo base
        self._create_base_section(main_frame)
        
    def _create_source_section(self, parent):
        """Crear sección de archivo fuente."""
        source_frame = ttk.LabelFrame(parent, text="📊 Archivo Fuente (Datos)", padding=15)
        source_frame.pack(side='left', fill='both', expand=True)
        
        # Descripción
        desc_label = ttk.Label(source_frame, 
                              text="Seleccione el archivo Excel que contiene los datos a procesar",
                              foreground='gray')
        desc_label.pack(anchor='w', pady=(0, 10))
        
        # Selección de archivo
        file_frame = ttk.Frame(source_frame)
        file_frame.pack(fill='x', pady=(0, 15))
        
        self.source_entry = ttk.Entry(file_frame, textvariable=self.source_file_var, 
                                     state='readonly', width=40)
        self.source_entry.pack(side='left', fill='x', expand=True)
        
        self.source_btn = ttk.Button(file_frame, text="Examinar...", 
                                    command=self._select_source_file)
        self.source_btn.pack(side='right', padx=(10, 0))
        
        # Información del archivo
        self.source_info_frame = ttk.LabelFrame(source_frame, text="Información del Archivo")
        self.source_info_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        self.source_info_text = tk.Text(self.source_info_frame, height=8, width=40, 
                                       state='disabled', wrap='word')
        scrollbar_source = ttk.Scrollbar(self.source_info_frame, orient='vertical', 
                                        command=self.source_info_text.yview)
        self.source_info_text.configure(yscrollcommand=scrollbar_source.set)
        
        self.source_info_text.pack(side='left', fill='both', expand=True)
        scrollbar_source.pack(side='right', fill='y')
        
    def _create_base_section(self, parent):
        """Crear sección de archivo base."""
        base_frame = ttk.LabelFrame(parent, text="🗂️ Archivo Base (Mapeo)", padding=15)
        base_frame.pack(side='right', fill='both', expand=True)
        
        # Descripción
        desc_label = ttk.Label(base_frame, 
                              text="Archivo Excel para mapeo de valores (opcional)",
                              foreground='gray')
        desc_label.pack(anchor='w', pady=(0, 10))
        
        # Selección de archivo
        file_frame = ttk.Frame(base_frame)
        file_frame.pack(fill='x', pady=(0, 15))
        
        self.base_entry = ttk.Entry(file_frame, textvariable=self.base_file_var, 
                                   state='readonly', width=40)
        self.base_entry.pack(side='left', fill='x', expand=True)
        
        self.base_btn = ttk.Button(file_frame, text="Examinar...", 
                                  command=self._select_base_file)
        self.base_btn.pack(side='right', padx=(10, 0))
        
        # Botón para limpiar
        self.clear_base_btn = ttk.Button(file_frame, text="Limpiar", 
                                        command=self._clear_base_file)
        self.clear_base_btn.pack(side='right', padx=(5, 5))
        
        # Información del archivo
        self.base_info_frame = ttk.LabelFrame(base_frame, text="Información del Archivo")
        self.base_info_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        self.base_info_text = tk.Text(self.base_info_frame, height=8, width=40, 
                                     state='disabled', wrap='word')
        scrollbar_base = ttk.Scrollbar(self.base_info_frame, orient='vertical', 
                                      command=self.base_info_text.yview)
        self.base_info_text.configure(yscrollcommand=scrollbar_base.set)
        
        self.base_info_text.pack(side='left', fill='both', expand=True)
        scrollbar_base.pack(side='right', fill='y')
        
    def _select_source_file(self):
        """Seleccionar archivo fuente."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar Archivo Fuente",
            filetypes=[("Archivos Excel", "*.xlsx *.xls"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            try:
                # Cargar archivo
                df_info = self.file_manager.load_source_file(file_path)
                
                # Actualizar UI
                self.source_file_var.set(file_path)
                self._update_source_info(df_info)
                
                # Notificar callback
                self.on_source_loaded(file_path, df_info)
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar archivo fuente:\n{str(e)}")
                
    def _select_base_file(self):
        """Seleccionar archivo base."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar Archivo Base",
            filetypes=[("Archivos Excel", "*.xlsx *.xls"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            try:
                # Cargar archivo
                df_info = self.file_manager.load_base_file(file_path)
                
                # Actualizar UI
                self.base_file_var.set(file_path)
                self._update_base_info(df_info)
                
                # Notificar callback
                self.on_base_loaded(file_path, df_info)
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar archivo base:\n{str(e)}")
                
    def _clear_base_file(self):
        """Limpiar archivo base."""
        self.base_file_var.set("")
        self.file_manager.clear_base_file()
        self._clear_base_info()
        
    def _update_source_info(self, df_info: dict):
        """Actualizar información del archivo fuente."""
        info_text = f"""📊 INFORMACIÓN DEL ARCHIVO FUENTE

📁 Archivo: {df_info['file_name']}
📏 Tamaño: {df_info['file_size']}
📋 Hojas: {', '.join(df_info['sheets'])}
🗂️ Hoja activa: {df_info['active_sheet']}

📊 DATOS:
• Filas: {df_info['rows']:,}
• Columnas: {df_info['columns_count']}
• Memoria: {df_info['memory_usage']}

📋 COLUMNAS:
"""
        
        for i, col in enumerate(df_info['columns'], 1):
            info_text += f"{i:2d}. {col}\n"
            
        self._set_text_content(self.source_info_text, info_text)
        
    def _update_base_info(self, df_info: dict):
        """Actualizar información del archivo base."""
        info_text = f"""🗂️ INFORMACIÓN DEL ARCHIVO BASE

📁 Archivo: {df_info['file_name']}
📏 Tamaño: {df_info['file_size']}
📋 Hojas: {', '.join(df_info['sheets'])}
🗂️ Hoja activa: {df_info['active_sheet']}

📊 DATOS:
• Filas: {df_info['rows']:,}
• Columnas: {df_info['columns_count']}
• Memoria: {df_info['memory_usage']}

📋 COLUMNAS:
"""
        
        for i, col in enumerate(df_info['columns'], 1):
            info_text += f"{i:2d}. {col}\n"
            
        self._set_text_content(self.base_info_text, info_text)
        
    def _clear_base_info(self):
        """Limpiar información del archivo base."""
        self._set_text_content(self.base_info_text, "No hay archivo base cargado")
        
    def _set_text_content(self, text_widget: tk.Text, content: str):
        """Establecer contenido de un widget Text."""
        text_widget.config(state='normal')
        text_widget.delete(1.0, tk.END)
        text_widget.insert(1.0, content)
        text_widget.config(state='disabled')