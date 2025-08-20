# -*- coding: utf-8 -*-
"""
Gestor de archivos Excel
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Dict, List, Any
import logging
from config.settings import AppSettings

class FileManager:
    """Gestor para cargar y analizar archivos Excel"""
    
    def __init__(self, settings: AppSettings):
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        self.source_file: Optional[Path] = None
        self.base_file: Optional[Path] = None
        self.source_df: Optional[pd.DataFrame] = None
        self.base_df: Optional[pd.DataFrame] = None
        
    def load_source_file(self, file_path: str) -> Dict[str, Any]:
        """Cargar archivo Excel fuente"""
        try:
            path = Path(file_path)
            
            # Validaciones
            if not path.exists():
                raise FileNotFoundError(f"El archivo no existe: {file_path}")
                
            if path.suffix.lower() not in self.settings.supported_formats:
                raise ValueError(f"Formato no soportado: {path.suffix}")
                
            if path.stat().st_size > self.settings.max_file_size_mb * 1024 * 1024:
                raise ValueError(f"Archivo muy grande (máximo {self.settings.max_file_size_mb}MB)")
            
            # Cargar archivo
            self.source_df = pd.read_excel(file_path)
            self.source_file = path
            
            self.logger.info(f"Archivo fuente cargado: {file_path}")
            self.logger.info(f"Dimensiones: {self.source_df.shape}")
            
            # Retornar información del archivo
            return self.get_source_info()
            
        except Exception as e:
            self.logger.error(f"Error cargando archivo fuente: {e}")
            raise e  # Re-lanzar la excepción para que sea manejada por el UI
    
    def load_base_file(self, file_path: str) -> Dict[str, Any]:
        """Cargar archivo Excel base para mapeo"""
        try:
            path = Path(file_path)
            
            # Validaciones similares
            if not path.exists():
                raise FileNotFoundError(f"El archivo no existe: {file_path}")
                
            if path.suffix.lower() not in self.settings.supported_formats:
                raise ValueError(f"Formato no soportado: {path.suffix}")
            
            # Cargar archivo
            self.base_df = pd.read_excel(file_path)
            self.base_file = path
            
            self.logger.info(f"Archivo base cargado: {file_path}")
            
            # Retornar información del archivo
            return self.get_base_info()
            
        except Exception as e:
            self.logger.error(f"Error cargando archivo base: {e}")
            raise e
            self.logger.info(f"Dimensiones: {self.base_df.shape}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error cargando archivo base: {e}")
            return False
    
    def get_source_columns(self) -> List[str]:
        """Obtener lista de columnas del archivo fuente"""
        if self.source_df is not None:
            return list(self.source_df.columns)
        return []
    
    def get_base_columns(self) -> List[str]:
        """Obtener lista de columnas del archivo base"""
        if self.base_df is not None:
            return list(self.base_df.columns)
        return []
    
    def get_source_preview(self, max_rows: int = None) -> Optional[pd.DataFrame]:
        """Obtener vista previa del archivo fuente"""
        if self.source_df is not None:
            rows = max_rows or self.settings.max_preview_rows
            return self.source_df.head(rows)
        return None
    
    def get_base_preview(self, max_rows: int = None) -> Optional[pd.DataFrame]:
        """Obtener vista previa del archivo base"""
        if self.base_df is not None:
            rows = max_rows or self.settings.max_preview_rows
            return self.base_df.head(rows)
        return None
    
    def get_source_info(self) -> Dict[str, Any]:
        """Obtener información del archivo fuente"""
        if self.source_df is not None:
            file_size = self.source_file.stat().st_size
            file_size_mb = file_size / (1024 * 1024)
            
            return {
                'file_path': str(self.source_file),
                'file_name': self.source_file.name,
                'file_size': f"{file_size_mb:.2f} MB",
                'sheets': ['Hoja1'],  # Por defecto, pandas lee la primera hoja
                'active_sheet': 'Hoja1',
                'rows': len(self.source_df),
                'columns_count': len(self.source_df.columns),
                'columns': list(self.source_df.columns),
                'column_names': list(self.source_df.columns),
                'data_types': self.source_df.dtypes.to_dict(),
                'memory_usage': f"{self.source_df.memory_usage(deep=True).sum() / (1024 * 1024):.2f} MB"
            }
        return {}
    
    def get_base_info(self) -> Dict[str, Any]:
        """Obtener información del archivo base"""
        if self.base_df is not None:
            file_size = self.base_file.stat().st_size
            file_size_mb = file_size / (1024 * 1024)
            
            return {
                'file_path': str(self.base_file),
                'file_name': self.base_file.name,
                'file_size': f"{file_size_mb:.2f} MB",
                'sheets': ['Hoja1'],  # Por defecto, pandas lee la primera hoja
                'active_sheet': 'Hoja1',
                'rows': len(self.base_df),
                'columns_count': len(self.base_df.columns),
                'columns': list(self.base_df.columns),
                'column_names': list(self.base_df.columns),
                'data_types': self.base_df.dtypes.to_dict(),
                'memory_usage': f"{self.base_df.memory_usage(deep=True).sum() / (1024 * 1024):.2f} MB"
            }
        return {}
    
    def validate_files(self) -> List[str]:
        """Validar archivos cargados"""
        errors = []
        
        if self.source_df is None:
            errors.append("No se ha cargado un archivo fuente")
        elif self.source_df.empty:
            errors.append("El archivo fuente está vacío")
            
        return errors
    
    def clear_files(self):
        """Limpiar archivos cargados"""
        self.source_file = None
        self.base_file = None
        self.source_df = None
        self.base_df = None
        self.logger.info("Archivos limpiados")
    
    def get_source_data(self) -> Optional[pd.DataFrame]:
        """Obtener datos del archivo fuente"""
        return self.source_df
    
    def get_base_data(self) -> Optional[pd.DataFrame]:
        """Obtener datos del archivo base"""
        return self.base_df