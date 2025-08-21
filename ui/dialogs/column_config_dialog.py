import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional

from models.column_config import ColumnConfig, DataType
from config.constants import DATA_TYPE_COLORS

class ColumnConfigDialog:
    """Diálogo para configurar una columna del archivo destino."""
    
    def __init__(self, parent, title: str, source_columns: List[str], 
                 existing_config: Optional[ColumnConfig] = None, file_manager=None):
        self.parent = parent
        self.source_columns = source_columns
        self.existing_config = existing_config
        self.file_manager = file_manager  # Agregar esta línea
        self.result: Optional[ColumnConfig] = None
        
        # Crear ventana modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x550")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar ventana
        self._center_window()
        
        # Variables de control
        self._create_variables()
        
        # Crear widgets
        self._create_widgets()
        
        # Cargar datos existentes si los hay
        if existing_config:
            self._load_existing_config()
        
        # Esperar resultado
        self.dialog.wait_window()
    
    def _center_window(self):
        """Centrar ventana en la pantalla."""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (550 // 2)
        self.dialog.geometry(f"500x550+{x}+{y}")
    
    def _create_variables(self):
        """Crear variables de control."""
        self.name_var = tk.StringVar()
        self.display_name_var = tk.StringVar()
        self.data_type_var = tk.StringVar(value=DataType.TEXT.value)
        self.source_column_var = tk.StringVar()
        self.is_generated_var = tk.BooleanVar()
        self.format_string_var = tk.StringVar()
        self.width_var = tk.StringVar()
        self.required_var = tk.BooleanVar()
        self.position_var = tk.StringVar(value="0")
        self.description_var = tk.StringVar()
        
        # Variables para generación numérica
        self.is_numeric_generator_var = tk.BooleanVar()
        self.numeric_start_var = tk.StringVar(value="1")
        
        # Variables para mapeo (CORREGIDAS)
        self.is_mapping_enabled_var = tk.BooleanVar()
        self.mapping_source_var = tk.StringVar()  # CORREGIDO: era mapping_source_column_var
        self.mapping_key_column_var = tk.StringVar()
        self.mapping_value_column_var = tk.StringVar()
        
        # Variables para columnas adicionales de mapeo
        self.mapping_additional_keys_vars = {}
        self.mapping_additional_keys_base_vars = {}
    
    def _create_widgets(self):
        """Crear widgets del diálogo."""
        # Frame principal
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Notebook para organizar configuraciones
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        # Tab 1: Información básica
        basic_frame = ttk.Frame(notebook)
        notebook.add(basic_frame, text="Información Básica")
        self._create_basic_tab(basic_frame)
        
        # Tab 2: Formato y Validación
        format_frame = ttk.Frame(notebook)
        notebook.add(format_frame, text="Formato y Validación")
        self._create_format_tab(format_frame)
        
        # Tab 3: Generador Numérico
        numeric_frame = ttk.Frame(notebook)
        notebook.add(numeric_frame, text="Generador Numérico")
        self._create_numeric_tab(numeric_frame)
        
        # Tab 4: Mapeo Dinámico
        mapping_frame = ttk.Frame(notebook)
        notebook.add(mapping_frame, text="Mapeo Dinámico")
        self._create_mapping_tab(mapping_frame)
        
        # Botones (siempre visibles)
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(button_frame, text="Cancelar", 
                  command=self._cancel).pack(side='right', padx=(5, 0))
        ttk.Button(button_frame, text="Aceptar", 
                  command=self._accept).pack(side='right')
    
    def _create_basic_tab(self, parent):
        """Crear tab de información básica."""
        # Nombre interno
        ttk.Label(parent, text="Nombre interno:").grid(row=0, column=0, sticky='w', pady=5)
        ttk.Entry(parent, textvariable=self.name_var, width=40).grid(row=0, column=1, sticky='ew', pady=5)
        
        # Nombre para mostrar
        ttk.Label(parent, text="Nombre para mostrar:").grid(row=1, column=0, sticky='w', pady=5)
        ttk.Entry(parent, textvariable=self.display_name_var, width=40).grid(row=1, column=1, sticky='ew', pady=5)
        
        # Tipo de datos
        ttk.Label(parent, text="Tipo de datos:").grid(row=2, column=0, sticky='w', pady=5)
        data_type_combo = ttk.Combobox(parent, textvariable=self.data_type_var, 
                                      values=[dt.value for dt in DataType], 
                                      state='readonly', width=37)
        data_type_combo.grid(row=2, column=1, sticky='ew', pady=5)
        
        # Columna fuente
        ttk.Label(parent, text="Columna fuente:").grid(row=3, column=0, sticky='w', pady=5)
        source_combo = ttk.Combobox(parent, textvariable=self.source_column_var,
                                   values=self.source_columns, state='readonly', width=37)
        source_combo.grid(row=3, column=1, sticky='ew', pady=5)
        
        # Columna generada
        ttk.Checkbutton(parent, text="Columna generada",
                       variable=self.is_generated_var).grid(row=4, column=0, columnspan=2, sticky='w', pady=5)
        
        # Posición
        ttk.Label(parent, text="Posición:").grid(row=5, column=0, sticky='w', pady=5)
        ttk.Entry(parent, textvariable=self.position_var, width=40).grid(row=5, column=1, sticky='ew', pady=5)
        
        # Descripción
        ttk.Label(parent, text="Descripción:").grid(row=6, column=0, sticky='w', pady=5)
        desc_text = tk.Text(parent, height=3, width=40)
        desc_text.grid(row=6, column=1, sticky='ew', pady=5)
        desc_text.bind('<KeyRelease>', lambda e: self.description_var.set(desc_text.get('1.0', 'end-1c')))
        
        # BOTÓN ACEPTAR EN INFORMACIÓN BÁSICA
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=7, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="Agregar Columna", 
                  command=self._accept, 
                  style='Accent.TButton').pack()
        
        parent.columnconfigure(1, weight=1)
    
    def _create_format_tab(self, parent):
        """Crear tab de formato y validación."""
        # Formato personalizado
        format_frame = ttk.LabelFrame(parent, text="📝 Formato Personalizado", padding=10)
        format_frame.pack(fill='x', pady=(0, 10))
        
        # Formato con ejemplos inline
        format_row = ttk.Frame(format_frame)
        format_row.pack(fill='x', pady=2)
        ttk.Label(format_row, text="Formato:").pack(side='left')
        format_entry = ttk.Entry(format_row, textvariable=self.format_string_var, width=20)
        format_entry.pack(side='left', padx=(10, 5))
        ttk.Label(format_row, text="Ej: dd/mm/yyyy, #,##0.00, 0.00%", 
                 foreground="gray", font=('TkDefaultFont', 8)).pack(side='left')
        
        # Botón de ayuda
        help_btn = ttk.Button(format_frame, text="❓ Ayuda", 
                             command=self._show_format_help)
        help_btn.pack(anchor='w', pady=(5, 0))
        
        # Ejemplos comunes
        examples_frame = ttk.LabelFrame(parent, text="📋 Ejemplos Comunes", padding=10)
        examples_frame.pack(fill='x', pady=(0, 10))
        
        examples = [
            ("Fecha: dd/mm/yyyy", "25/12/2024"),
            ("Número: #,##0.00", "1,234.56"),
            ("Porcentaje: 0.00%", "25.50%"),
            ("Moneda: $#,##0.00", "$1,234.56")
        ]
        
        for i, (format_ex, result_ex) in enumerate(examples):
            ttk.Label(examples_frame, text=f"{format_ex} → {result_ex}", 
                     font=('TkDefaultFont', 9)).pack(anchor='w', pady=1)
        
        # Opciones adicionales
        options_frame = ttk.LabelFrame(parent, text="⚙️ Opciones Adicionales", padding=10)
        options_frame.pack(fill='x')
        
        # Ancho y requerido en una fila
        options_row = ttk.Frame(options_frame)
        options_row.pack(fill='x', pady=5)
        ttk.Label(options_row, text="Ancho:").pack(side='left')
        ttk.Entry(options_row, textvariable=self.width_var, width=8).pack(side='left', padx=(5, 15))
        ttk.Checkbutton(options_row, text="Campo requerido", 
                       variable=self.required_var).pack(side='left')
    
    def _show_format_help(self):
        """Mostrar ayuda de formatos"""
        help_text = """
🎯 FORMATOS DISPONIBLES:

📅 FECHAS:
• dd/mm/yyyy → 25/12/2024
• mm/dd/yy → 12/25/24
• yyyy-mm-dd → 2024-12-25

🔢 NÚMEROS:
• #,##0.00 → 1,234.56 (con separadores)
• 0.00 → 1234.56 (sin separadores)
• 0.00% → 25.50% (porcentaje)

💰 MONEDA:
• $#,##0.00 → $1,234.56
• €#,##0.00 → €1,234.56

📝 TEXTO:
• @ → Texto simple
• "Código: "@ → Código: ABC123
        """
        messagebox.showinfo("Ayuda de Formatos", help_text)
    
    def _create_numeric_tab(self, parent):
        """Crear tab de generador numérico."""
        # Activar/desactivar opciones
        ttk.Checkbutton(parent, text="Activar generador numérico",
                       variable=self.is_numeric_generator_var,
                       command=self._toggle_numeric_options).pack(anchor='w')
        
        # Opciones del generador (se habilitan/deshabilitan)
        self.numeric_options_frame = ttk.Frame(parent)
        self.numeric_options_frame.pack(fill='x', pady=(10, 0))
        
        # Número inicial
        start_row = ttk.Frame(self.numeric_options_frame)
        start_row.pack(fill='x', pady=2)
        ttk.Label(start_row, text="Número inicial:").pack(side='left')
        ttk.Entry(start_row, textvariable=self.numeric_start_var, width=10).pack(side='left', padx=(10, 0))
        
        # Columnas de agrupación
        ttk.Label(self.numeric_options_frame, 
                 text="Columnas para agrupar (el número cambia cuando estos valores cambian):").pack(anchor='w', pady=(10, 5))
        
        # Frame con scroll para columnas de agrupación
        group_frame = ttk.Frame(self.numeric_options_frame)
        group_frame.pack(fill='x')
        
        # Crear checkboxes para cada columna del archivo fuente
        self.group_columns_vars = {}
        for i, col in enumerate(self.source_columns):
            var = tk.BooleanVar()
            self.group_columns_vars[col] = var
            ttk.Checkbutton(group_frame, text=col, variable=var).grid(
                row=i//3, column=i%3, sticky='w', padx=5, pady=2)
        
        # Inicializar estados
        self._toggle_numeric_options()
    
    def _toggle_numeric_options(self):
        """Habilitar/deshabilitar opciones del generador numérico"""
        state = 'normal' if self.is_numeric_generator_var.get() else 'disabled'
        for widget in self.numeric_options_frame.winfo_children():
            self._set_widget_state(widget, state)
    
    def _create_mapping_tab(self, parent):
        """Crear tab de mapeo dinámico."""
        # Activar/desactivar opciones
        ttk.Checkbutton(parent, text="Activar mapeo dinámico",
                       variable=self.is_mapping_enabled_var,
                       command=self._toggle_mapping_options).pack(anchor='w')
        
        # Explicación clara
        info_label = ttk.Label(parent, 
                              text="💡 Busca valores en el archivo base usando una columna como referencia",
                              foreground="blue", font=('TkDefaultFont', 8))
        info_label.pack(anchor='w', pady=(5, 10))
        
        # Opciones de mapeo
        self.mapping_options_frame = ttk.Frame(parent)
        self.mapping_options_frame.pack(fill='x')
        
        # Columna de referencia (del archivo fuente)
        ref_row = ttk.Frame(self.mapping_options_frame)
        ref_row.pack(fill='x', pady=2)
        ttk.Label(ref_row, text="Columna de referencia (archivo fuente):").pack(anchor='w')
        self.source_ref_combo = ttk.Combobox(ref_row, 
                                            textvariable=self.mapping_source_var,
                                            values=self.source_columns, 
                                            state='readonly', width=47)
        self.source_ref_combo.pack(fill='x', pady=2)
        
        # Columna clave (del archivo base)
        key_row = ttk.Frame(self.mapping_options_frame)
        key_row.pack(fill='x', pady=2)
        ttk.Label(key_row, text="Columna clave (archivo base para buscar):").pack(anchor='w')
        self.key_combo = ttk.Combobox(key_row, 
                                     textvariable=self.mapping_key_column_var,
                                     values=self._get_base_columns(), 
                                     state='readonly', width=47)
        self.key_combo.pack(fill='x', pady=2)
        
        # Columna valor (del archivo base)
        value_row = ttk.Frame(self.mapping_options_frame)
        value_row.pack(fill='x', pady=2)
        ttk.Label(value_row, text="Columna valor (archivo base para extraer):").pack(anchor='w')
        self.value_combo = ttk.Combobox(value_row, 
                                       textvariable=self.mapping_value_column_var,
                                       values=self._get_base_columns(), 
                                       state='readonly', width=47)
        self.value_combo.pack(fill='x', pady=2)
        
        # Ejemplo práctico
        example_frame = ttk.Frame(self.mapping_options_frame)
        example_frame.pack(fill='x', pady=(10, 0))
        ttk.Label(example_frame, text="📝 Ejemplo:", font=('TkDefaultFont', 8, 'bold')).pack(anchor='w')
        ttk.Label(example_frame, 
                 text="Archivo fuente tiene 'codigo_empleado' → buscar en archivo base → obtener 'nombre_empleado'",
                 font=('TkDefaultFont', 8), foreground="gray").pack(anchor='w')
        
        # SECCIÓN: COLUMNAS ADICIONALES DE REFERENCIA (OPCIONAL)
        additional_frame = ttk.Frame(self.mapping_options_frame)
        additional_frame.pack(fill='x', pady=(15, 0))
        
        # Título y explicación
        ttk.Label(additional_frame, text="🔗 Columnas adicionales de referencia (opcional):", 
                 font=('TkDefaultFont', 9, 'bold')).pack(anchor='w')
        ttk.Label(additional_frame, 
                 text="💡 Usar para evitar ambigüedades cuando una sola columna no es suficiente",
                 font=('TkDefaultFont', 8), foreground="blue").pack(anchor='w', pady=(0, 10))
        
        # Frame con scroll para columnas adicionales
        additional_scroll_frame = ttk.Frame(additional_frame)
        additional_scroll_frame.pack(fill='x')
        
        # Crear checkboxes para cada columna del archivo fuente
        self.mapping_additional_keys_vars = {}
        for i, col in enumerate(self.source_columns):
            var = tk.BooleanVar()
            self.mapping_additional_keys_vars[col] = var
            ttk.Checkbutton(additional_scroll_frame, text=col, variable=var).grid(
                row=i//3, column=i%3, sticky='w', padx=5, pady=2)
        
        # Inicializar estados
        self._toggle_mapping_options()
    
    def _toggle_mapping_options(self):
        """Habilitar/deshabilitar opciones de mapeo"""
        state = 'normal' if self.is_mapping_enabled_var.get() else 'disabled'
        
        # Actualizar valores de los comboboxes cuando se habilita el mapeo
        if self.is_mapping_enabled_var.get():
            base_columns = self._get_base_columns()
            self.key_combo.configure(values=base_columns)
            self.value_combo.configure(values=base_columns)
        
        # Establecer estado de los widgets
        for widget in self.mapping_options_frame.winfo_children():
            self._set_widget_state(widget, state)
    
    def _set_widget_state(self, widget, state):
        """Establecer estado de widget recursivamente"""
        try:
            widget.configure(state=state)
        except:
            pass
        for child in widget.winfo_children():
            self._set_widget_state(child, state)
    
    def _get_base_columns(self):
        """Obtener columnas del archivo base desde FileManager"""
        if self.file_manager:
            return self.file_manager.get_base_columns()
        return []
    
    def _load_existing_config(self):
        """Cargar configuración existente."""
        config = self.existing_config
        
        self.name_var.set(config.name)
        self.display_name_var.set(config.display_name)
        self.data_type_var.set(config.data_type.value)
        
        if config.source_column:
            self.source_column_var.set(config.source_column)
        
        self.is_generated_var.set(config.is_generated)
        
        if config.format_string:
            self.format_string_var.set(config.format_string)
        
        if config.width:
            self.width_var.set(str(config.width))
        
        self.required_var.set(config.required)
        self.position_var.set(str(config.position))
        
        if config.description:
            self.description_var.set(config.description)
        
        # Configuraciones avanzadas - Generador numérico
        self.is_numeric_generator_var.set(config.is_numeric_generator)
        self.numeric_start_var.set(str(config.numeric_start))
        
        # Cargar columnas de agrupación del generador numérico
        if config.numeric_grouping_columns:
            for col_name in config.numeric_grouping_columns:
                if col_name in self.group_columns_vars:
                    self.group_columns_vars[col_name].set(True)
        
        # Configuraciones avanzadas - Mapeo dinámico
        has_mapping = bool(config.mapping_source or config.mapping_key_column or config.mapping_value_column)
        self.is_mapping_enabled_var.set(has_mapping)  # CORREGIDO: Activar checkbox de mapeo
        
        if config.mapping_source:
            self.mapping_source_var.set(config.mapping_source)
        if config.mapping_key_column:
            self.mapping_key_column_var.set(config.mapping_key_column)
        if config.mapping_value_column:
            self.mapping_value_column_var.set(config.mapping_value_column)
        
        # Cargar columnas adicionales de mapeo
        if config.mapping_additional_keys:
            for col_name in config.mapping_additional_keys:
                if col_name in self.mapping_additional_keys_vars:
                    self.mapping_additional_keys_vars[col_name].set(True)
        
        # Actualizar estados de los widgets después de cargar
        self._toggle_numeric_options()
        self._toggle_mapping_options()
    
    def _validate_input(self) -> bool:
        """Validar entrada del usuario."""
        if not self.name_var.get().strip():
            messagebox.showerror("Error", "El nombre interno es requerido")
            return False
        
        if not self.display_name_var.get().strip():
            messagebox.showerror("Error", "El nombre para mostrar es requerido")
            return False
        
        # Validar posición
        try:
            int(self.position_var.get())
        except ValueError:
            messagebox.showerror("Error", "La posición debe ser un número entero")
            return False
        
        # Validar ancho si se especifica
        if self.width_var.get().strip():
            try:
                int(self.width_var.get())
            except ValueError:
                messagebox.showerror("Error", "El ancho debe ser un número entero")
                return False
        
        # Validar número inicial para generador numérico
        if self.is_numeric_generator_var.get():
            try:
                int(self.numeric_start_var.get())
            except ValueError:
                messagebox.showerror("Error", "El número inicial debe ser un entero")
                return False
        
        return True
    
    def _accept(self):
        """Aceptar configuración."""
        if not self._validate_input():
            return
        
        try:
            # Obtener columnas de agrupación seleccionadas
            grouping_columns = []
            if hasattr(self, 'group_columns_vars'):
                grouping_columns = [col for col, var in self.group_columns_vars.items() if var.get()]
                print(f"DEBUG: Columnas de agrupación seleccionadas: {grouping_columns}")
            
            # Obtener columnas adicionales de mapeo seleccionadas
            additional_keys = []
            if hasattr(self, 'mapping_additional_keys_vars'):
                additional_keys = [col for col, var in self.mapping_additional_keys_vars.items() if var.get()]
                print(f"DEBUG: Columnas adicionales de referencia seleccionadas: {additional_keys}")
            
            # Crear configuración
            self.result = ColumnConfig(
                name=self.name_var.get().strip(),
                display_name=self.display_name_var.get().strip(),
                data_type=DataType(self.data_type_var.get()),
                source_column=self.source_column_var.get().strip() or None,
                is_generated=self.is_generated_var.get(),
                format_string=self.format_string_var.get().strip() or None,
                width=int(self.width_var.get()) if self.width_var.get().strip() else None,
                required=self.required_var.get(),
                position=int(self.position_var.get()),
                description=self.description_var.get().strip() or None,
                is_numeric_generator=self.is_numeric_generator_var.get(),
                numeric_start=int(self.numeric_start_var.get()),
                numeric_grouping_columns=grouping_columns,  # CORREGIDO: Incluir columnas de agrupación
                mapping_source=self.mapping_source_var.get().strip() or None if self.is_mapping_enabled_var.get() else None,
                mapping_key_column=self.mapping_key_column_var.get().strip() or None if self.is_mapping_enabled_var.get() else None,
                mapping_value_column=self.mapping_value_column_var.get().strip() or None if self.is_mapping_enabled_var.get() else None,
                mapping_additional_keys=additional_keys if self.is_mapping_enabled_var.get() else []
            )
            
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creando configuración: {str(e)}")
    
    def _cancel(self):
        """Cancelar diálogo."""
        self.result = None
        self.dialog.destroy()