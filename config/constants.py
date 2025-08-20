# -*- coding: utf-8 -*-
"""
Constantes de la aplicación
"""

# Formatos de archivo soportados
SUPPORTED_FORMATS = {
    ".xlsx": "Excel 2007+ (*.xlsx)",
    ".xls": "Excel 97-2003 (*.xls)",
    ".csv": "Valores separados por comas (*.csv)",
    ".json": "JavaScript Object Notation (*.json)",
    ".txt": "Archivo de texto (*.txt)"
}

# Extensiones de archivo de entrada
INPUT_EXTENSIONS = [".xlsx", ".xls"]

# Extensiones de archivo de salida
OUTPUT_EXTENSIONS = [".xlsx", ".csv", ".json", ".txt"]

# Formatos de exportación soportados
SUPPORTED_EXPORT_FORMATS = {
    "xlsx": "Excel 2007+ (*.xlsx)",
    "csv": "Valores separados por comas (*.csv)",
    "json": "JavaScript Object Notation (*.json)",
    "txt": "Archivo de texto (*.txt)"
}

# Tamaños máximos de archivo (en bytes)
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
MAX_PREVIEW_ROWS = 1000
MAX_COLUMNS = 256

# Tipos de datos soportados
DATA_TYPES = {
    "text": "Texto",
    "number": "Número",
    "date": "Fecha",
    "datetime": "Fecha y Hora",
    "time": "Hora",
    "boolean": "Verdadero/Falso",
    "currency": "Moneda",
    "percentage": "Porcentaje"
}

# Colores para tipos de datos
DATA_TYPE_COLORS = {
    "text": "#E3F2FD",      # Azul claro
    "number": "#E8F5E8",    # Verde claro
    "date": "#FFF3E0",      # Naranja claro
    "datetime": "#FCE4EC",  # Rosa claro
    "time": "#F3E5F5",     # Púrpura claro
    "boolean": "#FFEBEE",   # Rojo claro
    "currency": "#E0F2F1",  # Verde agua claro
    "percentage": "#FFF8E1" # Amarillo claro
}

# Formatos de fecha
DATE_FORMATS = {
    "dd/mm/yyyy": "31/12/2023",
    "mm/dd/yyyy": "12/31/2023",
    "yyyy-mm-dd": "2023-12-31",
    "dd-mm-yyyy": "31-12-2023",
    "dd/mm/yy": "31/12/23"
}

# Formatos de número
NUMBER_FORMATS = {
    "general": "General",
    "0": "Entero",
    "0.00": "Decimal (2 dígitos)",
    "#,##0": "Entero con separadores",
    "#,##0.00": "Decimal con separadores",
    "0%": "Porcentaje",
    "0.00%": "Porcentaje (2 dígitos)"
}

# Tipos de generación numérica
NUMERIC_TYPES = {
    "simple": "Numeración Simple",
    "grouped": "Numeración Agrupada",
    "matricula": "Matrícula Académica"
}

# Tipos de matrícula
MATRICULA_TYPES = {
    "REG": "Regular",
    "TRA": "Traslado",
    "ESP": "Especial",
    "VIS": "Visitante",
    "INT": "Internacional"
}

# Tipos de mapeo
MAPPING_TYPES = {
    "simple": "Mapeo Simple",
    "multi_column": "Mapeo Multi-columna"
}

# Colores de interfaz
COLORS = {
    "primary": "#1976D2",
    "secondary": "#424242",
    "success": "#4CAF50",
    "warning": "#FF9800",
    "error": "#F44336",
    "info": "#2196F3",
    "light": "#F5F5F5",
    "dark": "#212121"
}

# Iconos (usando emojis para simplicidad)
ICONS = {
    "file": "📁",
    "excel": "📊",
    "config": "⚙️",
    "preview": "👁️",
    "export": "💾",
    "add": "➕",
    "edit": "✏️",
    "delete": "🗑️",
    "up": "⬆️",
    "down": "⬇️",
    "check": "✅",
    "warning": "⚠️",
    "error": "❌",
    "info": "ℹ️"
}

# Mensajes de la aplicación
MESSAGES = {
    "file_loaded": "Archivo cargado correctamente",
    "file_error": "Error al cargar el archivo",
    "export_success": "Archivo exportado exitosamente",
    "export_error": "Error al exportar el archivo",
    "validation_error": "Error de validación",
    "no_file_selected": "No se ha seleccionado ningún archivo",
    "no_columns_selected": "No se han seleccionado columnas",
    "invalid_configuration": "Configuración inválida",
    "file_too_large": "El archivo es demasiado grande",
    "unsupported_format": "Formato de archivo no soportado",
    "backup_created": "Copia de seguridad creada",
    "processing": "Procesando...",
    "ready": "Listo"
}

# Configuración de ventanas
WINDOW_CONFIG = {
    "main_window": {
        "title": "Excel Builder Pro",
        "width": 1200,
        "height": 800,
        "min_width": 800,
        "min_height": 600
    },
    "dialog": {
        "width": 600,
        "height": 400
    }
}

# Configuración de logging
LOG_LEVELS = {
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50
}

# Configuración de exportación por defecto
DEFAULT_EXPORT_CONFIG = {
    "format": "xlsx",
    "include_headers": True,
    "auto_adjust_columns": True,
    "create_backup": True,
    "max_rows_per_file": 100000
}

# Configuración de validación
VALIDATION_RULES = {
    "max_column_name_length": 255,
    "max_sheet_name_length": 31,
    "max_file_name_length": 255,
    "min_numeric_value": -999999999,
    "max_numeric_value": 999999999
}

# Patrones de expresiones regulares
REGEX_PATTERNS = {
    "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    "phone": r"^[+]?[1-9]?[0-9]{7,15}$",
    "numeric": r"^-?\d*\.?\d+$",
    "date_iso": r"^\d{4}-\d{2}-\d{2}$",
    "time": r"^\d{2}:\d{2}(:\d{2})?$"
}

# Configuración de temas
THEMES = {
    "light": {
        "bg": "#FFFFFF",
        "fg": "#000000",
        "select_bg": "#0078D4",
        "select_fg": "#FFFFFF"
    },
    "dark": {
        "bg": "#2D2D2D",
        "fg": "#FFFFFF",
        "select_bg": "#0078D4",
        "select_fg": "#FFFFFF"
    }
}