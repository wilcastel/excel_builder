# -*- coding: utf-8 -*-
"""
Modelo de configuración de columna
"""

from dataclasses import dataclass
from typing import Optional, Any, Dict
from enum import Enum

class DataType(Enum):
    """Tipos de datos soportados"""
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    DATETIME = "datetime"
    TIME = "time"
    BOOLEAN = "boolean"
    CURRENCY = "currency"
    PERCENTAGE = "percentage"

@dataclass
class ColumnConfig:
    """Configuración de una columna del archivo destino"""
    
    # Información básica
    name: str
    display_name: str
    data_type: DataType
    
    # Configuración de origen
    source_column: Optional[str] = None
    is_generated: bool = False
    
    # Configuración de formato
    format_string: Optional[str] = None
    width: Optional[int] = None
    
    # Configuración de validación
    required: bool = False
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    
    # Configuración de mapeo
    mapping_source: Optional[str] = None
    mapping_key_column: Optional[str] = None
    mapping_value_column: Optional[str] = None
    mapping_additional_keys: list = None  # Columnas adicionales para mapeo multi-columna
    mapping_additional_keys_base: list = None  # Columnas correspondientes en el archivo base
    
    # Configuración de generación numérica
    is_numeric_generator: bool = False
    numeric_start: int = 1
    numeric_grouping_columns: list = None
    
    # Metadatos
    position: int = 0
    description: Optional[str] = None
    
    def __post_init__(self):
        """Inicialización posterior"""
        if self.numeric_grouping_columns is None:
            self.numeric_grouping_columns = []
        if self.mapping_additional_keys is None:
            self.mapping_additional_keys = []
        if self.mapping_additional_keys_base is None:
            self.mapping_additional_keys_base = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario"""
        return {
            "name": self.name,
            "display_name": self.display_name,
            "data_type": self.data_type.value,
            "source_column": self.source_column,
            "is_generated": self.is_generated,
            "format_string": self.format_string,
            "width": self.width,
            "required": self.required,
            "position": self.position,
            "description": self.description,
            # Agregar campos de mapeo
            "mapping_source": self.mapping_source,
            "mapping_key_column": self.mapping_key_column,
            "mapping_value_column": self.mapping_value_column,
            "mapping_additional_keys": self.mapping_additional_keys,
            "mapping_additional_keys_base": self.mapping_additional_keys_base,
            # Agregar campos de generador numérico
            "is_numeric_generator": self.is_numeric_generator,
            "numeric_start": self.numeric_start,
            "numeric_grouping_columns": self.numeric_grouping_columns,
            # Agregar campos de validación
            "min_value": self.min_value,
            "max_value": self.max_value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ColumnConfig':
        """Crear desde diccionario"""
        data_type = DataType(data.get("data_type", "text"))
        return cls(
            name=data["name"],
            display_name=data["display_name"],
            data_type=data_type,
            source_column=data.get("source_column"),
            is_generated=data.get("is_generated", False),
            format_string=data.get("format_string"),
            width=data.get("width"),
            required=data.get("required", False),
            position=data.get("position", 0),
            description=data.get("description"),
            # Agregar campos de mapeo
            mapping_source=data.get("mapping_source"),
            mapping_key_column=data.get("mapping_key_column"),
            mapping_value_column=data.get("mapping_value_column"),
            mapping_additional_keys=data.get("mapping_additional_keys", []),
            mapping_additional_keys_base=data.get("mapping_additional_keys_base", []),
            # Agregar campos de generador numérico
            is_numeric_generator=data.get("is_numeric_generator", False),
            numeric_start=data.get("numeric_start", 1),
            numeric_grouping_columns=data.get("numeric_grouping_columns", []),
            # Agregar campos de validación
            min_value=data.get("min_value"),
            max_value=data.get("max_value")
        )
    
    def validate(self) -> list:
        """Validar configuración de columna"""
        errors = []
        
        if not self.name:
            errors.append("El nombre de la columna es requerido")
        
        if not self.display_name:
            errors.append("El nombre para mostrar es requerido")
        
        # Validación más flexible para columnas generadas
        if self.is_generated:
            # Si es generada, debe tener al menos una de estas opciones:
            # 1. Columna fuente (para mapeo)
            # 2. Generador numérico
            # 3. Configuración de mapeo
            has_source = bool(self.source_column)
            has_numeric = self.is_numeric_generator
            has_mapping = bool(self.mapping_source and self.mapping_key_column and self.mapping_value_column)
            
            if not (has_source or has_numeric or has_mapping):
                errors.append("Las columnas generadas deben tener: columna fuente, ser generador numérico, o tener configuración de mapeo")
        
        return errors