# -*- coding: utf-8 -*-
"""
Utilidades y funciones auxiliares
"""

import re
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import logging
import os
from config.settings import AppSettings

def setup_logging(settings: AppSettings) -> None:
    """
    Configurar el sistema de logging de la aplicación - Versión Optimizada
    
    Args:
        settings: Configuración de la aplicación
    """
    # Crear directorio de logs si no existe
    log_dir = Path(settings.log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configurar formato de logging optimizado
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    date_format = '%H:%M:%S'
    
    # Configurar logging con optimizaciones para rendimiento
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=[
            # FileHandler con buffer para reducir escrituras
            logging.FileHandler(settings.log_file, encoding='utf-8', mode='a'),
            # StreamHandler solo para errores críticos en consola
            logging.StreamHandler()
        ]
    )
    
    # Configurar logger específico para la aplicación
    logger = logging.getLogger('excel_builder_pro')
    
    # Configurar nivel de logging más restrictivo para módulos específicos
    # Reducir logging de debug en módulos de procesamiento intensivo
    logging.getLogger('core.export_manager').setLevel(logging.WARNING)
    logging.getLogger('core.numeric_generator').setLevel(logging.WARNING)
    logging.getLogger('core.mapping_manager').setLevel(logging.WARNING)
    
    # Configurar logging de consola solo para errores
    console_handler = logging.getLogger().handlers[1]  # StreamHandler
    console_handler.setLevel(logging.ERROR)
    
    logger.info(f"Sistema de logging optimizado configurado - Nivel: {settings.log_level}")
    logger.info(f"Archivo de log: {settings.log_file}")


class ExcelHelper:
    """Utilidades para trabajar con archivos Excel"""
    
    @staticmethod
    def get_sheet_names(file_path: str) -> List[str]:
        """Obtener nombres de hojas de un archivo Excel"""
        try:
            excel_file = pd.ExcelFile(file_path)
            return excel_file.sheet_names
        except Exception as e:
            logging.error(f"Error obteniendo hojas de {file_path}: {e}")
            return []
    
    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Any]:
        """Obtener información detallada de un archivo Excel"""
        try:
            path = Path(file_path)
            excel_file = pd.ExcelFile(file_path)
            
            info = {
                'file_name': path.name,
                'file_size': path.stat().st_size,
                'file_size_mb': round(path.stat().st_size / (1024 * 1024), 2),
                'modified_date': datetime.fromtimestamp(path.stat().st_mtime),
                'sheet_count': len(excel_file.sheet_names),
                'sheet_names': excel_file.sheet_names,
                'sheets_info': {}
            }
            
            # Información de cada hoja
            for sheet_name in excel_file.sheet_names:
                try:
                    df = pd.read_excel(file_path, sheet_name=sheet_name, nrows=1)
                    full_df = pd.read_excel(file_path, sheet_name=sheet_name)
                    
                    info['sheets_info'][sheet_name] = {
                        'rows': len(full_df),
                        'columns': len(full_df.columns),
                        'column_names': full_df.columns.tolist()
                    }
                except Exception as e:
                    info['sheets_info'][sheet_name] = {
                        'error': str(e)
                    }
            
            return info
            
        except Exception as e:
            logging.error(f"Error obteniendo información de {file_path}: {e}")
            return {}
    
    @staticmethod
    def detect_data_types(df: pd.DataFrame) -> Dict[str, str]:
        """Detectar tipos de datos automáticamente"""
        type_mapping = {}
        
        for column in df.columns:
            series = df[column].dropna()
            
            if series.empty:
                type_mapping[column] = 'text'
                continue
            
            # Intentar detectar tipo
            if pd.api.types.is_numeric_dtype(series):
                type_mapping[column] = 'number'
            elif pd.api.types.is_datetime64_any_dtype(series):
                type_mapping[column] = 'datetime'
            else:
                # Verificar si es fecha en formato string
                try:
                    pd.to_datetime(series.head(10), errors='raise')
                    type_mapping[column] = 'date'
                except:
                    # Verificar si es booleano
                    unique_values = set(series.astype(str).str.lower())
                    bool_values = {'true', 'false', '1', '0', 'si', 'no', 'yes', 'no'}
                    if unique_values.issubset(bool_values):
                        type_mapping[column] = 'boolean'
                    else:
                        type_mapping[column] = 'text'
        
        return type_mapping
    
    @staticmethod
    def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
        """Limpiar nombres de columnas"""
        df_copy = df.copy()
        
        # Limpiar nombres
        new_columns = []
        for col in df_copy.columns:
            # Convertir a string y limpiar
            clean_name = str(col).strip()
            # Remover caracteres especiales
            clean_name = re.sub(r'[^\w\s-]', '', clean_name)
            # Reemplazar espacios con guiones bajos
            clean_name = re.sub(r'\s+', '_', clean_name)
            # Convertir a minúsculas
            clean_name = clean_name.lower()
            
            new_columns.append(clean_name)
        
        df_copy.columns = new_columns
        return df_copy
    
    @staticmethod
    def preview_data(df: pd.DataFrame, max_rows: int = 100) -> Dict[str, Any]:
        """Crear vista previa de datos"""
        preview_df = df.head(max_rows)
        
        return {
            'data': preview_df,
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'preview_rows': len(preview_df),
            'column_info': {
                col: {
                    'dtype': str(df[col].dtype),
                    'null_count': df[col].isnull().sum(),
                    'unique_count': df[col].nunique()
                }
                for col in df.columns
            }
        }

