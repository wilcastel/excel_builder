# -*- coding: utf-8 -*-
"""
Gestor de mapeo dinámico desde archivo base
"""

import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
import logging
from datetime import datetime

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
    
    def create_dynamic_mapping(self, 
                              source_column: str, 
                              base_key_column: str, 
                              base_value_column: str,
                              additional_keys: List[str] = None) -> str:
        """
        Crear mapeo dinámico con soporte para columnas adicionales
        
        Args:
            source_column: Columna del archivo fuente para buscar
            base_key_column: Columna del archivo base para comparar
            base_value_column: Columna del archivo base para extraer valor
            additional_keys: Lista de columnas adicionales del archivo fuente para evitar ambigüedades
            
        Returns:
            ID único del mapeo creado
        """
        try:
            if self.base_df is None:
                raise ValueError("No se ha cargado un archivo base para crear el mapeo")
            
            # Validar que las columnas existen en el archivo base
            if base_key_column not in self.base_df.columns:
                raise ValueError(f"Columna clave no encontrada en archivo base: {base_key_column}")
            
            if base_value_column not in self.base_df.columns:
                raise ValueError(f"Columna valor no encontrada en archivo base: {base_value_column}")
            
            # Crear identificador único para este mapeo
            mapping_id = f"{source_column}_{base_key_column}_{base_value_column}"
            
            # Crear diccionario de mapeo
            mapping_dict = {}
            
            for _, row in self.base_df.iterrows():
                key = str(row[base_key_column]).strip()
                value = row[base_value_column]
                
                if pd.notna(key) and key != "":
                    # Si hay columnas adicionales, crear clave compuesta
                    if additional_keys:
                        # Buscar las columnas correspondientes en el archivo base
                        key_parts = [key]
                        
                        for additional_col in additional_keys:
                            # Buscar columna correspondiente en el archivo base
                            found_col = self._find_corresponding_base_column(additional_col)
                            if found_col and found_col in row.index:
                                key_parts.append(str(row[found_col]).strip())
                            # Si no encuentra la columna, NO agregar nada (omitir esa columna)
                        
                        # Crear clave compuesta solo con las columnas que existen
                        key = "|".join(key_parts)
                        
                        # Guardar las columnas adicionales que realmente se usaron
                        if not hasattr(self, '_used_additional_keys'):
                            self._used_additional_keys = {}
                        self._used_additional_keys[mapping_id] = [
                            col for col in additional_keys 
                            if self._find_corresponding_base_column(col) and 
                            self._find_corresponding_base_column(col) in self.base_df.columns
                        ]
                    
                    # Normalizar el valor según el tipo de dato
                    normalized_value = self._normalize_value(value, base_value_column)
                    mapping_dict[key] = normalized_value
            
            # Guardar mapeo completo
            self.mappings[mapping_id] = {
                'type': 'dynamic',
                'source_column': source_column,
                'base_key_column': base_key_column,
                'base_value_column': base_value_column,
                'mapping_dict': mapping_dict,
                'additional_keys': additional_keys or [],
                'total_entries': len(mapping_dict)
            }
            
            self.logger.info(f"Mapeo dinámico creado: {mapping_id} con {len(mapping_dict)} entradas")
            if additional_keys:
                self.logger.info(f"Columnas adicionales de referencia: {additional_keys}")
            
            return mapping_id
            
        except Exception as e:
            self.logger.error(f"Error creando mapeo dinámico: {e}")
            raise
    
    def _find_corresponding_base_column(self, source_column: str) -> str:
        """
        Buscar la columna correspondiente en el archivo base
        
        Args:
            source_column: Nombre de la columna del archivo fuente
            
        Returns:
            Nombre de la columna correspondiente en el archivo base
        """
        if self.base_df is None:
            return None
        
        # 1. Búsqueda exacta
        if source_column in self.base_df.columns:
            return source_column
        
        # 2. Búsqueda case-insensitive
        for col in self.base_df.columns:
            if col.lower() == source_column.lower():
                return col
        
        # 3. Búsqueda por similitud de nombres
        name_mappings = {
            'nombre programa': ['tema', 'programa', 'nombre'],
            'tema': ['nombre programa', 'programa', 'nombre'],
            'programa': ['tema', 'nombre programa', 'nombre'],
            'ciudad': ['dirección', 'ubicación', 'ciudad'],
            'dirección': ['ciudad', 'ubicación'],
            'fecha': ['fecha (dd/mm/aa)', 'fecha'],
            'fecha (dd/mm/aa)': ['fecha', 'fecha (dd/mm/aa)'],
            'módulo': ['módulo', 'modulo'],
            'cupos': ['cupos', 'capacidad'],
            'hora inicio': ['hora inicio (24h)', 'hora_inicio'],
            'hora final': ['hora final (24h)', 'hora_final']
        }
        
        # Buscar en el mapeo
        for key, alternatives in name_mappings.items():
            if source_column.lower() in key or key in source_column.lower():
                for alt in alternatives:
                    for col in self.base_df.columns:
                        if alt.lower() in col.lower():
                            return col
        
        # 4. Búsqueda por similitud de palabras
        source_words = set(source_column.lower().split())
        best_match = None
        best_similarity = 0
        
        for col in self.base_df.columns:
            col_words = set(col.lower().split())
            if source_words and col_words:
                similarity = len(source_words.intersection(col_words)) / len(source_words.union(col_words))
                if similarity > 0.3 and similarity > best_similarity:  # 30% de similitud
                    best_similarity = similarity
                    best_match = col
        
        return best_match
    
    def _normalize_value(self, value: Any, column_name: str) -> Any:
        """
        Normalizar valor según el tipo de columna esperado
        
        Args:
            value: Valor a normalizar
            column_name: Nombre de la columna para determinar el tipo
            
        Returns:
            Valor normalizado
        """
        try:
            # Si el valor es NaN, devolver None
            if pd.isna(value):
                return None
            
            # Detectar tipo de columna por nombre
            column_lower = column_name.lower()
            
            # Columnas numéricas
            if any(keyword in column_lower for keyword in ['id', 'codigo', 'numero', 'numero_', 'num_']):
                try:
                    return int(float(value))
                except (ValueError, TypeError):
                    return value
            
            # Columnas de fecha
            elif any(keyword in column_lower for keyword in ['fecha', 'date', 'fecha_']):
                if isinstance(value, str):
                    # Intentar parsear diferentes formatos de fecha
                    for fmt in ['%d/%m/%y', '%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y']:
                        try:
                            dt = datetime.strptime(value, fmt)
                            return dt.strftime('%d/%m/%y')
                        except ValueError:
                            continue
                return value
            
            # Para otros tipos, devolver el valor tal como está
            return value
            
        except Exception as e:
            self.logger.warning(f"Error normalizando valor {value} para columna {column_name}: {e}")
            return value
    
    def apply_dynamic_mapping(self, 
                             source_df: pd.DataFrame, 
                             mapping_id: str,
                             default_value: Any = None) -> List[Any]:
        """
        Aplicar mapeo dinámico a un DataFrame fuente
        
        Args:
            source_df: DataFrame fuente con los datos a mapear
            mapping_id: ID del mapeo a aplicar
            default_value: Valor por defecto si no se encuentra coincidencia
            
        Returns:
            Lista de valores mapeados
        """
        try:
            if mapping_id not in self.mappings:
                raise ValueError(f"Mapeo no encontrado: {mapping_id}")
            
            mapping_info = self.mappings[mapping_id]
            mapping_dict = mapping_info['mapping_dict']
            source_column = mapping_info['source_column']
            additional_keys = mapping_info.get('additional_keys', [])
            
            # Usar solo las columnas adicionales que realmente existen en el archivo base
            if hasattr(self, '_used_additional_keys') and mapping_id in self._used_additional_keys:
                additional_keys = self._used_additional_keys[mapping_id]
            
            # Validar que la columna fuente existe
            if source_column not in source_df.columns:
                raise ValueError(f"Columna fuente no encontrada: {source_column}")
            
            # Validar columnas adicionales
            missing_additional = [col for col in additional_keys if col not in source_df.columns]
            if missing_additional:
                self.logger.warning(f"Columnas adicionales no encontradas: {missing_additional}")
            
            mapped_values = []
            
            for _, row in source_df.iterrows():
                try:
                    # Obtener valor de la columna fuente
                    source_value = str(row[source_column]).strip()
                    
                    # Normalizar fechas si es necesario
                    if source_column.lower() in ['fecha', 'date', 'fecha (dd/mm/aa)']:
                        source_value = self._normalize_date_value(source_value)
                    
                    # Crear clave de búsqueda
                    if additional_keys:
                        # Clave compuesta con columnas adicionales
                        search_parts = [source_value]
                        
                        for additional_col in additional_keys:
                            if additional_col in row.index:
                                additional_value = str(row[additional_col]).strip()
                                search_parts.append(additional_value)
                            # Si no encuentra la columna, NO agregar nada (omitir esa columna)
                        
                        search_key = "|".join(search_parts)
                    else:
                        # Búsqueda simple
                        search_key = source_value
                    
                    # Buscar el valor en el mapeo
                    mapped_value = self._find_mapped_value(mapping_dict, search_key, default_value)
                    mapped_values.append(mapped_value)
                    
                except Exception as e:
                    self.logger.warning(f"Error procesando fila para mapeo {mapping_id}: {e}")
                    mapped_values.append(default_value)
            
            return mapped_values
            
        except Exception as e:
            self.logger.error(f"Error aplicando mapeo dinámico: {e}")
            return [default_value] * len(source_df)
    
    def _normalize_date_value(self, date_value: str) -> str:
        """
        Normalizar valor de fecha a formato dd/mm/yy
        
        Args:
            date_value: Valor de fecha como string
            
        Returns:
            Fecha normalizada en formato dd/mm/yy
        """
        try:
            if not date_value or date_value.strip() == "":
                return ""
            
            # Si ya está en formato dd/mm/yy, devolver tal como está
            if len(date_value.split('/')) == 3 and len(date_value.split('/')[2]) == 2:
                return date_value
            
            # Manejar formato datetime de Excel (YYYY-MM-DD HH:MM:SS)
            if ' ' in date_value and '-' in date_value:
                # Extraer solo la parte de la fecha
                date_part = date_value.split(' ')[0]
                try:
                    dt = datetime.strptime(date_part, '%Y-%m-%d')
                    return dt.strftime('%d/%m/%y')
                except ValueError:
                    pass
            
            # Intentar parsear diferentes formatos
            for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%Y/%m/%d', '%Y-%m-%d %H:%M:%S']:
                try:
                    dt = datetime.strptime(date_value, fmt)
                    return dt.strftime('%d/%m/%y')
                except ValueError:
                    continue
            
            # Si no se puede parsear, devolver el valor original
            return date_value
            
        except Exception as e:
            self.logger.warning(f"Error normalizando fecha {date_value}: {e}")
            return date_value
    
    def _find_mapped_value(self, mapping_dict: Dict, search_key: str, default_value: Any) -> Any:
        """
        Buscar valor en el diccionario de mapeo con diferentes estrategias
        
        Args:
            mapping_dict: Diccionario de mapeo
            search_key: Clave a buscar
            default_value: Valor por defecto
            
        Returns:
            Valor encontrado o valor por defecto
        """
        # 1. Búsqueda exacta
        if search_key in mapping_dict:
            return mapping_dict[search_key]
        
        # 2. Búsqueda case-insensitive
        for key, value in mapping_dict.items():
            if str(key).strip().lower() == search_key.lower():
                return value
        
        # 3. Búsqueda parcial (para casos donde hay espacios extra)
        search_key_clean = search_key.strip()
        for key, value in mapping_dict.items():
            if str(key).strip() == search_key_clean:
                return value
        
        # 4. Si no se encuentra, devolver valor por defecto
        return default_value
    
    def validate_mapping(self, mapping_id: str) -> Dict[str, Any]:
        """
        Validar un mapeo específico y devolver estadísticas
        
        Args:
            mapping_id: ID del mapeo a validar
            
        Returns:
            Diccionario con estadísticas del mapeo
        """
        if mapping_id not in self.mappings:
            return {"error": f"Mapeo no encontrado: {mapping_id}"}
        
        mapping_info = self.mappings[mapping_id]
        mapping_dict = mapping_info['mapping_dict']
        
        # Estadísticas básicas
        stats = {
            "total_entries": len(mapping_dict),
            "unique_keys": len(set(mapping_dict.keys())),
            "unique_values": len(set(mapping_dict.values())),
            "null_values": sum(1 for v in mapping_dict.values() if pd.isna(v) or v is None),
            "additional_keys": mapping_info.get('additional_keys', [])
        }
        
        # Análisis de tipos de valores
        value_types = {}
        for value in mapping_dict.values():
            if pd.isna(value) or value is None:
                continue
            value_type = type(value).__name__
            value_types[value_type] = value_types.get(value_type, 0) + 1
        
        stats["value_types"] = value_types
        
        return stats
    
    def get_mapping_info(self, mapping_name: str) -> Dict[str, Any]:
        """Obtener información de un mapeo"""
        if mapping_name in self.mappings:
            return self.mappings[mapping_name].copy()
        return {}
    
    def get_all_mappings(self) -> List[str]:
        """Obtener lista de todos los mapeos"""
        return list(self.mappings.keys())
    
    def get_config(self) -> Dict[str, Any]:
        """Obtener configuración actual de mapeos"""
        return {
            'mappings': self.mappings,
            'total_mappings': len(self.mappings)
        }
    
    # Métodos de compatibilidad para mantener la funcionalidad existente
    def add_simple_mapping(self, source_column: str, base_key_column: str, base_value_column: str) -> bool:
        """Método de compatibilidad - usar create_dynamic_mapping en su lugar"""
        try:
            mapping_id = self.create_dynamic_mapping(source_column, base_key_column, base_value_column)
            return bool(mapping_id)
        except Exception as e:
            self.logger.error(f"Error en add_simple_mapping: {e}")
            return False
    
    def create_mapping(self, base_df: pd.DataFrame, key_column: str, value_column: str, mapping_name: str) -> bool:
        """Método de compatibilidad - usar create_dynamic_mapping en su lugar"""
        try:
            self.set_base_dataframe(base_df)
            mapping_id = self.create_dynamic_mapping(key_column, key_column, value_column)
            return bool(mapping_id)
        except Exception as e:
            self.logger.error(f"Error en create_mapping: {e}")
            return False
    
    def apply_mapping(self, source_df: pd.DataFrame, source_column: str, mapping_name: str, default_value: Any = None) -> List[Any]:
        """Método de compatibilidad - usar apply_dynamic_mapping en su lugar"""
        try:
            return self.apply_dynamic_mapping(source_df, mapping_name, default_value)
        except Exception as e:
            self.logger.error(f"Error en apply_mapping: {e}")
            return [default_value] * len(source_df)
    
    def create_multi_column_mapping(self, base_df: pd.DataFrame, key_columns: List[str], value_columns: List[str], mapping_name: str, separator: str = "_") -> bool:
        """Método de compatibilidad - usar create_dynamic_mapping con additional_keys en su lugar"""
        try:
            self.set_base_dataframe(base_df)
            # Para mapeo multi-columna, usar la primera columna como principal y las demás como adicionales
            if key_columns:
                additional_keys = key_columns[1:] if len(key_columns) > 1 else []
                mapping_id = self.create_dynamic_mapping(key_columns[0], key_columns[0], value_columns[0], additional_keys)
                return bool(mapping_id)
            return False
        except Exception as e:
            self.logger.error(f"Error en create_multi_column_mapping: {e}")
            return False
    
    def apply_multi_column_mapping(self, source_df: pd.DataFrame, source_columns: List[str], mapping_name: str, target_column: str = None, default_value: Any = None) -> List[Any]:
        """Método de compatibilidad - usar apply_dynamic_mapping en su lugar"""
        try:
            return self.apply_dynamic_mapping(source_df, mapping_name, default_value)
        except Exception as e:
            self.logger.error(f"Error en apply_multi_column_mapping: {e}")
            return [default_value] * len(source_df)
    
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
    
    def get_mapping_statistics(self, mapping_name: str) -> Dict[str, Any]:
        """Obtener estadísticas de un mapeo (método de compatibilidad)"""
        return self.validate_mapping(mapping_name)