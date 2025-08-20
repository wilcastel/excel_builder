import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Callable, Optional

from core.column_manager import ColumnManager
from models.column_config import ColumnConfig, DataType
from config.constants import DATA_TYPE_COLORS

class ColumnFrame(ttk.Frame):
    """Frame para configuración de columnas del archivo destino."""
    
    def __init__(self, parent, column_manager: ColumnManager, 
                 on_config_changed: Callable, file_manager=None):
        super().__init__(parent)
        self.column_manager = column_manager
        self.on_config_changed = on_config_changed
        self.file_manager = file_manager  # Agregar esta línea
        
        self.source_columns: List[str] = []
        self.selected_columns: Dict[str, tk.BooleanVar] = {}
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Crear widgets del frame."""
        # Título
        title_label = ttk.Label(self, text="Configuración de Columnas", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(10, 20))
        
        # Frame principal con dos paneles
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=20)
        
        # Panel izquierdo - Columnas fuente
        self._create_source_panel(main_frame)
        
        # Separador
        separator = ttk.Separator(main_frame, orient='vertical')
        separator.pack(side='left', fill='y', padx=15)
        
        # Panel derecho - Configuración destino
        self._create_destination_panel(main_frame)
        
    def _create_source_panel(self, parent):
        """Crear panel de columnas fuente."""
        source_frame = ttk.LabelFrame(parent, text="📊 Columnas Fuente", padding=15)
        source_frame.pack(side='left', fill='both', expand=True)
        
        # Controles de selección
        controls_frame = ttk.Frame(source_frame)
        controls_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(controls_frame, text="Seleccionar Todo", 
                  command=self._select_all_columns).pack(side='left', padx=(0, 5))
        ttk.Button(controls_frame, text="Deseleccionar Todo", 
                  command=self._deselect_all_columns).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="Agregar Seleccionadas", 
                  command=self._add_selected_columns).pack(side='right')
        
        # Lista de columnas con checkboxes
        list_frame = ttk.Frame(source_frame)
        list_frame.pack(fill='both', expand=True)
        
        # Canvas y scrollbar para lista scrolleable
        self.canvas = tk.Canvas(list_frame, height=300)
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Mensaje inicial
        self.no_source_label = ttk.Label(self.scrollable_frame, 
                                        text="Cargue un archivo fuente para ver las columnas",
                                        foreground='gray')
        self.no_source_label.pack(pady=20)
        
    def _create_destination_panel(self, parent):
        """Crear panel de configuración destino."""
        dest_frame = ttk.LabelFrame(parent, text="🎯 Columnas Destino", padding=15)
        dest_frame.pack(side='right', fill='both', expand=True)
        
        # Controles de columnas destino
        controls_frame = ttk.Frame(dest_frame)
        controls_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(controls_frame, text="Nueva Columna", 
                  command=self._add_new_column).pack(side='left', padx=(0, 5))
        ttk.Button(controls_frame, text="Editar", 
                  command=self._edit_selected_column).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="Eliminar", 
                  command=self._remove_selected_column).pack(side='left', padx=5)
        
        # Controles de orden
        order_frame = ttk.Frame(controls_frame)
        order_frame.pack(side='right')
        
        ttk.Button(order_frame, text="↑", width=3,
                  command=self._move_column_up).pack(side='left', padx=2)
        ttk.Button(order_frame, text="↓", width=3,
                  command=self._move_column_down).pack(side='left', padx=2)
        
        # Treeview para columnas destino
        tree_frame = ttk.Frame(dest_frame)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('name', 'type', 'source', 'format')
        self.dest_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        # Configurar columnas
        self.dest_tree.heading('name', text='Nombre')
        self.dest_tree.heading('type', text='Tipo')
        self.dest_tree.heading('source', text='Fuente')
        self.dest_tree.heading('format', text='Formato')
        
        self.dest_tree.column('name', width=120)
        self.dest_tree.column('type', width=80)
        self.dest_tree.column('source', width=100)
        self.dest_tree.column('format', width=80)
        
        # Scrollbar para treeview
        tree_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', 
                                      command=self.dest_tree.yview)
        self.dest_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.dest_tree.pack(side='left', fill='both', expand=True)
        tree_scrollbar.pack(side='right', fill='y')
        
        # Bind eventos
        self.dest_tree.bind('<Double-1>', lambda e: self._edit_selected_column())
        
    def update_source_columns(self, columns: List[str]):
        """Actualizar lista de columnas fuente."""
        self.source_columns = columns
        self.selected_columns.clear()
        
        # Limpiar frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        if not columns:
            self.no_source_label = ttk.Label(self.scrollable_frame, 
                                            text="No hay columnas disponibles",
                                            foreground='gray')
            self.no_source_label.pack(pady=20)
            return
            
        # Crear checkboxes para cada columna
        for i, column in enumerate(columns):
            var = tk.BooleanVar()
            self.selected_columns[column] = var
            
            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(fill='x', pady=2)
            
            checkbox = ttk.Checkbutton(frame, text=f"{i+1:2d}. {column}", 
                                     variable=var)
            checkbox.pack(anchor='w')
            
    def _select_all_columns(self):
        """Seleccionar todas las columnas."""
        for var in self.selected_columns.values():
            var.set(True)
            
    def _deselect_all_columns(self):
        """Deseleccionar todas las columnas."""
        for var in self.selected_columns.values():
            var.set(False)
            
    def _add_selected_columns(self):
        """Agregar columnas seleccionadas a la configuración"""
        selected = [col for col, var in self.selected_columns.items() if var.get()]
        
        if not selected:
            messagebox.showwarning("Advertencia", "No hay columnas seleccionadas")
            return
            
        for column in selected:
            # Crear configuración básica
            config = ColumnConfig(
                name=column,
                display_name=column,  # Agregar display_name
                data_type=DataType.TEXT,
                source_column=column
            )
            
            try:
                self.column_manager.add_column(config)
            except ValueError as e:
                messagebox.showwarning("Advertencia", str(e))
                
        self._refresh_destination_tree()
        self._notify_config_changed()
        
    def _add_new_column(self):
        """Agregar nueva columna personalizada."""
        from ..dialogs.column_config_dialog import ColumnConfigDialog
        
        dialog = ColumnConfigDialog(
            self, 
            "Nueva Columna", 
            self.source_columns,
            file_manager=self.file_manager  # Agregar esta línea
        )
        
        if dialog.result:
            try:
                # Verificar si se agregó correctamente
                if self.column_manager.add_column(dialog.result):
                    self._refresh_destination_tree()
                    self._notify_config_changed()
                    messagebox.showinfo("Éxito", f"Columna '{dialog.result.name}' agregada correctamente")
                else:
                    # Mostrar errores de validación
                    errors = dialog.result.validate()
                    if errors:
                        error_msg = "Errores en la configuración:\n" + "\n".join(errors)
                        messagebox.showerror("Error de Validación", error_msg)
                    else:
                        messagebox.showerror("Error", "No se pudo agregar la columna. Verifique que el nombre no esté duplicado.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        else:
            # El usuario canceló el diálogo
            print("Diálogo cancelado por el usuario")
    
    def _edit_selected_column(self):
        """Editar columna seleccionada."""
        selection = self.dest_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione una columna para editar")
            return
            
        item = selection[0]
        column_name = self.dest_tree.item(item)['values'][0]
        
        # Obtener la configuración actual
        current_config = self.column_manager.get_column(column_name)
        if not current_config:
            return
            
        from ..dialogs import ColumnConfigDialog
        
        dialog = ColumnConfigDialog(
            self, 
            "Editar Columna", 
            self.source_columns, 
            current_config,
            file_manager=self.file_manager  # Agregar esta línea
        )
        if dialog.result:
            try:
                # Actualizar la columna existente
                self.column_manager.update_column(column_name, **dialog.result.to_dict())
                self._refresh_destination_tree()
                self._notify_config_changed()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                
    def _remove_selected_column(self):
        """Eliminar columna seleccionada."""
        selection = self.dest_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione una columna para eliminar")
            return
            
        item = selection[0]
        column_name = self.dest_tree.item(item)['values'][0]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar la columna '{column_name}'?"):
            self.column_manager.remove_column(column_name)
            self._refresh_destination_tree()
            self._notify_config_changed()
            
    def _move_column_up(self):
        """Mover columna hacia arriba."""
        selection = self.dest_tree.selection()
        if not selection:
            return
            
        item = selection[0]
        column_name = self.dest_tree.item(item)['values'][0]
        
        # Usar move_column con dirección "up"
        if self.column_manager.move_column(column_name, "up"):
            self._refresh_destination_tree()
            self._notify_config_changed()
            
    def _move_column_down(self):
        """Mover columna hacia abajo."""
        selection = self.dest_tree.selection()
        if not selection:
            return
            
        item = selection[0]
        column_name = self.dest_tree.item(item)['values'][0]
        
        # Usar move_column con dirección "down"
        if self.column_manager.move_column(column_name, "down"):
            self._refresh_destination_tree()
            self._notify_config_changed()
            
    def _refresh_destination_tree(self):
        """Actualizar árbol de columnas destino"""
        # Limpiar árbol
        for item in self.dest_tree.get_children():
            self.dest_tree.delete(item)
            
        # Agregar columnas
        for config in self.column_manager.get_all_columns():
            # Asegurar que data_type sea un enum
            data_type_value = config.data_type.value if hasattr(config.data_type, 'value') else str(config.data_type)
            
            values = (
                config.display_name,
                data_type_value,
                config.source_column or 'Generado',
                config.format_string or 'Ninguno'
            )
            
            item = self.dest_tree.insert('', 'end', values=values)
            
            # Aplicar colores según tipo de dato (opcional)
            # if config.data_type in DATA_TYPE_COLORS:
            #     # Aquí podrías aplicar tags de color si los tienes configurados
            #     pass
            if config.data_type in DATA_TYPE_COLORS:
                self.dest_tree.set(item, 'type', config.data_type.value)
                
    def _notify_config_changed(self):
        """Notificar cambio en configuración."""
        config_data = {
            'columns': [config.to_dict() for config in self.column_manager.get_all_columns()],  # Cambiar aquí también
            'count': len(self.column_manager.get_all_columns())  # Y aquí
        }
        self.on_config_changed(config_data)