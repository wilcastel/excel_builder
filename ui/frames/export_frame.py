import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Callable, Dict, Any
import os
from datetime import datetime

from core.export_manager import ExportManager
from config.constants import SUPPORTED_EXPORT_FORMATS

class ExportFrame(ttk.Frame):
    """Frame para configuración y exportación de archivos."""
    
    def __init__(self, parent, export_manager: ExportManager, 
                 on_export_requested: Callable):
        super().__init__(parent)
        self.export_manager = export_manager
        self.on_export_requested = on_export_requested
        
        self.column_config: Dict = {}
        self.numeric_config: Dict = {}
        self.mapping_config: Dict = {}
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Crear widgets del frame."""
        # Título
        title_label = ttk.Label(self, text="Exportación de Archivos", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(10, 15))
        
        # Frame principal con distribución optimizada
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=20)
        
        # PANEL SUPERIOR (50% del espacio) - Configuración y Resumen
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill='x', pady=(0, 10))
        
        # Configuración de exportación (lado izquierdo)
        config_frame = ttk.Frame(top_frame)
        config_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        self._create_export_config(config_frame)
        
        # Resumen de configuración (lado derecho)
        summary_frame = ttk.Frame(top_frame)
        summary_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        self._create_summary_panel(summary_frame)
        
        # PANEL INFERIOR (50% del espacio) - Vista Previa y Exportación
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill='both', expand=True)
        
        # Vista previa (parte superior del panel inferior)
        preview_frame = ttk.Frame(bottom_frame)
        preview_frame.pack(fill='both', expand=True, pady=(0, 10))
        self._create_preview_panel(preview_frame)
        
        # Exportación (parte inferior del panel inferior)
        export_frame = ttk.Frame(bottom_frame)
        export_frame.pack(fill='x')
        self._create_export_panel(export_frame)
        
    def _create_export_config(self, parent):
        """Crear configuración de exportación."""
        config_frame = ttk.LabelFrame(parent, text="⚙️ Configuración de Exportación", padding=10)
        config_frame.pack(fill='both', expand=True)
        
        # Primera fila - Archivo y formato
        first_row = ttk.Frame(config_frame)
        first_row.pack(fill='x', pady=(0, 8))
        
        # Archivo de destino
        file_frame = ttk.Frame(first_row)
        file_frame.pack(side='left', fill='x', expand=True)
        
        ttk.Label(file_frame, text="Archivo de Destino:").pack(anchor='w')
        
        file_select_frame = ttk.Frame(file_frame)
        file_select_frame.pack(fill='x', pady=(3, 0))
        
        self.output_file_var = tk.StringVar()
        self.output_entry = ttk.Entry(file_select_frame, textvariable=self.output_file_var)
        self.output_entry.pack(side='left', fill='x', expand=True)
        
        ttk.Button(file_select_frame, text="Examinar...", 
                  command=self._select_output_file).pack(side='right', padx=(8, 0))
        
        # Formato
        format_frame = ttk.Frame(first_row)
        format_frame.pack(side='right', padx=(15, 0))
        
        ttk.Label(format_frame, text="Formato:").pack(anchor='w')
        
        self.format_var = tk.StringVar(value="xlsx")
        format_combo = ttk.Combobox(format_frame, textvariable=self.format_var, 
                                   values=list(SUPPORTED_EXPORT_FORMATS.keys()), 
                                   state='readonly', width=12)
        format_combo.pack(pady=(3, 0))
        
        # Segunda fila - Opciones y límites
        second_row = ttk.Frame(config_frame)
        second_row.pack(fill='x', pady=8)
        
        # Opciones de exportación
        options_frame = ttk.LabelFrame(second_row, text="Opciones", padding=8)
        options_frame.pack(side='left', fill='both', expand=True)
        
        self.include_headers = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Incluir encabezados", 
                       variable=self.include_headers).pack(anchor='w')
        
        self.auto_adjust_columns = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Ajustar ancho de columnas automáticamente", 
                       variable=self.auto_adjust_columns).pack(anchor='w')
        
        self.apply_formatting = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Aplicar formato profesional", 
                       variable=self.apply_formatting).pack(anchor='w')
        
        self.create_backup = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Crear copia de seguridad", 
                       variable=self.create_backup).pack(anchor='w')
        
        # Límites
        limits_frame = ttk.LabelFrame(second_row, text="Límites", padding=8)
        limits_frame.pack(side='right', fill='y', padx=(8, 0))
        
        ttk.Label(limits_frame, text="Máximo de filas:").pack(anchor='w')
        self.max_rows = tk.IntVar(value=100000)
        ttk.Entry(limits_frame, textvariable=self.max_rows, width=10).pack(anchor='w', pady=(0, 5))
        
        ttk.Label(limits_frame, text="Hoja de destino:").pack(anchor='w')
        self.sheet_name = tk.StringVar(value="Datos")
        ttk.Entry(limits_frame, textvariable=self.sheet_name, width=15).pack(anchor='w')
        
    def _create_summary_panel(self, parent):
        """Crear panel de resumen de configuración."""
        summary_frame = ttk.LabelFrame(parent, text="📋 Resumen de Configuración", padding=10)
        summary_frame.pack(fill='both', expand=True)
        
        # Frame con dos columnas para mejor organización
        summary_content = ttk.Frame(summary_frame)
        summary_content.pack(fill='both', expand=True)
        
        # Columna izquierda
        left_summary = ttk.Frame(summary_content)
        left_summary.pack(side='left', fill='both', expand=True)
        
        # Estado general (más prominente)
        self.validation_summary = ttk.Label(left_summary, text="⚠️ Configuración incompleta", 
                                           foreground='orange', font=('Arial', 10, 'bold'))
        self.validation_summary.pack(anchor='w', pady=(0, 8))
        
        # Columnas configuradas
        self.columns_summary = ttk.Label(left_summary, text="Columnas: No configuradas", 
                                        foreground='gray')
        self.columns_summary.pack(anchor='w')
        
        # Generador numérico (opcional)
        self.numeric_summary = ttk.Label(left_summary, text="Generador numérico: No configurado", 
                                        foreground='gray')
        self.numeric_summary.pack(anchor='w')
        
        # Columna derecha
        right_summary = ttk.Frame(summary_content)
        right_summary.pack(side='right', fill='both', expand=True)
        
        # Mapeo (opcional) 
        self.mapping_summary = ttk.Label(right_summary, text="Mapeo: No configurado", 
                                        foreground='gray')
        self.mapping_summary.pack(anchor='w')
        
        # Validación
        self.validation_status = ttk.Label(right_summary, text="Validación: Pendiente", 
                                          foreground='orange')
        self.validation_status.pack(anchor='w')
        
        # Información de división de archivos
        self.split_info = ttk.Label(right_summary, text="", foreground='blue')
        self.split_info.pack(anchor='w', pady=(5, 0))
        
        # Labels de respaldo para compatibilidad
        self.columns_info = self.columns_summary
        self.numeric_info = self.numeric_summary
        self.mapping_info = self.mapping_summary
        
    def _create_preview_panel(self, parent):
        """Crear panel de vista previa."""
        preview_frame = ttk.LabelFrame(parent, text="👁️ Vista Previa del Resultado", padding=10)
        preview_frame.pack(fill='both', expand=True)
        
        # Controles de vista previa
        controls_frame = ttk.Frame(preview_frame)
        controls_frame.pack(fill='x', pady=(0, 8))
        
        ttk.Button(controls_frame, text="Generar Vista Previa", 
                  command=self._generate_preview).pack(side='left')
        
        ttk.Label(controls_frame, text="Filas a mostrar:").pack(side='left', padx=(15, 5))
        self.preview_rows = tk.IntVar(value=20)
        ttk.Entry(controls_frame, textvariable=self.preview_rows, width=8).pack(side='left')
        
        # Información de vista previa
        self.preview_info = ttk.Label(controls_frame, text="", foreground='gray')
        self.preview_info.pack(side='right')
        
        # Treeview para vista previa
        preview_list_frame = ttk.Frame(preview_frame)
        preview_list_frame.pack(fill='both', expand=True)
        
        self.preview_tree = ttk.Treeview(preview_list_frame, show='headings', height=6)
        
        preview_scrollbar_v = ttk.Scrollbar(preview_list_frame, orient='vertical', 
                                           command=self.preview_tree.yview)
        preview_scrollbar_h = ttk.Scrollbar(preview_list_frame, orient='horizontal', 
                                           command=self.preview_tree.xview)
        
        self.preview_tree.configure(yscrollcommand=preview_scrollbar_v.set,
                                   xscrollcommand=preview_scrollbar_h.set)
        
        self.preview_tree.pack(side='left', fill='both', expand=True)
        preview_scrollbar_v.pack(side='right', fill='y')
        preview_scrollbar_h.pack(side='bottom', fill='x')
        
    def _create_export_panel(self, parent):
        """Crear panel de exportación."""
        export_frame = ttk.LabelFrame(parent, text="📤 Exportación", padding=10)
        export_frame.pack(fill='x')
        
        # Botones de acción
        buttons_frame = ttk.Frame(export_frame)
        buttons_frame.pack(fill='x')
        
        ttk.Button(buttons_frame, text="Validar Configuración", 
                  command=self._validate_config).pack(side='left')
        
        ttk.Button(buttons_frame, text="Exportar Archivo", 
                  command=self._export_file, 
                  style='Accent.TButton').pack(side='left', padx=(8, 0))
        
        ttk.Button(buttons_frame, text="Abrir Carpeta de Destino", 
                  command=self._open_output_folder).pack(side='right')
        
        # Barra de progreso
        progress_frame = ttk.Frame(export_frame)
        progress_frame.pack(fill='x', pady=(8, 0))
        
        self.export_progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.export_progress.pack(fill='x')
        
        self.export_status = ttk.Label(progress_frame, text="Listo para exportar", 
                                      foreground='gray')
        self.export_status.pack(pady=(3, 0))
        
    def update_column_config(self, config_data: Dict):
        """Actualizar configuración de columnas."""
        self.column_config = config_data
        count = config_data.get('count', 0)
        self.columns_summary.config(
            text=f"Columnas: {count} configuradas",
            foreground='green' if count > 0 else 'gray'
        )
        
        # Actualizar información de división de archivos si hay datos fuente disponibles
        self._update_split_info()
    
    def _update_split_info(self):
        """Actualizar información sobre división de archivos."""
        try:
            # Intentar obtener datos fuente y configuración de columnas
            if (hasattr(self, 'get_source_data_callback') and self.get_source_data_callback and 
                self.column_config.get('columns')):
                
                source_data = self.get_source_data_callback()
                if source_data is not None and not source_data.empty:
                    # Convertir configuración de columnas a objetos ColumnConfig
                    from models.column_config import ColumnConfig
                    column_configs = []
                    for col_data in self.column_config.get('columns', []):
                        if isinstance(col_data, dict):
                            col_config = ColumnConfig.from_dict(col_data)
                            column_configs.append(col_config)
                        else:
                            column_configs.append(col_data)
                    
                    # Obtener información de exportación
                    export_info = self.export_manager.get_export_info(source_data, column_configs)
                    
                    if export_info['will_split']:
                        self.split_info.config(
                            text=f"📁 Se dividirá en {export_info['num_files']} archivos (~{export_info['estimated_size_per_file_mb']} MB cada uno)",
                            foreground='blue'
                        )
                    else:
                        self.split_info.config(
                            text=f"📄 Un solo archivo (~{export_info['estimated_size_mb']} MB)",
                            foreground='green'
                        )
                else:
                    self.split_info.config(text="", foreground='gray')
            else:
                self.split_info.config(text="", foreground='gray')
                
        except Exception as e:
            self.split_info.config(text="", foreground='gray')
        
    def update_numeric_config(self, config_data: Dict):
        """Actualizar configuración numérica."""
        self.numeric_config = config_data
        gen_type = config_data.get('type', 'none')
        self.numeric_summary.config(
            text=f"Generador numérico: {gen_type.title()}",
            foreground='green' if gen_type != 'none' else 'gray'
        )
        
    def update_mapping_config(self, config_data: Dict):
        """Actualizar configuración de mapeo."""
        self.mapping_config = config_data
        
        # Contar mapeos dinámicos configurados
        mappings_count = 0
        if config_data:
            # Contar las columnas que tienen mapeo dinámico
            for key, mapping_dict in config_data.items():
                if isinstance(mapping_dict, dict) and mapping_dict:
                    mappings_count += 1
        
        self.mapping_summary.config(
            text=f"Mapeo: {mappings_count} configurados",
            foreground='green' if mappings_count > 0 else 'gray'
        )
        
    def _select_output_file(self):
        """Seleccionar archivo de salida."""
        file_path = filedialog.asksaveasfilename(
            title="Guardar archivo como",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            self.output_file_var.set(file_path)
            
    def _generate_preview(self):
        """Generar vista previa de los datos"""
        try:
            # Validar configuración mínima
            if not self.column_config.get('columns'):
                messagebox.showwarning("Advertencia", "No hay columnas configuradas")
                return
            
            # Obtener datos reales usando create_preview_data del ExportManager
            from models.column_config import ColumnConfig, DataType
            import pandas as pd
            
            # Convertir configuración de columnas a objetos ColumnConfig
            column_configs = []
            for col_data in self.column_config.get('columns', []):
                if isinstance(col_data, dict):
                    col_config = ColumnConfig.from_dict(col_data)  # Usar from_dict para cargar todos los campos
                    column_configs.append(col_config)
                else:
                    column_configs.append(col_data)
            
            # Obtener datos fuente del callback
            try:
                # Intentar obtener datos reales si están disponibles
                if hasattr(self, 'get_source_data_callback') and self.get_source_data_callback:
                    source_data = self.get_source_data_callback()
                    if source_data is not None and not source_data.empty:
                        preview_df = self.export_manager.create_preview_data(
                            source_data, 
                            column_configs, 
                            max_rows=self.preview_rows.get(),
                            mapping_config=self.mapping_config  # Pasar configuración de mapeo
                        )
                    else:
                        raise ValueError("No hay datos fuente disponibles")
                else:
                    raise ValueError("No hay callback para obtener datos fuente")
            except:
                # Crear datos de muestra si no hay datos reales disponibles
                columns_data = {}
                for col_config in column_configs:
                    col_name = col_config.display_name
                    columns_data[col_name] = [f"Dato {i+1}" for i in range(self.preview_rows.get())]
                
                preview_df = pd.DataFrame(columns_data)
            
            # Configurar treeview
            columns = list(preview_df.columns)
            self.preview_tree['columns'] = columns
            
            # Limpiar treeview
            for item in self.preview_tree.get_children():
                self.preview_tree.delete(item)
                
            # Configurar encabezados
            for col in columns:
                self.preview_tree.heading(col, text=col)
                self.preview_tree.column(col, width=100)
                
            # Agregar datos
            for _, row in preview_df.iterrows():
                self.preview_tree.insert('', 'end', values=list(row))
                
            # Actualizar información
            self.preview_info.config(
                text=f"Mostrando {len(preview_df)} filas de {len(columns)} columnas"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar vista previa: {str(e)}")
            
    def _validate_config(self):
        """Validar configuración antes de exportar."""
        try:
            errors = []
            warnings = []
            
            # Validar archivo de salida
            if not self.output_file_var.get():
                errors.append("Debe especificar un archivo de destino")
                
            # Validar columnas
            if not self.column_config.get('columns'):
                errors.append("Debe configurar al menos una columna")
                
            # Validar directorio de salida
            output_dir = os.path.dirname(self.output_file_var.get())
            if output_dir and not os.path.exists(output_dir):
                warnings.append(f"El directorio {output_dir} no existe")
                
            # Mostrar resultados
            if errors:
                messagebox.showerror("Errores de Validación", "\n".join(errors))
                self.validation_summary.config(text="Validación: Errores encontrados", 
                                              foreground='red')
            elif warnings:
                messagebox.showwarning("Advertencias", "\n".join(warnings))
                self.validation_summary.config(text="Validación: Advertencias", 
                                              foreground='orange')
            else:
                messagebox.showinfo("Validación", "Configuración válida")
                self.validation_summary.config(text="Validación: Exitosa", 
                                              foreground='green')
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en validación: {str(e)}")
            
    def _export_file(self):
        """Exportar archivo."""
        try:
            # Validar configuración
            self._validate_config()
            
            if self.validation_summary.cget('foreground') == 'red':
                messagebox.showerror("Error", "Corrija los errores de validación antes de exportar")
                return
            
            # Verificar si se dividirá en múltiples archivos
            split_warning = None
            if (hasattr(self, 'get_source_data_callback') and self.get_source_data_callback and 
                self.column_config.get('columns')):
                
                try:
                    source_data = self.get_source_data_callback()
                    if source_data is not None and not source_data.empty:
                        from models.column_config import ColumnConfig
                        column_configs = []
                        for col_data in self.column_config.get('columns', []):
                            if isinstance(col_data, dict):
                                col_config = ColumnConfig.from_dict(col_data)
                                column_configs.append(col_config)
                            else:
                                column_configs.append(col_data)
                        
                        export_info = self.export_manager.get_export_info(source_data, column_configs)
                        if export_info['will_split']:
                            split_warning = f"El archivo será dividido en {export_info['num_files']} partes debido a su tamaño ({export_info['total_rows']:,} filas). ¿Desea continuar?"
                except:
                    pass
            
            # Mostrar advertencia si se dividirá
            if split_warning:
                result = messagebox.askyesno("Archivo Grande", split_warning)
                if not result:
                    return
                
            # Preparar configuración de exportación
            export_config = {
                'output_file': self.output_file_var.get(),
                'format': self.format_var.get(),
                'sheet_name': self.sheet_name.get(),
                'include_headers': self.include_headers.get(),
                'auto_adjust_columns': self.auto_adjust_columns.get(),
                'apply_formatting': self.apply_formatting.get(),
                'create_backup': self.create_backup.get(),
                'max_rows': self.max_rows.get()
            }
            
            # Iniciar exportación
            self.export_status.config(text="Iniciando exportación...")
            self.export_progress.config(value=0)
            
            # Llamar callback de exportación
            self.on_export_requested(export_config)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
            self.export_status.config(text="Error en exportación")
            
    def _open_output_folder(self):
        """Abrir carpeta de destino."""
        output_file = self.output_file_var.get()
        if output_file:
            output_dir = os.path.dirname(output_file)
            if os.path.exists(output_dir):
                os.startfile(output_dir)  # Windows
            else:
                messagebox.showwarning("Advertencia", "La carpeta de destino no existe")
        else:
            messagebox.showwarning("Advertencia", "No se ha especificado un archivo de destino")
            
    def update_export_progress(self, value: float, status: str = "", files_created: int = None):
        """Actualizar progreso de exportación."""
        self.export_progress.config(value=value)
        
        if files_created and files_created > 1:
            status_text = f"{status} ({files_created} archivos creados)"
        else:
            status_text = status
            
        if status_text:
            self.export_status.config(text=status_text)