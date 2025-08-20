@echo off
echo ========================================
echo Constructor de Excel Builder Pro
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

echo Python encontrado. Instalando dependencias...

REM Instalar PyInstaller si no está disponible
pip install pyinstaller

echo.
echo Construyendo ejecutable...
echo.

REM Construir usando el archivo .spec
pyinstaller ExcelBuilderPro.spec

if errorlevel 1 (
    echo.
    echo ERROR: Fallo en la construcción
    pause
    exit /b 1
)

echo.
echo ========================================
echo ¡Construcción completada exitosamente!
echo ========================================
echo.
echo El ejecutable se encuentra en: dist\ExcelBuilderPro.exe
echo.
echo Puedes distribuir este archivo a otros usuarios.
echo No necesitan Python instalado para ejecutarlo.
echo.
pause
