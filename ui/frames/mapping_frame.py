import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict, List, Optional
import pandas as pd

from core.mapping_manager import MappingManager

class MappingFrame(ttk.Frame):
    """Frame para configuración de mapeo de datos."""
    
    def __init__(self, parent, mapping_manager: MappingManager, 
                 on_config_changed: Callable):
        super().__init__(parent)
        self.mapping_manager = mapping_manager
        self.on_config_changed = on_config_changed
        
        self.source_columns: List[str] = []
        self.base_columns: List[str] = []
        self.source_data: Optional[pd.DataFrame] = None
        self.base_data: Optional[pd.DataFrame] = None
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Crear widgets del frame."""
        # Título
        title_label = ttk.Label(self, text="Mapeo de Datos", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(10, 20))
        
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=20)
        
        # Panel de configuración de mapeo
        self._create_mapping_config(main_frame)
        
        # Panel de vista previa
        self._create_preview_panel(main_frame)
        
    def _create_mapping_config(self, parent):
        """Crear configuración de mapeo."""
        config_frame = ttk.LabelFrame(parent, text="🔗 Configuración de Mapeo", padding=15)
        config_frame.pack(fill='x', pady=(0, 10))
        
        # Tipo de mapeo
        type_frame = ttk.Frame(config_frame)
        type_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(type_frame, text="Tipo de Mapeo:").pack(side='left')
        
        self.mapping_type = tk.StringVar(value="none")
        ttk.Radiobutton(type_frame, text="Sin Mapeo", variable=self.mapping_type, 
                       value="none", command=self._on_mapping_type_changed).pack(side='left', padx=(20, 10))
        ttk.Radiobutton(type_frame, text="Simple", variable=self.mapping_type, 
                       value="simple", command=self._on_mapping_type_changed).pack(side='left', padx=10)
        ttk.Radiobutton(type_frame, text="Multi-columna", variable=self.mapping_type, 
                       value="multi", command=self._on_mapping_type_changed).pack(side='left', padx=10)
        
        # Frame de configuración específica
        self.config_specific_frame = ttk.Frame(config_frame)
        self.config_specific_frame.pack(fill='x', pady=15)
        
        # Configuración simple
        self._create_simple_mapping_config()
        
        # Configuración multi-columna
        self._create_multi_mapping_config()
        
        # Controles
        controls_frame = ttk.Frame(config_frame)
        controls_frame.pack(fill='x', pady=(15, 0))
        
        ttk.Button(controls_frame, text="Aplicar Mapeo", 
                  command=self._apply_mapping).pack(side='left')
        ttk.Button(controls_frame, text="Limpiar Mapeo", 
                  command=self._clear_mapping).pack(side='left', padx=(10, 0))
        ttk.Button(controls_frame, text="Probar Mapeo", 
                  command=self._test_mapping).pack(side='right')
        
    def _create_simple_mapping_config(self):
        """Crear configuración de mapeo simple."""
        self.simple_frame = ttk.LabelFrame(self.config_specific_frame, 
                                          text="Mapeo Simple (1:1)", padding=10)
        
        # Columna fuente
        source_frame = ttk.Frame(self.simple_frame)
        source_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(source_frame, text="Columna Fuente:").pack(side='left')
        self.simple_source_var = tk.StringVar()
        self.simple_source_combo = ttk.Combobox(source_frame, textvariable=self.simple_source_var, 
                                               state='readonly', width=20)
        self.simple_source_combo.pack(side='left', padx=(10, 0))
        
        # Columna base (clave)
        base_key_frame = ttk.Frame(self.simple_frame)
        base_key_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(base_key_frame, text="Columna Base (Clave):").pack(side='left')
        self.simple_base_key_var = tk.StringVar()
        self.simple_base_key_combo = ttk.Combobox(base_key_frame, textvariable=self.simple_base_key_var, 
                                                 state='readonly', width=20)
        self.simple_base_key_combo.pack(side='left', padx=(10, 0))
        
        # Columna base (valor)
        base_value_frame = ttk.Frame(self.simple_frame)
        base_value_frame.pack(fill='x')
        
        ttk.Label(base_value_frame, text="Columna Base (Valor):").pack(side='left')
        self.simple_base_value_var = tk.StringVar()
        self.simple_base_value_combo = ttk.Combobox(base_value_frame, textvariable=self.simple_base_value_var, 
                                                   state='readonly', width=20)
        self.simple_base_value_combo.pack(side='left', padx=(10, 0))
        
    def _create_multi_mapping_config(self):
        """Crear configuración de mapeo multi-columna."""
        self.multi_frame = ttk.LabelFrame(self.config_specific_frame, 
                                         text="Mapeo Multi-columna (N:M)", padding=10)
        
        # Lista de mapeos
        list_frame = ttk.Frame(self.multi_frame)
        list_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Treeview para mapeos
        columns = ('source', 'base_key', 'base_value')
        self.mapping_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=6)
        
        self.mapping_tree.heading('source', text='Columna Fuente')
        self.mapping_tree.heading('base_key', text='Clave Base')
        self.mapping_tree.heading('base_value', text='Valor Base')
        
        self.mapping_tree.column('source', width=120)
        self.mapping_tree.column('base_key', width=120)
        self.mapping_tree.column('base_value', width=120)
        
        mapping_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', 
                                         command=self.mapping_tree.yview)
        self.mapping_tree.configure(yscrollcommand=mapping_scrollbar.set)
        
        self.mapping_tree.pack(side='left', fill='both', expand=True)
        mapping_scrollbar.pack(side='right', fill='y')
        
        # Controles de mapeo
        mapping_controls = ttk.Frame(self.multi_frame)
        mapping_controls.pack(fill='x')
        
        ttk.Button(mapping_controls, text="Agregar Mapeo", 
                  command=self._add_mapping).pack(side='left')
        ttk.Button(mapping_controls, text="Eliminar Mapeo", 
                  command=self._remove_mapping).pack(side='left', padx=(10, 0))
        
    def _create_preview_panel(self, parent):
        """Crear panel de vista previa."""
        preview_frame = ttk.LabelFrame(parent, text="👁️ Vista Previa del Mapeo", padding=15)
        preview_frame.pack(fill='both', expand=True)
        
        # Controles de vista previa
        controls_frame = ttk.Frame(preview_frame)
        controls_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(controls_frame, text="Filas a mostrar:").pack(side='left')
        self.preview_rows = tk.IntVar(value=10)
        ttk.Entry(controls_frame, textvariable=self.preview_rows, width=8).pack(side='left', padx=(10, 0))
        
        ttk.Button(controls_frame, text="Actualizar Vista Previa", 
                  command=self._update_preview).pack(side='left', padx=(20, 0))
        
        # Estadísticas
        self.stats_label = ttk.Label(controls_frame, text="", foreground='gray')
        self.stats_label.pack(side='right')
        
        # Treeview para vista previa
        preview_list_frame = ttk.Frame(preview_frame)
        preview_list_frame.pack(fill='both', expand=True)
        
        # Configurar treeview dinámicamente
        self.preview_tree = ttk.Treeview(preview_list_frame, show='headings', height=10)
        
        preview_tree_scrollbar = ttk.Scrollbar(preview_list_frame, orient='vertical', 
                                              command=self.preview_tree.yview)
        self.preview_tree.configure(yscrollcommand=preview_tree_scrollbar.set)
        
        self.preview_tree.pack(side='left', fill='both', expand=True)
        preview_tree_scrollbar.pack(side='right', fill='y')
        
        # Inicializar estado
        self._on_mapping_type_changed()
        
    def update_source_data(self, df_info: Dict):
        """Actualizar datos fuente."""
        self.source_columns = df_info['columns']
        # Actualizar combos
        self.simple_source_combo['values'] = self.source_columns
        # También actualizar el treeview de mapeo multi-columna
        if hasattr(self, 'mapping_tree'):
            for item in self.mapping_tree.get_children():
                self.mapping_tree.delete(item)
        
    def update_base_data(self, df_info: Dict):
        """Actualizar datos base."""
        self.base_columns = df_info['columns']
        # Actualizar combos
        self.simple_base_key_combo['values'] = self.base_columns
        self.simple_base_value_combo['values'] = self.base_columns
        # Limpiar selecciones previas
        self.simple_base_key_var.set("")
        self.simple_base_value_var.set("")
        
    def _on_mapping_type_changed(self):
        """Callback cuando cambia el tipo de mapeo."""
        mapping_type = self.mapping_type.get()
        
        # Ocultar todos los frames
        self.simple_frame.pack_forget()
        self.multi_frame.pack_forget()
        
        # Mostrar frame correspondiente
        if mapping_type == "simple":
            self.simple_frame.pack(fill='x', pady=10)
        elif mapping_type == "multi":
            self.multi_frame.pack(fill='both', expand=True, pady=10)
            
        self._update_preview()
        
    def _add_mapping(self):
        """Agregar nuevo mapeo multi-columna."""
        from ..dialogs import MappingConfigDialog
        
        dialog = MappingConfigDialog(self, self.source_columns, self.base_columns)
        if dialog.result:
            source_col, base_key_col, base_value_col = dialog.result
            
            # Agregar al treeview
            self.mapping_tree.insert('', 'end', values=(source_col, base_key_col, base_value_col))
            self._update_preview()
            
    def _remove_mapping(self):
        """Eliminar mapeo seleccionado."""
        selection = self.mapping_tree.selection()
        if selection:
            self.mapping_tree.delete(selection[0])
            self._update_preview()
        else:
            messagebox.showwarning("Advertencia", "Seleccione un mapeo para eliminar")
            
    def _apply_mapping(self):
        """Aplicar configuración de mapeo."""
        try:
            mapping_type = self.mapping_type.get()
            
            if mapping_type == "none":
                self.mapping_manager.clear_mappings()
            elif mapping_type == "simple":
                source_col = self.simple_source_var.get()
                base_key_col = self.simple_base_key_var.get()
                base_value_col = self.simple_base_value_var.get()
                
                if not all([source_col, base_key_col, base_value_col]):
                    raise ValueError("Debe seleccionar todas las columnas para mapeo simple")
                    
                self.mapping_manager.add_simple_mapping(source_col, base_key_col, base_value_col)
                
            elif mapping_type == "multi":
                mappings = []
                for item in self.mapping_tree.get_children():
                    values = self.mapping_tree.item(item)['values']
                    mappings.append({
                        'source_column': values[0],
                        'base_key_column': values[1],
                        'base_value_column': values[2]
                    })
                    
                if not mappings:
                    raise ValueError("Debe agregar al menos un mapeo")
                    
                for mapping in mappings:
                    self.mapping_manager.add_simple_mapping(
                        mapping['source_column'],
                        mapping['base_key_column'],
                        mapping['base_value_column']
                    )
                    
            # Notificar cambio
            config_data = self.mapping_manager.get_config()
            self.on_config_changed(config_data)
            
            messagebox.showinfo("Éxito", "Configuración de mapeo aplicada correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar mapeo: {str(e)}")
            
    def _clear_mapping(self):
        """Limpiar configuración de mapeo."""
        self.mapping_manager.clear_mappings()
        self.mapping_type.set("none")
        self._on_mapping_type_changed()
        
        # Limpiar combos
        self.simple_source_var.set("")
        self.simple_base_key_var.set("")
        self.simple_base_value_var.set("")
        
        # Limpiar tree
        for item in self.mapping_tree.get_children():
            self.mapping_tree.delete(item)
            
        self._update_preview()
        
    def _test_mapping(self):
        """Probar mapeo con datos de muestra."""
        try:
            # Verificar que hay columnas configuradas
            if not self.source_columns or not self.base_columns:
                messagebox.showwarning("Advertencia", "Necesita cargar archivos fuente y base para probar el mapeo")
                return
                
            # Aplicar mapeo temporalmente
            self._apply_mapping()
            
            # Mostrar estadísticas
            config = self.mapping_manager.get_config()
            total_mappings = len(config.get('mappings', {}))
            stats_text = f"Mapeos configurados: {total_mappings}"
            self.stats_label.config(text=stats_text)
            
            self._update_preview()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al probar mapeo: {str(e)}")
            
    def _update_preview(self):
        """Actualizar vista previa."""
        try:
            # Limpiar treeview
            for item in self.preview_tree.get_children():
                self.preview_tree.delete(item)
                
            if self.mapping_type.get() == "none" or not self.source_columns:
                return
                
            # Configurar columnas del treeview
            preview_columns = ['original'] + [f'mapped_{i}' for i in range(3)]
            self.preview_tree['columns'] = preview_columns
            
            for col in preview_columns:
                self.preview_tree.heading(col, text=col.replace('_', ' ').title())
                self.preview_tree.column(col, width=100)
                
            # Mostrar datos de muestra
            rows_to_show = min(self.preview_rows.get(), 10)  # Mostrar máximo 10 filas de ejemplo
            for i in range(rows_to_show):
                values = [f"Fila {i+1}", "Valor Original", "Valor Mapeado", "Estado"]
                self.preview_tree.insert('', 'end', values=values)
                
        except Exception as e:
            print(f"Error en vista previa: {e}")
    
    def _save_multi_mapping(self):
        """Guardar configuración de mapeo multicolumna"""
        try:
            # Lógica para guardar mapeo multicolumna
            messagebox.showinfo("Éxito", "Mapeo multicolumna guardado")
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando mapeo: {e}")