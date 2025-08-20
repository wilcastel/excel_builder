# -*- coding: utf-8 -*-
"""
Gestor de configuración de columnas
"""

from typing import List, Dict, Optional, Any
import logging
from models.column_config import ColumnConfig, DataType

class ColumnManager:
    """Gestor para configuración y manejo de columnas"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.columns: List[ColumnConfig] = []
        self.selected_source_columns: List[str] = []
        
    def add_column(self, column_config: ColumnConfig) -> bool:
        """Agregar nueva columna"""
        try:
            # Validar configuración
            errors = column_config.validate()
            if errors:
                self.logger.error(f"Errores en configuración de columna: {errors}")
                return False
            
            # Verificar que no exista una columna con el mismo nombre
            if any(col.name == column_config.name for col in self.columns):
                self.logger.error(f"Ya existe una columna con el nombre: {column_config.name}")
                return False
            
            # Asignar posición si no está definida
            if column_config.position == 0:
                column_config.position = len(self.columns) + 1
            
            self.columns.append(column_config)
            self.logger.info(f"Columna agregada: {column_config.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error agregando columna: {e}")
            return False
    
    def remove_column(self, column_name: str) -> bool:
        """Eliminar columna por nombre"""
        try:
            self.columns = [col for col in self.columns if col.name != column_name]
            self._reorder_positions()
            self.logger.info(f"Columna eliminada: {column_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error eliminando columna: {e}")
            return False
    
    def move_column(self, column_name: str, direction: str) -> bool:
        """Mover columna arriba o abajo"""
        try:
            column_index = next((i for i, col in enumerate(self.columns) if col.name == column_name), -1)
            
            if column_index == -1:
                return False
            
            if direction == "up" and column_index > 0:
                self.columns[column_index], self.columns[column_index - 1] = \
                    self.columns[column_index - 1], self.columns[column_index]
            elif direction == "down" and column_index < len(self.columns) - 1:
                self.columns[column_index], self.columns[column_index + 1] = \
                    self.columns[column_index + 1], self.columns[column_index]
            else:
                return False
            
            self._reorder_positions()
            return True
            
        except Exception as e:
            self.logger.error(f"Error moviendo columna: {e}")
            return False
    
    def update_column(self, column_name: str, **kwargs) -> bool:
        """Actualizar configuración de columna"""
        try:
            column = next((col for col in self.columns if col.name == column_name), None)
            if not column:
                return False
            
            # Actualizar atributos con conversión de tipos
            for key, value in kwargs.items():
                if hasattr(column, key):
                    # Convertir data_type de string a enum si es necesario
                    if key == 'data_type' and isinstance(value, str):
                        try:
                            value = DataType(value)
                        except ValueError:
                            self.logger.error(f"Tipo de dato inválido: {value}")
                            return False
                    
                    setattr(column, key, value)
            
            # Validar después de actualizar
            errors = column.validate()
            if errors:
                self.logger.error(f"Errores en configuración actualizada: {errors}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error actualizando columna: {e}")
            return False
    
    def get_column(self, column_name: str) -> Optional[ColumnConfig]:
        """Obtener configuración de columna por nombre"""
        return next((col for col in self.columns if col.name == column_name), None)
    
    def get_all_columns(self) -> List[ColumnConfig]:
        """Obtener todas las columnas ordenadas por posición"""
        return sorted(self.columns, key=lambda x: x.position)
    
    def get_source_columns(self) -> List[ColumnConfig]:
        """Obtener columnas que provienen del archivo fuente"""
        return [col for col in self.columns if col.source_column and not col.is_generated]
    
    def get_generated_columns(self) -> List[ColumnConfig]:
        """Obtener columnas generadas"""
        return [col for col in self.columns if col.is_generated]
    
    def set_selected_source_columns(self, columns: List[str]):
        """Establecer columnas seleccionadas del archivo fuente"""
        self.selected_source_columns = columns
        self.logger.info(f"Columnas fuente seleccionadas: {len(columns)}")
    
    def create_columns_from_source(self, source_columns: List[str]) -> bool:
        """Crear configuraciones de columna desde columnas fuente"""
        try:
            for col_name in source_columns:
                if col_name in self.selected_source_columns:
                    column_config = ColumnConfig(
                        name=col_name,
                        display_name=col_name,
                        data_type=DataType.TEXT,
                        source_column=col_name,
                        position=len(self.columns) + 1
                    )
                    self.add_column(column_config)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error creando columnas desde fuente: {e}")
            return False
    
    def _reorder_positions(self):
        """Reordenar posiciones de columnas"""
        for i, column in enumerate(self.columns):
            column.position = i + 1
    
    def validate_all_columns(self) -> List[str]:
        """Validar todas las configuraciones de columnas"""
        all_errors = []
        
        for column in self.columns:
            errors = column.validate()
            if errors:
                all_errors.extend([f"{column.name}: {error}" for error in errors])
        
        return all_errors
    
    def clear_columns(self):
        """Limpiar todas las columnas"""
        self.columns.clear()
        self.selected_source_columns.clear()
        self.logger.info("Columnas limpiadas")
    
    def export_config(self) -> Dict[str, Any]:
        """Exportar configuración de columnas"""
        return {
            'columns': [col.to_dict() for col in self.columns],
            'selected_source_columns': self.selected_source_columns
        }
    
    def import_config(self, config: Dict[str, Any]) -> bool:
        """Importar configuración de columnas"""
        try:
            self.clear_columns()
            
            # Importar columnas
            for col_data in config.get('columns', []):
                column = ColumnConfig.from_dict(col_data)
                self.add_column(column)
            
            # Importar selección de columnas fuente
            self.selected_source_columns = config.get('selected_source_columns', [])
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error importando configuración: {e}")
            return False