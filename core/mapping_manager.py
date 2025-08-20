# -*- coding: utf-8 -*-
"""
Gestor de mapeo dinámico desde archivo base
"""

import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
import logging

class MappingManager:
    """Gestor para mapeo de datos desde archivo base"""
    
    def __init__(self):
        self.mappings: Dict[str, Dict] = {}
        self.logger = logging.getLogger(__name__)
        self.base_df = None  # Agregar referencia al archivo base
    
    def set_base_dataframe(self, base_df: pd.DataFrame):
        """Establecer el DataFrame base para crear mapeos"""
        self.base_df = base_df
        self.logger.info(f"DataFrame base establecido con {len(base_df)} filas")
    
    def add_simple_mapping(self, source_column: str, base_key_column: str, base_value_column: str) -> bool:
        """Agregar mapeo simple usando el archivo base"""
        try:
            if self.base_df is None:
                raise ValueError("No se ha cargado un archivo base para crear el mapeo")
            
            # Validar que las columnas existen en el archivo base
            if base_key_column not in self.base_df.columns:
                raise ValueError(f"Columna clave no encontrada en archivo base: {base_key_column}")
            
            if base_value_column not in self.base_df.columns:
                raise ValueError(f"Columna valor no encontrada en archivo base: {base_value_column}")
            
            mapping_name = f"simple_{source_column}_{base_key_column}_{base_value_column}"
            
            # Crear diccionario de mapeo real
            mapping_dict = {}
            for _, row in self.base_df.iterrows():
                key = str(row[base_key_column]).strip()
                value = row[base_value_column]
                
                if pd.notna(key) and key != "":
                    mapping_dict[key] = value
            
            # Guardar mapeo completo
            self.mappings[mapping_name] = {
                'type': 'simple',
                'source_column': source_column,
                'base_key_column': base_key_column,
                'base_value_column': base_value_column,
                'mapping': mapping_dict,  # Este es el diccionario que necesita ExportManager
                'total_entries': len(mapping_dict)
            }
            
            self.logger.info(f"Mapeo simple creado: {mapping_name} con {len(mapping_dict)} entradas")
            return True
            
        except Exception as e:
            self.logger.error(f"Error agregando mapeo simple: {e}")
            return False
    
    def create_mapping(self,
                      base_df: pd.DataFrame,
                      key_column: str,
                      value_column: str,
                      mapping_name: str) -> bool:
        """Crear mapeo desde archivo base"""
        try:
            # Validar columnas
            if key_column not in base_df.columns:
                raise ValueError(f"Columna clave no encontrada: {key_column}")
            
            if value_column not in base_df.columns:
                raise ValueError(f"Columna valor no encontrada: {value_column}")
            
            # Crear diccionario de mapeo
            mapping_dict = {}
            for _, row in base_df.iterrows():
                key = str(row[key_column]).strip()
                value = row[value_column]
                
                if pd.notna(key) and key != "":
                    mapping_dict[key] = value
            
            # Guardar mapeo
            self.mappings[mapping_name] = {
                'mapping': mapping_dict,
                'key_column': key_column,
                'value_column': value_column,
                'total_entries': len(mapping_dict)
            }
            
            self.logger.info(f"Mapeo '{mapping_name}' creado con {len(mapping_dict)} entradas")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creando mapeo: {e}")
            return False
    
    def apply_mapping(self,
                     source_df: pd.DataFrame,
                     source_column: str,
                     mapping_name: str,
                     default_value: Any = None) -> List[Any]:
        """Aplicar mapeo a columna del archivo fuente"""
        try:
            if mapping_name not in self.mappings:
                raise ValueError(f"Mapeo no encontrado: {mapping_name}")
            
            if source_column not in source_df.columns:
                raise ValueError(f"Columna fuente no encontrada: {source_column}")
            
            mapping_dict = self.mappings[mapping_name]['mapping']
            mapped_values = []
            
            for _, row in source_df.iterrows():
                source_value = str(row[source_column]).strip()
                mapped_value = mapping_dict.get(source_value, default_value)
                mapped_values.append(mapped_value)
            
            return mapped_values
            
        except Exception as e:
            self.logger.error(f"Error aplicando mapeo: {e}")
            return []
    
    def create_multi_column_mapping(self,
                                  base_df: pd.DataFrame,
                                  key_columns: List[str],
                                  value_columns: List[str],
                                  mapping_name: str,
                                  separator: str = "_") -> bool:
        """Crear mapeo con múltiples columnas clave y valor"""
        try:
            # Validar columnas
            missing_keys = [col for col in key_columns if col not in base_df.columns]
            missing_values = [col for col in value_columns if col not in base_df.columns]
            
            if missing_keys:
                raise ValueError(f"Columnas clave no encontradas: {missing_keys}")
            
            if missing_values:
                raise ValueError(f"Columnas valor no encontradas: {missing_values}")
            
            # Crear mapeo compuesto
            mapping_dict = {}
            for _, row in base_df.iterrows():
                # Crear clave compuesta
                key_parts = [str(row[col]).strip() for col in key_columns]
                composite_key = separator.join(key_parts)
                
                # Crear valor compuesto o diccionario
                if len(value_columns) == 1:
                    value = row[value_columns[0]]
                else:
                    value = {col: row[col] for col in value_columns}
                
                if composite_key and composite_key != separator * (len(key_columns) - 1):
                    mapping_dict[composite_key] = value
            
            # Guardar mapeo
            self.mappings[mapping_name] = {
                'mapping': mapping_dict,
                'key_columns': key_columns,
                'value_columns': value_columns,
                'separator': separator,
                'total_entries': len(mapping_dict)
            }
            
            self.logger.info(f"Mapeo multi-columna '{mapping_name}' creado con {len(mapping_dict)} entradas")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creando mapeo multi-columna: {e}")
            return False
    
    def apply_multi_column_mapping(self,
                                 source_df: pd.DataFrame,
                                 source_columns: List[str],
                                 mapping_name: str,
                                 target_column: str = None,
                                 default_value: Any = None) -> List[Any]:
        """Aplicar mapeo multi-columna"""
        try:
            if mapping_name not in self.mappings:
                raise ValueError(f"Mapeo no encontrado: {mapping_name}")
            
            mapping_info = self.mappings[mapping_name]
            mapping_dict = mapping_info['mapping']
            separator = mapping_info.get('separator', '_')
            
            # Validar columnas fuente
            missing_columns = [col for col in source_columns if col not in source_df.columns]
            if missing_columns:
                raise ValueError(f"Columnas fuente no encontradas: {missing_columns}")
            
            mapped_values = []
            
            for _, row in source_df.iterrows():
                # Crear clave compuesta
                key_parts = [str(row[col]).strip() for col in source_columns]
                composite_key = separator.join(key_parts)
                
                # Buscar valor mapeado
                mapped_value = mapping_dict.get(composite_key, default_value)
                
                # Si el valor es un diccionario y se especifica columna objetivo
                if isinstance(mapped_value, dict) and target_column:
                    mapped_value = mapped_value.get(target_column, default_value)
                
                mapped_values.append(mapped_value)
            
            return mapped_values
            
        except Exception as e:
            self.logger.error(f"Error aplicando mapeo multi-columna: {e}")
            return []
    
    def get_mapping_info(self, mapping_name: str) -> Dict[str, Any]:
        """Obtener información de un mapeo"""
        if mapping_name in self.mappings:
            return self.mappings[mapping_name].copy()
        return {}
    
    def get_all_mappings(self) -> List[str]:
        """Obtener lista de todos los mapeos"""
        return list(self.mappings.keys())
    
    def validate_mapping(self, mapping_name: str) -> List[str]:
        """Validar un mapeo específico"""
        errors = []
        
        if mapping_name not in self.mappings:
            errors.append(f"Mapeo '{mapping_name}' no existe")
            return errors
        
        mapping_info = self.mappings[mapping_name]
        mapping_dict = mapping_info.get('mapping', {})
        
        if not mapping_dict:
            errors.append(f"Mapeo '{mapping_name}' está vacío")
        
        # Verificar valores nulos
        null_keys = [k for k, v in mapping_dict.items() if pd.isna(v)]
        if null_keys:
            errors.append(f"Mapeo '{mapping_name}' tiene {len(null_keys)} valores nulos")
        
        return errors
    
    def get_mapping_statistics(self, mapping_name: str) -> Dict[str, Any]:
        """Obtener estadísticas de un mapeo"""
        if mapping_name not in self.mappings:
            return {}
        
        mapping_dict = self.mappings[mapping_name]['mapping']
        
        # Contar tipos de valores
        value_types = {}
        null_count = 0
        
        for value in mapping_dict.values():
            if pd.isna(value):
                null_count += 1
            else:
                value_type = type(value).__name__
                value_types[value_type] = value_types.get(value_type, 0) + 1
        
        return {
            'total_entries': len(mapping_dict),
            'null_values': null_count,
            'value_types': value_types,
            'unique_values': len(set(mapping_dict.values()))
        }
    
    def clear_mapping(self, mapping_name: str) -> bool:
        """Eliminar un mapeo específico"""
        if mapping_name in self.mappings:
            del self.mappings[mapping_name]
            self.logger.info(f"Mapeo '{mapping_name}' eliminado")
            return True
        return False
    
    def clear_all_mappings(self):
        """Eliminar todos los mapeos"""
        self.mappings.clear()
        self.logger.info("Todos los mapeos eliminados")
    
    def export_mappings(self) -> Dict[str, Any]:
        """Exportar todos los mapeos"""
        return {
            'mappings': self.mappings,
            'total_mappings': len(self.mappings)
        }
    
    def import_mappings(self, mappings_data: Dict[str, Any]) -> bool:
        """Importar mapeos desde datos"""
        try:
            self.mappings = mappings_data.get('mappings', {})
            self.logger.info(f"Importados {len(self.mappings)} mapeos")
            return True
        except Exception as e:
            self.logger.error(f"Error importando mapeos: {e}")
            return False
    
    def get_config(self) -> Dict[str, Any]:
        """Obtener configuración actual de mapeos"""
        return {
            'mappings': self.mappings,
            'total_mappings': len(self.mappings)
        }