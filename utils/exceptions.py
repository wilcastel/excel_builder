# -*- coding: utf-8 -*-
"""
Excepciones personalizadas para Excel Builder Pro
"""

class ExcelBuilderError(Exception):
    """Excepción base para Excel Builder Pro"""
    pass

class ValidationError(ExcelBuilderError):
    """Error de validación de datos"""
    
    def __init__(self, message: str, errors: list = None):
        super().__init__(message)
        self.errors = errors or []

class FileProcessingError(ExcelBuilderError):
    """Error en procesamiento de archivos"""
    
    def __init__(self, message: str, file_path: str = None):
        super().__init__(message)
        self.file_path = file_path

class ConfigurationError(ExcelBuilderError):
    """Error en configuración"""
    pass

class ExportError(ExcelBuilderError):
    """Error en exportación"""
    
    def __init__(self, message: str, export_config: dict = None):
        super().__init__(message)
        self.export_config = export_config

class MappingError(ExcelBuilderError):
    """Error en mapeo de datos"""
    pass

class NumericGenerationError(ExcelBuilderError):
    """Error en generación numérica"""
    pass