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
from pathlib import Path

# Agregar el directorio raíz al path para imports
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from ui.main_window import MainWindow
from config.settings import AppSettings
from utils.helpers import setup_logging

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