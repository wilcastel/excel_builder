# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Análisis de la aplicación
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),
        ('ui', 'ui'),
        ('core', 'core'),
        ('models', 'models'),
        ('utils', 'utils'),
    ],
    hiddenimports=[
        'pandas',
        'openpyxl',
        'xlrd',
        'PIL',
        'PIL._tkinter_finder',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'yaml',
        'toml',
        'json5',
        'requests',
        'logging',
        'pathlib',
        'typing',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Eliminar archivos innecesarios para reducir el tamaño
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Crear el ejecutable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ExcelBuilderPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin consola para aplicación GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)
