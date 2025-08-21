#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel Builder Pro - Constructor Dinámico de Archivos Excel
Punto de entrada principal de la aplicación

Autor: wilcastell
Versión: 1.0.0
Fecha: 2025
"""

import sys
import os
import importlib
from pathlib import Path



# Agregar el directorio raíz al path para imports
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Forzar recarga de módulos para desarrollo
def force_reload_modules():
    """Forzar recarga de módulos para desarrollo"""
    modules_to_reload = [
        'core.mapping_manager',
        'core.export_manager',
        'core.file_manager',
        'core.column_manager',
        'ui.main_window',
        'ui.frames.column_frame',
        'ui.frames.export_frame',
        'ui.dialogs.column_config_dialog'
    ]
    
    for module_name in modules_to_reload:
        if module_name in sys.modules:
            try:
                importlib.reload(sys.modules[module_name])
            except Exception as e:
                pass

from ui.main_window import MainWindow
from config.settings import AppSettings
from utils.helpers import setup_logging

# Recargar módulos DESPUÉS de que se carguen
force_reload_modules()

def main():
    """Función principal de la aplicación"""
    try:

        
        # Inicializar configuración primero
        settings = AppSettings()
        
        # Configurar logging con la configuración
        setup_logging(settings)
        
        # Crear y ejecutar la aplicación
        app = MainWindow(settings)
        app.run()
        
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()