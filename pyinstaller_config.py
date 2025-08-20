#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración optimizada para PyInstaller
Excel Builder Pro
"""

import os
import sys
from pathlib import Path

# Configuración de la aplicación
APP_NAME = "ExcelBuilderPro"
APP_VERSION = "1.0.0"
MAIN_SCRIPT = "main.py"

# Directorios a incluir
DATA_DIRS = [
    "config",
    "ui", 
    "core",
    "models",
    "utils"
]

# Módulos ocultos que PyInstaller debe incluir
HIDDEN_IMPORTS = [
    # Dependencias principales
    "pandas",
    "openpyxl",
    "xlrd",
    "PIL",
    "PIL._tkinter_finder",
    
    # Interfaz gráfica
    "tkinter",
    "tkinter.ttk", 
    "tkinter.messagebox",
    "tkinter.filedialog",
    
    # Utilidades
    "yaml",
    "toml",
    "json5",
    "requests",
    "logging",
    "pathlib",
    "typing",
    
    # Módulos específicos de la aplicación
    "config.settings",
    "config.constants",
    "core.file_manager",
    "core.column_manager", 
    "core.export_manager",
    "core.mapping_manager",
    "core.numeric_generator",
    "ui.main_window",
    "ui.frames.file_frame",
    "ui.frames.column_frame",
    "ui.frames.export_frame",
    "ui.frames.utilities_frame",
    "ui.dialogs.column_config_dialog",
    "ui.dialogs.export_dialog",
    "ui.dialogs.mapping_config_dialog",
    "models.column_config",
    "models.export_config",
    "models.file_info",
    "utils.config_manager",
    "utils.exceptions",
    "utils.helpers",
    "utils.validators"
]

# Archivos a excluir para reducir el tamaño
EXCLUDES = [
    "matplotlib",
    "numpy.tests",
    "pandas.tests", 
    "scipy",
    "IPython",
    "jupyter",
    "notebook",
    "sphinx",
    "pytest",
    "unittest",
    "doctest",
    "pdb",
    "profile",
    "cProfile"
]

# Configuración de PyInstaller
PYINSTALLER_CONFIG = {
    "name": APP_NAME,
    "script": MAIN_SCRIPT,
    "onefile": True,
    "windowed": True,
    "console": False,
    "debug": False,
    "strip": True,
    "upx": True,
    "upx_exclude": [],
    "runtime_tmpdir": None,
    "excludes": EXCLUDES,
    "hiddenimports": HIDDEN_IMPORTS,
    "datas": [(dir_name, dir_name) for dir_name in DATA_DIRS if os.path.exists(dir_name)],
    "icon": "assets/icon.ico" if os.path.exists("assets/icon.ico") else None,
    "clean": True,
    "noconfirm": True
}

def get_pyinstaller_args():
    """Generar argumentos de línea de comandos para PyInstaller"""
    args = [
        "--onefile",
        "--windowed", 
        "--name", APP_NAME,
        "--clean",
        "--noconfirm"
    ]
    
    # Agregar directorios de datos
    for dir_name in DATA_DIRS:
        if os.path.exists(dir_name):
            args.extend(["--add-data", f"{dir_name};{dir_name}"])
    
    # Agregar imports ocultos
    for module in HIDDEN_IMPORTS:
        args.extend(["--hidden-import", module])
    
    # Agregar exclusiones
    for module in EXCLUDES:
        args.extend(["--exclude-module", module])
    
    # Agregar icono si existe
    if os.path.exists("assets/icon.ico"):
        args.extend(["--icon", "assets/icon.ico"])
    
    # Agregar script principal
    args.append(MAIN_SCRIPT)
    
    return args

if __name__ == "__main__":
    print("Configuración de PyInstaller para Excel Builder Pro")
    print("=" * 50)
    print(f"Nombre: {APP_NAME}")
    print(f"Versión: {APP_VERSION}")
    print(f"Script principal: {MAIN_SCRIPT}")
    print(f"Directorios incluidos: {DATA_DIRS}")
    print(f"Módulos ocultos: {len(HIDDEN_IMPORTS)}")
    print(f"Módulos excluidos: {len(EXCLUDES)}")
