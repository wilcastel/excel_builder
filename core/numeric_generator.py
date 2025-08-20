# -*- coding: utf-8 -*-
"""
Generador numérico dinámico - Versión Optimizada
"""

import pandas as pd
from typing import List, Dict, Any, Optional
import logging
from collections import defaultdict

class NumericGenerator:
    """Generador de números secuenciales con agrupación dinámica - Versión Optimizada"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.counters: Dict[str, int] = defaultdict(int)
        self.group_mappings: Dict[str, Dict[str, int]] = {}
        
        # Cache para optimización
        self._sequence_cache = {}
        self._group_cache = {}
        
        # Configuración por defecto
        self.config = {
            'type': 'none',
            'start_number': 1,
            'increment': 1,
            'padding': 0,
            'prefix': '',
            'suffix': '',
            'grouping_columns': [],
            'academic_year': '',
            'matricula_type': ''
        }
    
    def set_config(self, config: Dict[str, Any]):
        """Establecer configuración del generador"""
        self.config.update(config)
        # Limpiar cache cuando cambia la configuración
        self._sequence_cache.clear()
        self._group_cache.clear()
    
    def get_config(self) -> Dict[str, Any]:
        """Obtener configuración actual del generador"""
        return self.config.copy()
    
    def generate_sequence(self, 
                         df: pd.DataFrame,
                         grouping_columns: List[str],
                         start_number: int = 1,
                         prefix: str = "",
                         suffix: str = "",
                         padding: int = 0) -> List[str]:
        """Generar secuencia numérica con agrupación - Versión Optimizada"""
        try:
            # Usar cache si es posible
            cache_key = f"{len(df)}_{start_number}_{prefix}_{suffix}_{padding}_{'_'.join(grouping_columns)}"
            if cache_key in self._sequence_cache:
                return self._sequence_cache[cache_key]
            
            if not grouping_columns:
                # Sin agrupación, secuencia simple
                result = self._generate_simple_sequence(len(df), start_number, prefix, suffix, padding)
            else:
                # Con agrupación
                result = self._generate_grouped_sequence(df, grouping_columns, start_number, prefix, suffix, padding)
            
            # Guardar en cache
            self._sequence_cache[cache_key] = result
            return result
            
        except Exception as e:
            self.logger.error(f"Error generando secuencia: {e}")
            return []
    
    def _generate_simple_sequence(self, 
                                count: int, 
                                start_number: int,
                                prefix: str,
                                suffix: str,
                                padding: int) -> List[str]:
        """Generar secuencia simple sin agrupación - Versión Optimizada"""
        sequence = []
        
        # Optimización: usar list comprehension en lugar de bucle
        if padding > 0:
            sequence = [f"{prefix}{str(start_number + i).zfill(padding)}{suffix}" for i in range(count)]
        else:
            sequence = [f"{prefix}{start_number + i}{suffix}" for i in range(count)]
        
        return sequence
    
    def _generate_grouped_sequence(self,
                                 df: pd.DataFrame,
                                 grouping_columns: List[str],
                                 start_number: int,
                                 prefix: str,
                                 suffix: str,
                                 padding: int) -> List[str]:
        """Generar secuencia con agrupación por columnas - Versión Optimizada"""
        sequence = []
        group_counters = defaultdict(lambda: start_number)
        
        # Validar que las columnas existen
        missing_columns = [col for col in grouping_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Columnas no encontradas: {missing_columns}")
        
        # Optimización: procesar en lotes
        batch_size = 1000
        total_rows = len(df)
        
        for batch_start in range(0, total_rows, batch_size):
            batch_end = min(batch_start + batch_size, total_rows)
            batch_df = df.iloc[batch_start:batch_end]
            
            for _, row in batch_df.iterrows():
                # Crear clave de grupo
                group_key = "_".join([str(row[col]) for col in grouping_columns])
                
                # Obtener número para este grupo
                number = group_counters[group_key]
                group_counters[group_key] += 1
                
                # Formatear número
                if padding > 0:
                    formatted_number = str(number).zfill(padding)
                else:
                    formatted_number = str(number)
                
                sequence.append(f"{prefix}{formatted_number}{suffix}")
        
        # Guardar mapeo de grupos para referencia
        self.group_mappings["_".join(grouping_columns)] = dict(group_counters)
        
        return sequence
    
    def generate_matricula_style(self,
                                df: pd.DataFrame,
                                year_column: Optional[str] = None,
                                city_column: Optional[str] = None,
                                theme_column: Optional[str] = None,
                                module_column: Optional[str] = None,
                                start_number: int = 1,
                                year_digits: int = 2) -> List[str]:
        """Generar matrículas estilo específico (AACC-TTMM-NNNN) - Versión Optimizada"""
        try:
            matriculas = []
            group_counters = defaultdict(lambda: start_number)
            
            # Optimización: procesar en lotes
            batch_size = 1000
            total_rows = len(df)
            
            for batch_start in range(0, total_rows, batch_size):
                batch_end = min(batch_start + batch_size, total_rows)
                batch_df = df.iloc[batch_start:batch_end]
                
                for _, row in batch_df.iterrows():
                    # Extraer componentes
                    year_part = ""
                    if year_column and year_column in df.columns:
                        year_value = str(row[year_column])
                        if len(year_value) >= 4:
                            year_part = year_value[-year_digits:]
                        else:
                            year_part = year_value.zfill(year_digits)
                    
                    city_part = ""
                    if city_column and city_column in df.columns:
                        city_value = str(row[city_column])[:2].upper()
                        city_part = city_value.ljust(2, '0')
                    
                    theme_part = ""
                    if theme_column and theme_column in df.columns:
                        theme_value = str(row[theme_column])[:2].upper()
                        theme_part = theme_value.ljust(2, '0')
                    
                    module_part = ""
                    if module_column and module_column in df.columns:
                        module_value = str(row[module_column])[:2].upper()
                        module_part = module_value.ljust(2, '0')
                    
                    # Crear clave de grupo para el contador
                    group_key = f"{year_part}_{city_part}_{theme_part}_{module_part}"
                    
                    # Obtener número secuencial
                    number = group_counters[group_key]
                    group_counters[group_key] += 1
                    
                    # Formatear matrícula
                    number_part = str(number).zfill(4)
                    
                    # Construir matrícula final
                    parts = []
                    if year_part or city_part:
                        parts.append(f"{year_part}{city_part}")
                    if theme_part or module_part:
                        parts.append(f"{theme_part}{module_part}")
                    parts.append(number_part)
                    
                    matricula = "-".join(parts)
                    matriculas.append(matricula)
            
            return matriculas
            
        except Exception as e:
            self.logger.error(f"Error generando matrículas: {e}")
            return []
    
    def get_group_statistics(self, group_key: str) -> Dict[str, Any]:
        """Obtener estadísticas de un grupo"""
        if group_key in self.group_mappings:
            mapping = self.group_mappings[group_key]
            return {
                'total_groups': len(mapping),
                'max_count': max(mapping.values()) if mapping else 0,
                'min_count': min(mapping.values()) if mapping else 0,
                'groups': mapping
            }
        return {}
    
    def reset_counters(self):
        """Reiniciar todos los contadores - Versión Optimizada"""
        self.counters.clear()
        self.group_mappings.clear()
        self._sequence_cache.clear()
        self._group_cache.clear()
    
    def validate_grouping_columns(self, df: pd.DataFrame, columns: List[str]) -> List[str]:
        """Validar columnas de agrupación - Versión Optimizada"""
        errors = []
        
        if not columns:
            return errors
        
        missing_columns = [col for col in columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Columnas no encontradas: {missing_columns}")
        
        # Verificar que las columnas tienen datos
        for col in columns:
            if col in df.columns and df[col].isna().all():
                errors.append(f"La columna '{col}' está completamente vacía")
        
        return errors
    
    def generate_simple_sequence(self, count: int, start: int = None, increment: int = None, 
                               padding: int = None, prefix: str = None, suffix: str = None) -> List[str]:
        """Generar secuencia simple usando configuración - Versión Optimizada"""
        start = start if start is not None else self.config.get('start_number', 1)
        increment = increment if increment is not None else self.config.get('increment', 1)
        padding = padding if padding is not None else self.config.get('padding', 0)
        prefix = prefix if prefix is not None else self.config.get('prefix', '')
        suffix = suffix if suffix is not None else self.config.get('suffix', '')
        
        return self._generate_simple_sequence(count, start, prefix, suffix, padding)
    
    def generate_matricula_sequence(self, count: int, academic_year: str = None, 
                                  matricula_type: str = None, start_number: int = None) -> List[str]:
        """Generar secuencia de matrículas usando configuración - Versión Optimizada"""
        academic_year = academic_year or self.config.get('academic_year', '')
        matricula_type = matricula_type or self.config.get('matricula_type', '')
        start_number = start_number if start_number is not None else self.config.get('start_number', 1)
        
        # Generar matrículas básicas usando list comprehension para optimización
        matriculas = [f"{academic_year}-{matricula_type}-{str(start_number + i).zfill(4)}" 
                     for i in range(count)]
        
        return matriculas