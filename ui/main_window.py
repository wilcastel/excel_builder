import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Optional
import pandas as pd

from config.settings import AppSettings
from core import FileManager, ColumnManager, NumericGenerator, MappingManager, ExportManager
from .frames import FileFrame, ColumnFrame, ExportFrame, UtilitiesFrame

class MainWindow:
    """Ventana principal de la aplicación"""
    
    def __init__(self, settings: AppSettings):
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        
        # Inicializar gestores
        self.file_manager = FileManager(settings)  # Requires settings
        self.column_manager = ColumnManager()      # No parameters
        self.numeric_generator = NumericGenerator()  # No parameters
        self.mapping_manager = MappingManager()    # No parameters
        self.export_manager = ExportManager(settings)  # Requires settings
        
        # Variables de estado
        self.source_file_path: Optional[str] = None
        self.base_file_path: Optional[str] = None
        
        self._create_main_window()
        self._create_frames()
        self._setup_bindings()
        
    def _create_main_window(self):
        """Crear la ventana principal."""
        self.root = tk.Tk()
        self.root.title(f"{self.settings.app_name} v{self.settings.app_version}")
        self.root.geometry(f"{self.settings.window_width}x{self.settings.window_height}")
        self.root.minsize(800, 600)
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use(self.settings.theme)
        
        # Crear notebook principal
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Barra de estado
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.status_var = tk.StringVar(value="Listo")
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var)
        self.status_label.pack(side='left')
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.status_frame, 
            variable=self.progress_var,
            length=200
        )
        self.progress_bar.pack(side='right', padx=(10, 0))
        
    def _create_frames(self):
        """Crear frames principales."""
        # Crear frame de archivos
        self.file_frame = FileFrame(
            self.notebook, 
            self.file_manager,
            on_source_loaded=self._on_source_file_loaded,
            on_base_loaded=self._on_base_file_loaded
        )
        self.notebook.add(self.file_frame, text="📁 Archivos")
        
        # Frame de configuración de columnas
        self.column_frame = ColumnFrame(
            self.notebook,
            self.column_manager,
            on_config_changed=self._on_column_config_changed,
            file_manager=self.file_manager
        )
        self.notebook.add(self.column_frame, text="📊 Columnas")
        
        # Frame de exportación
        self.export_frame = ExportFrame(
            self.notebook,
            self.export_manager,
            on_export_requested=self._on_export_requested
        )
        
        # Configurar callback para obtener datos fuente
        self.export_frame.get_source_data_callback = lambda: self.file_manager.get_source_data()
        self.notebook.add(self.export_frame, text="📤 Exportar")
        
        # Frame de utilidades
        self.utilities_frame = UtilitiesFrame(
            self.notebook,
            self.settings
        )
        self.notebook.add(self.utilities_frame, text="🔧 Utilidades")
        
    def _setup_bindings(self):
        """Configurar eventos y bindings."""
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Binding para cambio de tab
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        
    def _on_source_file_loaded(self, file_path: str, df_info: dict):
        """Callback cuando se carga el archivo fuente."""
        self.source_file_path = file_path
        self.logger.info(f"Archivo fuente cargado: {file_path}")
        
        # Actualizar frames dependientes
        self.column_frame.update_source_columns(df_info['columns'])
        
        self._update_status(f"Archivo fuente cargado: {df_info['rows']} filas, {df_info['columns_count']} columnas")
        
    def _on_base_file_loaded(self, file_path: str, df_info: dict):
        """Callback cuando se carga el archivo base."""
        self.base_file_path = file_path
        self.logger.info(f"Archivo base cargado: {file_path}")
        
        self._update_status(f"Archivo base cargado: {df_info['rows']} filas, {df_info['columns_count']} columnas")
        
    def _on_column_config_changed(self, config_data: dict):
        """Callback cuando cambia la configuración de columnas."""
        self.logger.debug("Configuración de columnas actualizada")
        self.export_frame.update_column_config(config_data)
        
        # Actualizar también el mapeo dinámico en el export frame
        mapping_config = self._create_mapping_from_columns()
        self.export_frame.update_mapping_config(mapping_config)
        
    def _on_export_requested(self, export_config: dict):
        """Callback cuando se solicita exportación."""
        try:
            self._update_status("Iniciando exportación...")
            self.progress_var.set(0)
            
            # Validar que hay archivo fuente
            if not self.file_manager.source_df is not None:
                raise ValueError("No se ha cargado un archivo fuente")
            
            # Crear mapeo dinámico desde las columnas configuradas
            mapping_config = self._create_mapping_from_columns()
            
            # Realizar exportación
            result = self.export_manager.export_excel(
                source_data=self.file_manager.get_source_data(),
                column_configs=self.column_manager.get_all_columns(),
                numeric_config=self.numeric_generator.get_config(),
                mapping_config=mapping_config,
                export_config=export_config,
                progress_callback=self._update_progress
            )
            
            # Actualizar estado final
            if result.get('files_created', 1) > 1:
                self._update_status(f"Exportación completada: {result['files_created']} archivos creados")
                messagebox.showinfo(
                    "Exportación Exitosa",
                    f"Se crearon {result['files_created']} archivos exitosamente:\n\n" +
                    f"Archivo principal: {result['file_path']}\n" +
                    f"Filas procesadas: {result['rows_processed']:,}\n\n" +
                    f"Todos los archivos:\n" + "\n".join(result.get('all_files', []))
                )
            else:
                self._update_status(f"Exportación completada: {result['file_path']}")
                messagebox.showinfo(
                    "Exportación Exitosa",
                    f"Archivo exportado exitosamente:\n{result['file_path']}\n\nFilas procesadas: {result['rows_processed']:,}"
                )
            
            self.progress_var.set(100)
            
        except Exception as e:
            self.logger.error(f"Error en exportación: {e}")
            self._update_status(f"Error en exportación: {str(e)}")
            messagebox.showerror("Error de Exportación", str(e))
    
    def _create_mapping_from_columns(self) -> dict:
        """Crear configuración de mapeo desde las columnas configuradas"""
        mapping_config = {}
        
        # Obtener datos del archivo base si está cargado
        if self.file_manager.base_df is None:
            return mapping_config
        
        base_data = self.file_manager.base_df
        
        # Revisar cada columna configurada que tenga mapeo dinámico
        for col_config in self.column_manager.get_all_columns():
            if (hasattr(col_config, 'mapping_source') and col_config.mapping_source and 
                hasattr(col_config, 'mapping_key_column') and col_config.mapping_key_column and 
                hasattr(col_config, 'mapping_value_column') and col_config.mapping_value_column):
                
                # Verificar que las columnas existen en el archivo base
                if (col_config.mapping_key_column in base_data.columns and 
                    col_config.mapping_value_column in base_data.columns):
                    
                    # Crear diccionario de mapeo
                    mapping_dict = {}
                    for _, row in base_data.iterrows():
                        key = str(row[col_config.mapping_key_column]).strip()
                        value = row[col_config.mapping_value_column]
                        
                        if key and not pd.isna(key) and key != "":
                            mapping_dict[key] = value
                    
                    # Guardar el mapeo usando la columna clave como identificador
                    mapping_config[col_config.mapping_key_column] = mapping_dict
                    
                    self.logger.info(f"Mapeo creado para '{col_config.display_name}': {len(mapping_dict)} entradas")
        
        return mapping_config
            
    def _on_tab_changed(self, event):
        """Callback cuando cambia el tab activo."""
        current_tab = self.notebook.index(self.notebook.select())
        tab_names = ["Archivos", "Columnas", "Exportar", "Utilidades"]
        
        if current_tab < len(tab_names):
            self._update_status(f"Sección activa: {tab_names[current_tab]}")
            
    def _update_status(self, message: str):
        """Actualizar mensaje de estado."""
        self.status_var.set(message)
        self.root.update_idletasks()
        
    def _update_progress(self, value: float):
        """Actualizar barra de progreso."""
        self.progress_var.set(value)
        self.root.update_idletasks()
        
    def _on_closing(self):
        """Callback al cerrar la aplicación."""
        try:
            # Guardar configuraciones si es necesario
            self.logger.info("Cerrando aplicación")
            self.root.destroy()
        except Exception as e:
            self.logger.error(f"Error al cerrar: {e}")
            self.root.destroy()
            
    def run(self):
        """Ejecutar la aplicación."""
        try:
            self.logger.info(f"Iniciando {self.settings.app_name} v{self.settings.app_version}")
            self._update_status("Aplicación iniciada - Cargue un archivo fuente para comenzar")
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"Error crítico: {e}")
            messagebox.showerror("Error Crítico", f"Error inesperado: {str(e)}")