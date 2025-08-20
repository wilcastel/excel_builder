# -*- coding: utf-8 -*-
"""
Sistema de validaciones para datos y configuraciones
"""

import re
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from models.column_config import ColumnConfig, DataType
from .exceptions import ValidationError

class DataValidator:
    """Validador para datos de Excel y configuraciones"""
    
    @staticmethod
    def validate_dataframe(df: pd.DataFrame, min_rows: int = 1) -> List[str]:
        """Validar DataFrame básico"""
        errors = []
        
        if df is None:
            errors.append("DataFrame es None")
            return errors
        
        if df.empty:
            errors.append("DataFrame está vacío")
            return errors
        
        if len(df) < min_rows:
            errors.append(f"DataFrame debe tener al menos {min_rows} filas")
        
        # Verificar columnas duplicadas
        duplicate_cols = df.columns[df.columns.duplicated()].tolist()
        if duplicate_cols:
            errors.append(f"Columnas duplicadas encontradas: {duplicate_cols}")
        
        # Verificar columnas vacías
        empty_cols = [col for col in df.columns if df[col].isna().all()]
        if empty_cols:
            errors.append(f"Columnas completamente vacías: {empty_cols}")
        
        return errors
    
    @staticmethod
    def validate_column_data(df: pd.DataFrame, column: str, data_type: DataType) -> List[str]:
        """Validar datos de una columna específica"""
        errors = []
        
        if column not in df.columns:
            errors.append(f"Columna '{column}' no encontrada")
            return errors
        
        series = df[column].dropna()  # Ignorar valores nulos para validación
        
        if series.empty:
            return errors  # No hay datos para validar
        
        try:
            if data_type == DataType.NUMBER:
                # Intentar convertir a numérico
                pd.to_numeric(series, errors='raise')
            
            elif data_type == DataType.DATE:
                # Intentar convertir a fecha
                pd.to_datetime(series, errors='raise')
            
            elif data_type == DataType.DATETIME:
                # Intentar convertir a datetime
                pd.to_datetime(series, errors='raise')
            
            elif data_type == DataType.BOOLEAN:
                # Verificar valores booleanos
                valid_bool_values = {True, False, 'True', 'False', 'true', 'false', 
                                   '1', '0', 1, 0, 'Si', 'No', 'si', 'no'}
                invalid_values = set(series.astype(str)) - {str(v) for v in valid_bool_values}
                if invalid_values:
                    errors.append(f"Valores no booleanos en columna '{column}': {list(invalid_values)[:5]}")
            
            elif data_type == DataType.CURRENCY:
                # Validar formato de moneda
                for value in series.head(10):  # Verificar solo primeros 10
                    str_value = str(value)
                    if not re.match(r'^[\$]?[\d,]+\.?\d*$', str_value.replace(' ', '')):
                        errors.append(f"Formato de moneda inválido en columna '{column}': {value}")
                        break
            
            elif data_type == DataType.PERCENTAGE:
                # Validar formato de porcentaje
                for value in series.head(10):
                    str_value = str(value)
                    if not re.match(r'^\d+\.?\d*%?$', str_value.replace(' ', '')):
                        errors.append(f"Formato de porcentaje inválido en columna '{column}': {value}")
                        break
        
        except Exception as e:
            errors.append(f"Error validando columna '{column}' como {data_type.value}: {str(e)}")
        
        return errors
    
    @staticmethod
    def validate_numeric_range(df: pd.DataFrame, column: str, 
                             min_value: Optional[float] = None, 
                             max_value: Optional[float] = None) -> List[str]:
        """Validar rango numérico"""
        errors = []
        
        if column not in df.columns:
            return [f"Columna '{column}' no encontrada"]
        
        try:
            numeric_series = pd.to_numeric(df[column], errors='coerce')
            
            if min_value is not None:
                below_min = numeric_series < min_value
                if below_min.any():
                    count = below_min.sum()
                    errors.append(f"Columna '{column}': {count} valores por debajo del mínimo ({min_value})")
            
            if max_value is not None:
                above_max = numeric_series > max_value
                if above_max.any():
                    count = above_max.sum()
                    errors.append(f"Columna '{column}': {count} valores por encima del máximo ({max_value})")
        
        except Exception as e:
            errors.append(f"Error validando rango en columna '{column}': {str(e)}")
        
        return errors
    
    @staticmethod
    def validate_required_columns(df: pd.DataFrame, required_columns: List[str]) -> List[str]:
        """Validar que existan columnas requeridas"""
        errors = []
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            errors.append(f"Columnas requeridas faltantes: {missing_columns}")
        
        # Verificar que las columnas requeridas no estén vacías
        for col in required_columns:
            if col in df.columns and df[col].isna().all():
                errors.append(f"Columna requerida '{col}' está completamente vacía")
        
        return errors

