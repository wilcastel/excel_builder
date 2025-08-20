import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional, Tuple

class MappingConfigDialog:
    """Diálogo para configurar mapeo de columnas."""
    
    def __init__(self, parent, source_columns: List[str], base_columns: List[str]):
        self.parent = parent
        self.source_columns = source_columns
        self.base_columns = base_columns
        self.result: Optional[Tuple[str, str, str]] = None
        
        # Crear ventana modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Configurar Mapeo")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar ventana
        self._center_window()
        
        # Variables de control
        self.source_column_var = tk.StringVar()
        self.base_key_column_var = tk.StringVar()
        self.base_value_column_var = tk.StringVar()
        
        # Crear widgets
        self._create_widgets()
        
        # Esperar resultado
        self.dialog.wait_window()
    
    def _center_window(self):
        """Centrar ventana en la pantalla."""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"400x300+{x}+{y}")
    
    def _create_widgets(self):
        """Crear widgets del diálogo."""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Configurar Mapeo Multi-Columna", 
                               font=('TkDefaultFont', 12, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Columna fuente
        source_frame = ttk.Frame(main_frame)
        source_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(source_frame, text="Columna Fuente:").pack(anchor='w')
        source_combo = ttk.Combobox(source_frame, textvariable=self.source_column_var,
                                   values=self.source_columns, state='readonly', width=35)
        source_combo.pack(fill='x', pady=(5, 0))
        
        # Columna base (clave)
        base_key_frame = ttk.Frame(main_frame)
        base_key_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(base_key_frame, text="Columna Base (Clave):").pack(anchor='w')
        base_key_combo = ttk.Combobox(base_key_frame, textvariable=self.base_key_column_var,
                                     values=self.base_columns, state='readonly', width=35)
        base_key_combo.pack(fill='x', pady=(5, 0))
        
        # Columna base (valor)
        base_value_frame = ttk.Frame(main_frame)
        base_value_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(base_value_frame, text="Columna Base (Valor):").pack(anchor='w')
        base_value_combo = ttk.Combobox(base_value_frame, textvariable=self.base_value_column_var,
                                       values=self.base_columns, state='readonly', width=35)
        base_value_combo.pack(fill='x', pady=(5, 0))
        
        # Descripción
        desc_frame = ttk.Frame(main_frame)
        desc_frame.pack(fill='x', pady=(0, 20))
        
        desc_text = (
            "El mapeo buscará valores en la columna clave del archivo base "
            "que coincidan con los valores de la columna fuente, y retornará "
            "los valores correspondientes de la columna valor."
        )
        ttk.Label(desc_frame, text=desc_text, wraplength=350, 
                 justify='left', foreground='gray').pack()
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, text="Cancelar", 
                  command=self._cancel).pack(side='right', padx=(10, 0))
        ttk.Button(button_frame, text="Aceptar", 
                  command=self._accept).pack(side='right')
    
    def _validate_input(self) -> bool:
        """Validar entrada del usuario."""
        if not self.source_column_var.get():
            messagebox.showerror("Error", "Debe seleccionar una columna fuente")
            return False
        
        if not self.base_key_column_var.get():
            messagebox.showerror("Error", "Debe seleccionar una columna base (clave)")
            return False
        
        if not self.base_value_column_var.get():
            messagebox.showerror("Error", "Debe seleccionar una columna base (valor)")
            return False
        
        if self.base_key_column_var.get() == self.base_value_column_var.get():
            messagebox.showerror("Error", "La columna clave y valor deben ser diferentes")
            return False
        
        return True
    
    def _accept(self):
        """Aceptar configuración."""
        if not self._validate_input():
            return
        
        self.result = (
            self.source_column_var.get(),
            self.base_key_column_var.get(),
            self.base_value_column_var.get()
        )
        
        self.dialog.destroy()
    
    def _cancel(self):
        """Cancelar diálogo."""
        self.result = None
        self.dialog.destroy()