class FileHelper:
    """Utilidades para manejo de archivos"""
    
    @staticmethod
    def ensure_directory(path: Union[str, Path]) -> bool:
        """Asegurar que un directorio existe"""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logging.error(f"Error creando directorio {path}: {e}")
            return False
    
    @staticmethod
    def get_safe_filename(filename: str) -> str:
        """Obtener nombre de archivo seguro"""
        # Remover caracteres no válidos
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Limitar longitud
        if len(safe_name) > 200:
            name, ext = Path(safe_name).stem, Path(safe_name).suffix
            safe_name = name[:200-len(ext)] + ext
        
        return safe_name
    
    @staticmethod
    def backup_file(file_path: str, backup_dir: str = "backups") -> Optional[str]:
        """Crear copia de seguridad de un archivo"""
        try:
            source_path = Path(file_path)
            if not source_path.exists():
                return None
            
            # Crear directorio de backup
            backup_path = Path(backup_dir)
            backup_path.mkdir(exist_ok=True)
            
            # Generar nombre de backup con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{source_path.stem}_backup_{timestamp}{source_path.suffix}"
            backup_file_path = backup_path / backup_name
            
            # Copiar archivo
            import shutil
            shutil.copy2(source_path, backup_file_path)
            
            return str(backup_file_path)
            
        except Exception as e:
            logging.error(f"Error creando backup de {file_path}: {e}")
            return None
    
    @staticmethod
    def get_unique_filename(file_path: str) -> str:
        """Obtener nombre de archivo único si ya existe"""
        path = Path(file_path)
        
        if not path.exists():
            return file_path
        
        counter = 1
        while True:
            new_name = f"{path.stem}_{counter}{path.suffix}"
            new_path = path.parent / new_name
            
            if not new_path.exists():
                return str(new_path)
            
            counter += 1
            
            # Evitar bucle infinito
            if counter > 1000:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_name = f"{path.stem}_{timestamp}{path.suffix}"
                return str(path.parent / new_name)

class StringHelper:
    """Utilidades para manejo de strings"""
    
    @staticmethod
    def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
        """Truncar string con sufijo"""
        if len(text) <= max_length:
            return text
        
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Formatear tamaño de archivo"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        
        return f"{s} {size_names[i]}"
    
    @staticmethod
    def format_number(number: Union[int, float], decimals: int = 2) -> str:
        """Formatear número con separadores de miles"""
        if isinstance(number, int):
            return f"{number:,}"
        else:
            return f"{number:,.{decimals}f}"
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Limpiar texto removiendo caracteres especiales"""
        if not isinstance(text, str):
            text = str(text)
        
        # Remover caracteres de control
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        # Normalizar espacios
        text = re.sub(r'\s+', ' ', text)
        # Limpiar inicio y fin
        text = text.strip()
        
        return text