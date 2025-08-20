import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Dict, Any, Optional
import os
from datetime import datetime

from config.constants import SUPPORTED_EXPORT_FORMATS

class ExportDialog:
    """Diálogo para configurar opciones de exportación."""
    
    def __init__(self, parent, default_filename: str = ""):
        self.parent = parent
        self.default_filename = default_filename
        self.result: Optional[Dict[str, Any]] = None
        
        # Crear ventana modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Configurar Exportación")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar ventana
        self._center_window()
        
        # Variables de control
        self._create_variables()
        
        # Crear widgets
        self._create_widgets()
        
        # Configurar valores por defecto
        self._set_defaults()
        
        # Esperar resultado
        self.dialog.wait_window()
    
    def _center_window(self):
        """Centrar ventana en la pantalla."""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"500x400+{x}+{y}")
    
    def _create_variables(self):
        """Crear variables de control."""
        self.output_file_var = tk.StringVar()
        self.format_var = tk.StringVar(value="xlsx")
        self.include_headers_var = tk.BooleanVar(value=True)
        self.auto_adjust_columns_var = tk.BooleanVar(value=True)
        self.apply_formatting_var = tk.BooleanVar(value=True)
        self.create_backup_var = tk.BooleanVar(value=False)
        self.sheet_name_var = tk.StringVar(value="Datos")
        self.max_rows_per_sheet_var = tk.StringVar(value="1000000")
    
    def _create_widgets(self):
        """Crear widgets del diálogo."""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Configuración de Exportación", 
                               font=('TkDefaultFont', 12, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Archivo de salida
        file_frame = ttk.LabelFrame(main_frame, text="Archivo de Salida", padding=10)
        file_frame.pack(fill='x', pady=(0, 15))
        
        file_path_frame = ttk.Frame(file_frame)
        file_path_frame.pack(fill='x')
        
        ttk.Entry(file_path_frame, textvariable=self.output_file_var, width=50).pack(side='left', fill='x', expand=True)
        ttk.Button(file_path_frame, text="Examinar...", 
                  command=self._browse_output_file).pack(side='right', padx=(10, 0))
        
        # Formato
        format_frame = ttk.Frame(file_frame)
        format_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Label(format_frame, text="Formato:").pack(side='left')
        format_combo = ttk.Combobox(format_frame, textvariable=self.format_var,
                                   values=list(SUPPORTED_EXPORT_FORMATS.keys()), 
                                   state='readonly', width=15)
        format_combo.pack(side='left', padx=(10, 0))
        
        # Opciones de exportación
        options_frame = ttk.LabelFrame(main_frame, text="Opciones de Exportación", padding=10)
        options_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Checkbutton(options_frame, text="Incluir encabezados",
                       variable=self.include_headers_var).pack(anchor='w', pady=2)
        
        ttk.Checkbutton(options_frame, text="Ajustar ancho de columnas automáticamente",
                       variable=self.auto_adjust_columns_var).pack(anchor='w', pady=2)
        
        ttk.Checkbutton(options_frame, text="Aplicar formato a los datos",
                       variable=self.apply_formatting_var).pack(anchor='w', pady=2)
        
        ttk.Checkbutton(options_frame, text="Crear copia de seguridad",
                       variable=self.create_backup_var).pack(anchor='w', pady=2)
        
        # Configuración de hoja
        sheet_frame = ttk.LabelFrame(main_frame, text="Configuración de Hoja", padding=10)
        sheet_frame.pack(fill='x', pady=(0, 20))
        
        name_frame = ttk.Frame(sheet_frame)
        name_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(name_frame, text="Nombre de hoja:").pack(side='left')
        ttk.Entry(name_frame, textvariable=self.sheet_name_var, width=20).pack(side='left', padx=(10, 0))
        
        rows_frame = ttk.Frame(sheet_frame)
        rows_frame.pack(fill='x')
        
        ttk.Label(rows_frame, text="Máximo filas por hoja:").pack(side='left')
        ttk.Entry(rows_frame, textvariable=self.max_rows_per_sheet_var, width=15).pack(side='left', padx=(10, 0))
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, text="Cancelar", 
                  command=self._cancel).pack(side='right', padx=(10, 0))
        ttk.Button(button_frame, text="Exportar", 
                  command=self._accept).pack(side='right')
    
    def _set_defaults(self):
        """Configurar valores por defecto."""
        if self.default_filename:
            # Generar nombre de archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = os.path.splitext(self.default_filename)[0]
            default_path = f"{base_name}_exportado_{timestamp}.xlsx"
            self.output_file_var.set(default_path)
    
    def _browse_output_file(self):
        """Examinar archivo de salida."""
        file_types = [(desc, f"*.{ext}") for ext, desc in SUPPORTED_EXPORT_FORMATS.items()]
        file_types.append(("Todos los archivos", "*.*"))
        
        filename = filedialog.asksaveasfilename(
            title="Guardar archivo como",
            filetypes=file_types,
            defaultextension=".xlsx",
            initialfile=os.path.basename(self.output_file_var.get())
        )
        
        if filename:
            self.output_file_var.set(filename)
            
            # Actualizar formato basado en extensión
            ext = os.path.splitext(filename)[1].lower().lstrip('.')
            if ext in SUPPORTED_EXPORT_FORMATS:
                self.format_var.set(ext)
    
    def _validate_input(self) -> bool:
        """Validar entrada del usuario."""
        if not self.output_file_var.get().strip():
            messagebox.showerror("Error", "Debe especificar un archivo de salida")
            return False
        
        if not self.sheet_name_var.get().strip():
            messagebox.showerror("Error", "Debe especificar un nombre de hoja")
            return False
        
        # Validar máximo de filas
        try:
            max_rows = int(self.max_rows_per_sheet_var.get())
            if max_rows <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "El máximo de filas debe ser un número entero positivo")
            return False
        
        # Verificar si el directorio de salida existe
        output_dir = os.path.dirname(self.output_file_var.get())
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el directorio: {str(e)}")
                return False
        
        return True
    
    def _accept(self):
        """Aceptar configuración."""
        if not self._validate_input():
            return
        
        self.result = {
            'output_file': self.output_file_var.get().strip(),
            'format': self.format_var.get(),
            'include_headers': self.include_headers_var.get(),
            'auto_adjust_columns': self.auto_adjust_columns_var.get(),
            'apply_formatting': self.apply_formatting_var.get(),
            'create_backup': self.create_backup_var.get(),
            'sheet_name': self.sheet_name_var.get().strip(),
            'max_rows_per_sheet': int(self.max_rows_per_sheet_var.get())
        }
        
        self.dialog.destroy()
    
    def _cancel(self):
        """Cancelar diálogo."""
        self.result = None
        self.dialog.destroy()