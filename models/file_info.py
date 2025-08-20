# -*- coding: utf-8 -*-
"""
Modelo de información de archivos Excel
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from pathlib import Path
import datetime

@dataclass
class SheetInfo:
    """Información de una hoja de Excel"""
    name: str
    index: int
    rows: int
    columns: int
    has_header: bool = True
    column_names: List[str] = None
    
    def __post_init__(self):
        if self.column_names is None:
            self.column_names = []

@dataclass
class FileInfo:
    """Información completa de un archivo Excel"""
    file_path: Path
    file_name: str
    file_size: int
    created_date: datetime.datetime
    modified_date: datetime.datetime
    sheets: List[SheetInfo]
    total_rows: int = 0
    total_columns: int = 0
    file_format: str = ""
    is_valid: bool = True
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        
        # Calcular totales
        if self.sheets:
            self.total_rows = sum(sheet.rows for sheet in self.sheets)
            self.total_columns = max(sheet.columns for sheet in self.sheets) if self.sheets else 0
        
        # Determinar formato
        if not self.file_format:
            self.file_format = self.file_path.suffix.lower()
    
    @property
    def size_mb(self) -> float:
        """Tamaño del archivo en MB"""
        return self.file_size / (1024 * 1024)
    
    @property
    def sheet_names(self) -> List[str]:
        """Lista de nombres de hojas"""
        return [sheet.name for sheet in self.sheets]
    
    def get_sheet_by_name(self, name: str) -> Optional[SheetInfo]:
        """Obtener hoja por nombre"""
        for sheet in self.sheets:
            if sheet.name == name:
                return sheet
        return None
    
    def get_sheet_by_index(self, index: int) -> Optional[SheetInfo]:
        """Obtener hoja por índice"""
        for sheet in self.sheets:
            if sheet.index == index:
                return sheet
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario"""
        return {
            'file_path': str(self.file_path),
            'file_name': self.file_name,
            'file_size': self.file_size,
            'size_mb': self.size_mb,
            'created_date': self.created_date.isoformat(),
            'modified_date': self.modified_date.isoformat(),
            'total_rows': self.total_rows,
            'total_columns': self.total_columns,
            'file_format': self.file_format,
            'is_valid': self.is_valid,
            'error_message': self.error_message,
            'sheet_count': len(self.sheets),
            'sheet_names': self.sheet_names,
            'metadata': self.metadata
        }