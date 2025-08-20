#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para construir el ejecutable de Excel Builder Pro
Usando PyInstaller
"""

import os
import sys
import subprocess
from pathlib import Path

def install_pyinstaller():
    """Instalar PyInstaller si no está disponible"""
    try:
        import PyInstaller
        print("✅ PyInstaller ya está instalado")
    except ImportError:
        print("📦 Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_executable():
    """Construir el ejecutable"""
    print("🔨 Iniciando construcción del ejecutable...")
    
    # Configuración de PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",                    # Un solo archivo ejecutable
        "--windowed",                   # Sin consola (GUI app)
        "--name=ExcelBuilderPro",       # Nombre del ejecutable
        "--icon=assets/icon.ico",       # Icono (si existe)
        "--add-data=config;config",     # Incluir archivos de configuración
        "--add-data=ui;ui",             # Incluir archivos de UI
        "--add-data=core;core",         # Incluir módulos core
        "--add-data=models;models",     # Incluir modelos
        "--add-data=utils;utils",       # Incluir utilidades
        "--hidden-import=pandas",       # Importar pandas explícitamente
        "--hidden-import=openpyxl",     # Importar openpyxl explícitamente
        "--hidden-import=PIL",          # Importar Pillow explícitamente
        "--hidden-import=tkinter",      # Importar tkinter explícitamente
        "--hidden-import=yaml",         # Importar PyYAML explícitamente
        "--hidden-import=toml",         # Importar TOML explícitamente
        "--clean",                      # Limpiar archivos temporales
        "main.py"                       # Punto de entrada
    ]
    
    # Ejecutar PyInstaller
    try:
        subprocess.run(cmd, check=True)
        print("✅ Ejecutable creado exitosamente!")
        print("📁 Ubicación: dist/ExcelBuilderPro.exe")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al crear el ejecutable: {e}")
        return False
    
    return True

def main():
    """Función principal"""
    print("🚀 Constructor de Ejecutable - Excel Builder Pro")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not Path("main.py").exists():
        print("❌ Error: No se encontró main.py en el directorio actual")
        print("   Asegúrate de ejecutar este script desde la raíz del proyecto")
        return
    
    # Instalar PyInstaller si es necesario
    install_pyinstaller()
    
    # Construir el ejecutable
    if build_executable():
        print("\n🎉 ¡Construcción completada!")
        print("📋 Próximos pasos:")
        print("   1. El ejecutable está en: dist/ExcelBuilderPro.exe")
        print("   2. Puedes distribuir este archivo a otros usuarios")
        print("   3. No necesitan Python instalado para ejecutarlo")
    else:
        print("\n❌ La construcción falló. Revisa los errores arriba.")

if __name__ == "__main__":
    main()
