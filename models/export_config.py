# -*- coding: utf-8 -*-
"""
Modelo de configuración de exportación
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from pathlib import Path
from enum import Enum

class ExportFormat(Enum):
    """Formatos de exportación soportados"""
    XLSX = "xlsx"
    CSV = "csv"
    JSON = "json"
    TXT = "txt"

class CompressionType(Enum):
    """Tipos de compresión"""
    NONE = "none"
    ZIP = "zip"
    GZIP = "gzip"

@dataclass
class ExportOptions:
    """Opciones específicas de exportación"""
    include_headers: bool = True
    auto_adjust_columns: bool = True
    preserve_formatting: bool = True
    include_formulas: bool = False
    include_charts: bool = False
    include_images: bool = False
    freeze_header_row: bool = False
    add_filters: bool = False
    
    # Opciones CSV
    csv_delimiter: str = ","
    csv_encoding: str = "utf-8"
    csv_quote_char: str = '"'
    csv_escape_char: str = "\\"
    
    # Opciones JSON
    json_indent: int = 2
    json_ensure_ascii: bool = False
    
    # Opciones de formato
    date_format: str = "%Y-%m-%d"
    datetime_format: str = "%Y-%m-%d %H:%M:%S"
    number_format: str = "0.00"

@dataclass
class ExportConfig:
    """Configuración completa de exportación"""
    output_path: Path
    file_name: str
    format: ExportFormat
    sheet_name: str = "Datos"
    options: ExportOptions = field(default_factory=ExportOptions)
    
    # Configuración de backup
    create_backup: bool = True
    backup_directory: Optional[Path] = None
    max_backups: int = 5
    
    # Configuración de compresión
    compression: CompressionType = CompressionType.NONE
    compression_level: int = 6
    
    # Configuración de división
    split_large_files: bool = False
    max_rows_per_file: int = 100000
    
    # Metadatos
    author: str = "Excel Builder Pro"
    title: str = ""
    subject: str = ""
    description: str = ""
    keywords: List[str] = field(default_factory=list)
    
    # Configuración avanzada
    custom_properties: Dict[str, Any] = field(default_factory=dict)
    template_path: Optional[Path] = None
    
    def __post_init__(self):
        # Asegurar que output_path es Path
        if isinstance(self.output_path, str):
            self.output_path = Path(self.output_path)
        
        # Configurar directorio de backup por defecto
        if self.create_backup and self.backup_directory is None:
            self.backup_directory = self.output_path.parent / "backups"
        
        # Asegurar extensión correcta
        if not self.file_name.endswith(f".{self.format.value}"):
            self.file_name = f"{self.file_name}.{self.format.value}"
    
    @property
    def full_path(self) -> Path:
        """Ruta completa del archivo de salida"""
        return self.output_path / self.file_name
    
    @property
    def backup_path(self) -> Optional[Path]:
        """Ruta del directorio de backup"""
        return self.backup_directory if self.create_backup else None
    
    def get_backup_filename(self, timestamp: str = None) -> str:
        """Generar nombre de archivo de backup"""
        if not timestamp:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        name_without_ext = self.file_name.rsplit('.', 1)[0]
        ext = self.format.value
        return f"{name_without_ext}_backup_{timestamp}.{ext}"
    
    def validate(self) -> List[str]:
        """Validar configuración"""
        errors = []
        
        # Validar ruta de salida
        if not self.output_path.parent.exists():
            errors.append(f"El directorio padre no existe: {self.output_path.parent}")
        
        # Validar nombre de archivo
        if not self.file_name or self.file_name.strip() == "":
            errors.append("El nombre del archivo no puede estar vacío")
        
        # Validar caracteres inválidos en nombre
        invalid_chars = '<>:"/\\|?*'
        if any(char in self.file_name for char in invalid_chars):
            errors.append(f"El nombre del archivo contiene caracteres inválidos: {invalid_chars}")
        
        # Validar opciones CSV
        if self.format == ExportFormat.CSV:
            if len(self.options.csv_delimiter) != 1:
                errors.append("El delimitador CSV debe ser un solo carácter")
        
        # Validar división de archivos
        if self.split_large_files and self.max_rows_per_file <= 0:
            errors.append("El número máximo de filas por archivo debe ser mayor a 0")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario"""
        return {
            'output_path': str(self.output_path),
            'file_name': self.file_name,
            'format': self.format.value,
            'sheet_name': self.sheet_name,
            'create_backup': self.create_backup,
            'backup_directory': str(self.backup_directory) if self.backup_directory else None,
            'compression': self.compression.value,
            'split_large_files': self.split_large_files,
            'max_rows_per_file': self.max_rows_per_file,
            'author': self.author,
            'title': self.title,
            'subject': self.subject,
            'description': self.description,
            'keywords': self.keywords,
            'options': {
                'include_headers': self.options.include_headers,
                'auto_adjust_columns': self.options.auto_adjust_columns,
                'preserve_formatting': self.options.preserve_formatting,
                'csv_delimiter': self.options.csv_delimiter,
                'csv_encoding': self.options.csv_encoding,
                'json_indent': self.options.json_indent,
                'date_format': self.options.date_format,
                'datetime_format': self.options.datetime_format
            }
        }