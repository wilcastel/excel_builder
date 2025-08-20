# -*- coding: utf-8 -*-
"""
Frame de Utilidades - Excel Builder Pro
Funcionalidades para división de archivos y eliminación de duplicados
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

class UtilitiesFrame(ttk.Frame):
    """Frame para utilidades de archivos Excel"""
    
    def __init__(self, parent, settings):
        super().__init__(parent)
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        
        # Variables
        self.source_data = None
        self.source_file_path = None
        self.duplicate_criteria = []
        self.duplicate_groups = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interfaz de usuario"""
        # Notebook para las dos funcionalidades
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña de división de archivos
        self.split_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.split_frame, text="División de Archivos")
        self.setup_split_ui()
        
        # Pestaña de eliminación de duplicados
        self.duplicates_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.duplicates_frame, text="Eliminar Duplicados")
        self.setup_duplicates_ui()
    
    def setup_split_ui(self):
        """Configurar interfaz para división de archivos"""
        # Frame principal
        main_frame = ttk.Frame(self.split_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sección de archivo fuente
        source_frame = ttk.LabelFrame(main_frame, text="Archivo Fuente", padding=10)
        source_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Selección de archivo
        file_frame = ttk.Frame(source_frame)
        file_frame.pack(fill=tk.X)
        
        ttk.Label(file_frame, text="Archivo Excel:").pack(side=tk.LEFT)
        self.file_path_var = tk.StringVar()
        self.file_path_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, width=50)
        self.file_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 5))
        
        ttk.Button(file_frame, text="Examinar...", command=self.select_source_file).pack(side=tk.RIGHT)
        
        # Información del archivo
        self.file_info_frame = ttk.Frame(source_frame)
        self.file_info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.file_info_label = ttk.Label(self.file_info_frame, text="No se ha seleccionado ningún archivo")
        self.file_info_label.pack()
        
        # Sección de configuración de división
        config_frame = ttk.LabelFrame(main_frame, text="Configuración de División", padding=10)
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Filas por archivo
        rows_frame = ttk.Frame(config_frame)
        rows_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(rows_frame, text="Filas por archivo:").pack(side=tk.LEFT)
        self.rows_per_file_var = tk.StringVar(value="5000")
        self.rows_per_file_entry = ttk.Entry(rows_frame, textvariable=self.rows_per_file_var, width=10)
        self.rows_per_file_entry.pack(side=tk.LEFT, padx=(10, 5))
        ttk.Label(rows_frame, text="(máximo 10,000 recomendado)").pack(side=tk.LEFT)
        
        # Prefijo de archivos
        prefix_frame = ttk.Frame(config_frame)
        prefix_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(prefix_frame, text="Prefijo de archivos:").pack(side=tk.LEFT)
        self.file_prefix_var = tk.StringVar(value="archivo_dividido")
        self.file_prefix_entry = ttk.Entry(prefix_frame, textvariable=self.file_prefix_var, width=30)
        self.file_prefix_entry.pack(side=tk.LEFT, padx=(10, 5))
        
        # Información de división
        self.split_info_frame = ttk.Frame(config_frame)
        self.split_info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.split_info_label = ttk.Label(self.split_info_frame, text="")
        self.split_info_label.pack()
        
        # Botones de acción
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(buttons_frame, text="Calcular División", command=self.calculate_split).pack(side=tk.LEFT, padx=(0, 10))
        self.split_button = ttk.Button(buttons_frame, text="Dividir Archivo", command=self.split_file, state=tk.DISABLED)
        self.split_button.pack(side=tk.LEFT)
        
        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Estado
        self.status_var = tk.StringVar(value="Listo para dividir archivos")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.pack(pady=(5, 0))
    
    def setup_duplicates_ui(self):
        """Configurar interfaz para eliminación de duplicados"""
        # Frame principal
        main_frame = ttk.Frame(self.duplicates_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sección de archivo fuente
        source_frame = ttk.LabelFrame(main_frame, text="Archivo Fuente", padding=10)
        source_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Selección de archivo
        file_frame = ttk.Frame(source_frame)
        file_frame.pack(fill=tk.X)
        
        ttk.Label(file_frame, text="Archivo Excel:").pack(side=tk.LEFT)
        self.dup_file_path_var = tk.StringVar()
        self.dup_file_path_entry = ttk.Entry(file_frame, textvariable=self.dup_file_path_var, width=50)
        self.dup_file_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 5))
        
        ttk.Button(file_frame, text="Examinar...", command=self.select_duplicates_file).pack(side=tk.RIGHT)
        
        # Información del archivo
        self.dup_file_info_label = ttk.Label(source_frame, text="No se ha seleccionado ningún archivo")
        self.dup_file_info_label.pack(pady=(10, 0))
        
        # Sección de criterios de duplicados
        criteria_frame = ttk.LabelFrame(main_frame, text="Criterios de Duplicados", padding=10)
        criteria_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Lista de columnas disponibles
        columns_frame = ttk.Frame(criteria_frame)
        columns_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(columns_frame, text="Columnas disponibles:").pack(anchor=tk.W)
        
        # Frame para listbox y botones
        list_frame = ttk.Frame(columns_frame)
        list_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Lista de columnas disponibles
        self.available_columns_listbox = tk.Listbox(list_frame, height=6, selectmode=tk.MULTIPLE)
        self.available_columns_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar para la lista
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.available_columns_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.available_columns_listbox.config(yscrollcommand=scrollbar.set)
        
        # Botones para agregar/quitar criterios
        criteria_buttons_frame = ttk.Frame(criteria_frame)
        criteria_buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(criteria_buttons_frame, text="Agregar Criterio", command=self.add_criteria).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(criteria_buttons_frame, text="Limpiar Criterios", command=self.clear_criteria).pack(side=tk.LEFT)
        
        # Lista de criterios seleccionados
        selected_frame = ttk.Frame(criteria_frame)
        selected_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(selected_frame, text="Criterios seleccionados:").pack(anchor=tk.W)
        
        self.selected_criteria_listbox = tk.Listbox(selected_frame, height=4)
        self.selected_criteria_listbox.pack(fill=tk.X, pady=(5, 0))
        
        # Botones de acción
        action_buttons_frame = ttk.Frame(main_frame)
        action_buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(action_buttons_frame, text="Buscar Duplicados", command=self.find_duplicates).pack(side=tk.LEFT, padx=(0, 10))
        self.export_duplicates_button = ttk.Button(action_buttons_frame, text="Exportar Duplicados", command=self.export_duplicates, state=tk.DISABLED)
        self.export_duplicates_button.pack(side=tk.LEFT, padx=(0, 10))
        self.remove_duplicates_button = ttk.Button(action_buttons_frame, text="Eliminar Duplicados", command=self.remove_duplicates, state=tk.DISABLED)
        self.remove_duplicates_button.pack(side=tk.LEFT)
        
        # Información de duplicados
        self.duplicates_info_label = ttk.Label(main_frame, text="")
        self.duplicates_info_label.pack(pady=(10, 0))
        
        # Vista previa de duplicados
        preview_frame = ttk.LabelFrame(main_frame, text="Vista Previa de Duplicados", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Treeview para mostrar duplicados
        self.duplicates_tree = ttk.Treeview(preview_frame, show="tree")
        self.duplicates_tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar para treeview
        tree_scrollbar = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.duplicates_tree.yview)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.duplicates_tree.config(yscrollcommand=tree_scrollbar.set)
    
    def select_source_file(self):
        """Seleccionar archivo fuente para división"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Archivos Excel", "*.xlsx *.xls"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            self.file_path_var.set(file_path)
            self.load_file_info(file_path)
    
    def select_duplicates_file(self):
        """Seleccionar archivo fuente para duplicados"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Archivos Excel", "*.xlsx *.xls"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            self.dup_file_path_var.set(file_path)
            self.load_duplicates_file_info(file_path)
    
    def load_file_info(self, file_path: str):
        """Cargar información del archivo"""
        try:
            # Leer información del archivo
            df = pd.read_excel(file_path, nrows=1)  # Solo leer encabezados
            total_rows = len(pd.read_excel(file_path))
            
            file_size = Path(file_path).stat().st_size / (1024 * 1024)  # MB
            
            info_text = f"Archivo: {Path(file_path).name}\n"
            info_text += f"Filas: {total_rows:,}\n"
            info_text += f"Columnas: {len(df.columns)}\n"
            info_text += f"Tamaño: {file_size:.2f} MB"
            
            self.file_info_label.config(text=info_text)
            
            # Calcular división automáticamente
            self.calculate_split()
            
        except Exception as e:
            self.logger.error(f"Error cargando información del archivo: {e}")
            messagebox.showerror("Error", f"Error al cargar el archivo: {e}")
    
    def load_duplicates_file_info(self, file_path: str):
        """Cargar información del archivo para duplicados"""
        try:
            # Leer información del archivo
            df = pd.read_excel(file_path, nrows=1)  # Solo leer encabezados
            total_rows = len(pd.read_excel(file_path))
            
            info_text = f"Archivo: {Path(file_path).name} | Filas: {total_rows:,} | Columnas: {len(df.columns)}"
            self.dup_file_info_label.config(text=info_text)
            
            # Cargar columnas disponibles
            self.load_available_columns(df.columns.tolist())
            
        except Exception as e:
            self.logger.error(f"Error cargando información del archivo: {e}")
            messagebox.showerror("Error", f"Error al cargar el archivo: {e}")
    
    def load_available_columns(self, columns: List[str]):
        """Cargar columnas disponibles en la lista"""
        self.available_columns_listbox.delete(0, tk.END)
        for column in columns:
            self.available_columns_listbox.insert(tk.END, column)
    
    def calculate_split(self):
        """Calcular información de división"""
        try:
            file_path = self.file_path_var.get()
            if not file_path:
                messagebox.showwarning("Advertencia", "Selecciona un archivo primero")
                return
            
            rows_per_file = int(self.rows_per_file_var.get())
            if rows_per_file <= 0:
                messagebox.showerror("Error", "El número de filas por archivo debe ser mayor a 0")
                return
            
            # Leer archivo para obtener total de filas
            df = pd.read_excel(file_path)
            total_rows = len(df)
            
            # Calcular número de archivos
            num_files = (total_rows + rows_per_file - 1) // rows_per_file
            
            # Calcular tamaño estimado por archivo
            file_size = Path(file_path).stat().st_size / (1024 * 1024)  # MB
            estimated_size_per_file = file_size / num_files
            
            info_text = f"División calculada:\n"
            info_text += f"• Total de filas: {total_rows:,}\n"
            info_text += f"• Filas por archivo: {rows_per_file:,}\n"
            info_text += f"• Número de archivos: {num_files}\n"
            info_text += f"• Tamaño estimado por archivo: {estimated_size_per_file:.2f} MB"
            
            self.split_info_label.config(text=info_text)
            
            # Habilitar botón de división
            self.split_button.config(state=tk.NORMAL)
            
        except Exception as e:
            self.logger.error(f"Error calculando división: {e}")
            messagebox.showerror("Error", f"Error al calcular la división: {e}")
    
    def split_file(self):
        """Dividir archivo en partes"""
        try:
            file_path = self.file_path_var.get()
            rows_per_file = int(self.rows_per_file_var.get())
            prefix = self.file_prefix_var.get()
            
            if not prefix:
                prefix = "archivo_dividido"
            
            self.status_var.set("Dividiendo archivo...")
            self.progress_var.set(0)
            
            # Leer archivo completo
            df = pd.read_excel(file_path)
            total_rows = len(df)
            num_files = (total_rows + rows_per_file - 1) // rows_per_file
            
            # Crear directorio de exportación
            export_dir = Path(self.settings.default_export_dir)
            export_dir.mkdir(exist_ok=True)
            
            created_files = []
            
            for i in range(num_files):
                # Actualizar progreso
                progress = (i / num_files) * 100
                self.progress_var.set(progress)
                self.status_var.set(f"Procesando archivo {i + 1} de {num_files}...")
                self.update()
                
                # Calcular rango de filas
                start_row = i * rows_per_file
                end_row = min((i + 1) * rows_per_file, total_rows)
                
                # Extraer datos para este archivo
                file_data = df.iloc[start_row:end_row].copy()
                
                # Generar nombre de archivo
                if num_files == 1:
                    output_filename = f"{prefix}.xlsx"
                else:
                    output_filename = f"{prefix}_parte_{i + 1:03d}_de_{num_files:03d}.xlsx"
                
                output_path = export_dir / output_filename
                
                # Guardar archivo
                file_data.to_excel(output_path, index=False)
                created_files.append(output_filename)
            
            # Completar progreso
            self.progress_var.set(100)
            self.status_var.set(f"División completada. Se crearon {len(created_files)} archivos")
            
            messagebox.showinfo("Éxito", f"Archivo dividido exitosamente en {len(created_files)} partes.\n\nArchivos creados:\n" + "\n".join(created_files))
            
        except Exception as e:
            self.logger.error(f"Error dividiendo archivo: {e}")
            messagebox.showerror("Error", f"Error al dividir el archivo: {e}")
            self.status_var.set("Error en la división")
    
    def add_criteria(self):
        """Agregar criterio de duplicados"""
        selected_indices = self.available_columns_listbox.curselection()
        
        if not selected_indices:
            messagebox.showwarning("Advertencia", "Selecciona al menos una columna")
            return
        
        for index in selected_indices:
            column = self.available_columns_listbox.get(index)
            if column not in self.duplicate_criteria:
                self.duplicate_criteria.append(column)
                self.selected_criteria_listbox.insert(tk.END, column)
    
    def clear_criteria(self):
        """Limpiar criterios de duplicados"""
        self.duplicate_criteria.clear()
        self.selected_criteria_listbox.delete(0, tk.END)
        self.duplicates_tree.delete(*self.duplicates_tree.get_children())
        self.duplicates_info_label.config(text="")
        self.export_duplicates_button.config(state=tk.DISABLED)
        self.remove_duplicates_button.config(state=tk.DISABLED)
    
    def find_duplicates(self):
        """Buscar duplicados según criterios"""
        try:
            if not self.duplicate_criteria:
                messagebox.showwarning("Advertencia", "Selecciona al menos un criterio")
                return
            
            file_path = self.dup_file_path_var.get()
            if not file_path:
                messagebox.showwarning("Advertencia", "Selecciona un archivo primero")
                return
            
            # Leer archivo
            df = pd.read_excel(file_path)
            
            # Buscar duplicados
            duplicates = df[df.duplicated(subset=self.duplicate_criteria, keep=False)]
            
            if duplicates.empty:
                messagebox.showinfo("Información", "No se encontraron duplicados con los criterios seleccionados")
                return
            
            # Agrupar duplicados
            self.duplicate_groups = []
            grouped = duplicates.groupby(self.duplicate_criteria)
            
            for group_key, group_data in grouped:
                if len(group_data) > 1:  # Solo grupos con más de una fila
                    self.duplicate_groups.append({
                        'key': group_key,
                        'data': group_data,
                        'count': len(group_data)
                    })
            
            # Mostrar información
            total_duplicates = len(duplicates)
            total_groups = len(self.duplicate_groups)
            
            info_text = f"Duplicados encontrados:\n"
            info_text += f"• Total de filas duplicadas: {total_duplicates}\n"
            info_text += f"• Grupos de duplicados: {total_groups}"
            
            self.duplicates_info_label.config(text=info_text)
            
            # Mostrar duplicados en treeview
            self.show_duplicates_in_tree()
            
            # Habilitar botones
            self.export_duplicates_button.config(state=tk.NORMAL)
            self.remove_duplicates_button.config(state=tk.NORMAL)
            
        except Exception as e:
            self.logger.error(f"Error buscando duplicados: {e}")
            messagebox.showerror("Error", f"Error al buscar duplicados: {e}")
    
    def show_duplicates_in_tree(self):
        """Mostrar duplicados en el treeview"""
        # Limpiar treeview
        self.duplicates_tree.delete(*self.duplicates_tree.get_children())
        
        for i, group in enumerate(self.duplicate_groups):
            # Crear nodo principal para el grupo
            group_id = f"group_{i}"
            group_text = f"Grupo {i + 1} - {group['count']} filas duplicadas"
            
            # Crear texto de criterios
            criteria_text = " | ".join([f"{col}: {val}" for col, val in zip(self.duplicate_criteria, group['key'])])
            
            group_item = self.duplicates_tree.insert("", "end", group_id, text=f"{group_text} - {criteria_text}")
            
            # Agregar filas duplicadas como hijos
            for j, (idx, row) in enumerate(group['data'].iterrows()):
                row_text = f"Fila {idx + 1}: {row.iloc[0] if len(row) > 0 else 'N/A'}"  # Mostrar primera columna
                self.duplicates_tree.insert(group_item, "end", f"{group_id}_row_{j}", text=row_text)
    
    def export_duplicates(self):
        """Exportar duplicados a archivo Excel"""
        try:
            if not self.duplicate_groups:
                messagebox.showwarning("Advertencia", "No hay duplicados para exportar")
                return
            
            # Crear DataFrame con todos los duplicados
            all_duplicates = []
            for group in self.duplicate_groups:
                group_data = group['data'].copy()
                group_data['Grupo_Duplicado'] = f"Grupo_{len(all_duplicates) + 1}"
                all_duplicates.append(group_data)
            
            duplicates_df = pd.concat(all_duplicates, ignore_index=True)
            
            # Generar nombre de archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"duplicados_{timestamp}.xlsx"
            
            # Guardar archivo
            export_dir = Path(self.settings.default_export_dir)
            export_dir.mkdir(exist_ok=True)
            output_path = export_dir / filename
            
            duplicates_df.to_excel(output_path, index=False)
            
            messagebox.showinfo("Éxito", f"Duplicados exportados exitosamente a:\n{output_path}")
            
        except Exception as e:
            self.logger.error(f"Error exportando duplicados: {e}")
            messagebox.showerror("Error", f"Error al exportar duplicados: {e}")
    
    def remove_duplicates(self):
        """Eliminar duplicados del archivo original"""
        try:
            if not self.duplicate_groups:
                messagebox.showwarning("Advertencia", "No hay duplicados para eliminar")
                return
            
            # Confirmar eliminación
            total_duplicates = sum(len(group['data']) for group in self.duplicate_groups)
            response = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Estás seguro de que quieres eliminar {total_duplicates} filas duplicadas?\n\n"
                "Esta acción no se puede deshacer."
            )
            
            if not response:
                return
            
            file_path = self.dup_file_path_var.get()
            
            # Leer archivo original
            df = pd.read_excel(file_path)
            original_rows = len(df)
            
            # Eliminar duplicados (mantener la primera ocurrencia)
            df_clean = df.drop_duplicates(subset=self.duplicate_criteria, keep='first')
            remaining_rows = len(df_clean)
            removed_rows = original_rows - remaining_rows
            
            # Generar nombre de archivo limpio
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"archivo_sin_duplicados_{timestamp}.xlsx"
            
            # Guardar archivo limpio
            export_dir = Path(self.settings.default_export_dir)
            export_dir.mkdir(exist_ok=True)
            output_path = export_dir / filename
            
            df_clean.to_excel(output_path, index=False)
            
            messagebox.showinfo(
                "Éxito", 
                f"Duplicados eliminados exitosamente:\n\n"
                f"• Filas originales: {original_rows:,}\n"
                f"• Filas eliminadas: {removed_rows:,}\n"
                f"• Filas restantes: {remaining_rows:,}\n\n"
                f"Archivo guardado como: {filename}"
            )
            
            # Limpiar interfaz
            self.clear_criteria()
            
        except Exception as e:
            self.logger.error(f"Error eliminando duplicados: {e}")
            messagebox.showerror("Error", f"Error al eliminar duplicados: {e}")
