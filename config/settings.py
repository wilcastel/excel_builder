# -*- coding: utf-8 -*-
"""
Configuración global de la aplicación
"""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AppSettings:
    """Configuración principal de la aplicación"""
    
    # Información de la aplicación
    app_name: str = "Excel Builder Pro"
    app_version: str = "1.0.0"
    app_author: str = "Excel Builder Pro Team"
    
    # Configuración de ventana
    window_width: int = 1400
    window_height: int = 1000
    window_min_width: int = 1200
    window_min_height: int = 800
    
    # Configuración de archivos
    max_file_size_mb: int = 100
    supported_formats: tuple = (".xlsx", ".xls")
    default_export_format: str = ".xlsx"
    
    # Configuración de interfaz
    theme: str = "default"
    font_family: str = "Arial"
    font_size: int = 10
    
    # Configuración de exportación
    default_export_dir: str = "exportados"
    auto_backup: bool = True
    max_preview_rows: int = 100
    
    # Configuración de logging
    log_level: str = "INFO"
    log_file: str = "excel_builder.log"
    
    def __post_init__(self):
        """Inicialización posterior"""
        # Crear directorio de exportación si no existe
        export_path = Path(self.default_export_dir)
        export_path.mkdir(exist_ok=True)
        
        # Crear directorio de logs si no existe
        log_path = Path("logs")
        log_path.mkdir(exist_ok=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir configuración a diccionario"""
        return {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "window_width": self.window_width,
            "window_height": self.window_height,
            "theme": self.theme,
            "font_family": self.font_family,
            "font_size": self.font_size
        }