class FileValidator:
    """Validador para archivos"""
    
    @staticmethod
    def validate_file_path(file_path: str) -> List[str]:
        """Validar ruta de archivo"""
        errors = []
        
        if not file_path:
            errors.append("Ruta de archivo vacía")
            return errors
        
        path = Path(file_path)
        
        if not path.exists():
            errors.append(f"Archivo no existe: {file_path}")
        
        if not path.is_file():
            errors.append(f"La ruta no es un archivo: {file_path}")
        
        return errors
    
    @staticmethod
    def validate_excel_file(file_path: str) -> List[str]:
        """Validar archivo Excel específicamente"""
        errors = FileValidator.validate_file_path(file_path)
        
        if errors:  # Si ya hay errores básicos, no continuar
            return errors
        
        path = Path(file_path)
        
        # Verificar extensión
        valid_extensions = ['.xlsx', '.xls']
        if path.suffix.lower() not in valid_extensions:
            errors.append(f"Extensión de archivo no válida. Esperado: {valid_extensions}")
        
        # Verificar tamaño
        try:
            file_size_mb = path.stat().st_size / (1024 * 1024)
            if file_size_mb > 100:  # 100 MB límite
                errors.append(f"Archivo muy grande: {file_size_mb:.1f} MB (máximo: 100 MB)")
        except Exception as e:
            errors.append(f"Error verificando tamaño de archivo: {str(e)}")
        
        # Intentar abrir el archivo
        try:
            pd.read_excel(file_path, nrows=1)
        except Exception as e:
            errors.append(f"Error leyendo archivo Excel: {str(e)}")
        
        return errors
    
    @staticmethod
    def validate_output_path(output_path: str) -> List[str]:
        """Validar ruta de salida"""
        errors = []
        
        if not output_path:
            errors.append("Ruta de salida vacía")
            return errors
        
        path = Path(output_path)
        
        # Verificar directorio padre
        parent_dir = path.parent
        if not parent_dir.exists():
            try:
                parent_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                errors.append(f"No se puede crear directorio: {str(e)}")
        
        # Verificar permisos de escritura
        try:
            test_file = parent_dir / "test_write_permission.tmp"
            test_file.touch()
            test_file.unlink()
        except Exception as e:
            errors.append(f"Sin permisos de escritura en directorio: {str(e)}")
        
        return errors

class ConfigValidator:
    """Validador para configuraciones"""
    
    @staticmethod
    def validate_column_config(config: ColumnConfig) -> List[str]:
        """Validar configuración de columna"""
        errors = []
        
        # Validar nombre
        if not config.name or not config.name.strip():
            errors.append("Nombre de columna requerido")
        
        if not config.display_name or not config.display_name.strip():
            errors.append("Nombre para mostrar requerido")
        
        # Validar posición
        if config.position < 0:
            errors.append("Posición debe ser mayor o igual a 0")
        
        # Validar ancho
        if config.width is not None and config.width <= 0:
            errors.append("Ancho de columna debe ser mayor a 0")
        
        # Validar configuración numérica
        if config.is_numeric_generator:
            if config.numeric_start < 0:
                errors.append("Número inicial debe ser mayor o igual a 0")
        
        # Validar mapeo
        if config.mapping_source:
            if not config.mapping_key_column:
                errors.append("Columna clave requerida para mapeo")
            if not config.mapping_value_column:
                errors.append("Columna valor requerida para mapeo")
        
        return errors
    
    @staticmethod
    def validate_column_configs(configs: List[ColumnConfig]) -> List[str]:
        """Validar lista de configuraciones de columnas"""
        errors = []
        
        if not configs:
            errors.append("Al menos una configuración de columna es requerida")
            return errors
        
        # Verificar nombres únicos
        names = [config.name for config in configs]
        duplicate_names = [name for name in names if names.count(name) > 1]
        if duplicate_names:
            errors.append(f"Nombres de columna duplicados: {list(set(duplicate_names))}")
        
        # Verificar posiciones únicas
        positions = [config.position for config in configs]
        duplicate_positions = [pos for pos in positions if positions.count(pos) > 1]
        if duplicate_positions:
            errors.append(f"Posiciones duplicadas: {list(set(duplicate_positions))}")
        
        # Validar cada configuración individual
        for i, config in enumerate(configs):
            config_errors = ConfigValidator.validate_column_config(config)
            for error in config_errors:
                errors.append(f"Columna {i+1} ({config.name}): {error}")
        
        return errors
    
    @staticmethod
    def validate_export_config(config: Dict[str, Any]) -> List[str]:
        """Validar configuración de exportación"""
        errors = []
        
        # Validar archivo de salida
        if not config.get('output_file'):
            errors.append("Archivo de salida requerido")
        
        # Validar formato
        valid_formats = ['xlsx', 'xls', 'csv']
        if config.get('format') not in valid_formats:
            errors.append(f"Formato inválido. Válidos: {valid_formats}")
        
        # Validar nombre de hoja
        if not config.get('sheet_name'):
            errors.append("Nombre de hoja requerido")
        
        # Validar máximo de filas
        max_rows = config.get('max_rows_per_sheet', 0)
        if not isinstance(max_rows, int) or max_rows <= 0:
            errors.append("Máximo de filas debe ser un entero positivo")
        
        return errors