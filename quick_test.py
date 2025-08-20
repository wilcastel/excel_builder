#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba rápida del generador numérico
"""

import sys
import pandas as pd
from pathlib import Path

# Agregar el directorio raíz al path para imports
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from core.export_manager import ExportManager
from config.settings import AppSettings
from models.column_config import ColumnConfig, DataType

def test_quick():
    """Prueba rápida del generador numérico"""
    print("🧪 PRUEBA RÁPIDA DEL GENERADOR NUMÉRICO")
    print("=" * 50)
    
    # Crear datos de prueba simples
    data = pd.DataFrame({
        'Fecha': ['2025-02-18', '2025-02-18', '2025-02-21', '2025-02-21'],
        'Tema': ['Tema A', 'Tema A', 'Tema B', 'Tema B'],
        'Módulo': ['Módulo 1', 'Módulo 1', 'Módulo 2', 'Módulo 2']
    })
    
    print(f"Datos de prueba: {len(data)} filas")
    print("Grupo 1: Fecha=2025-02-18, Tema=Tema A, Módulo=Módulo 1")
    print("Grupo 2: Fecha=2025-02-21, Tema=Tema B, Módulo=Módulo 2")
    print()
    
    # Configurar export manager
    settings = AppSettings()
    export_manager = ExportManager(settings)
    
    # Verificar que el generador se inicializó correctamente
    print(f"✅ Generador inicializado: {export_manager.numeric_generator is not None}")
    print(f"✅ Contadores disponibles: {export_manager.numeric_generator.counters}")
    print()
    
    # Crear configuración de columna
    col_config = ColumnConfig(
        name='matricula',
        display_name='Matrícula',
        source_column='',
        data_type=DataType.TEXT,
        required=False,
        is_generated=True,
        is_numeric_generator=True,
        numeric_start=1,
        numeric_grouping_columns=['Fecha', 'Tema', 'Módulo']
    )
    
    # Pre-procesar grupos
    export_manager._preprocess_numeric_groups(data, col_config)
    
    print("📝 RESULTADOS:")
    print("-" * 30)
    
    for idx, row in data.iterrows():
        number = export_manager._get_column_value(row, col_config, data)
        print(f"Fila {idx + 1}: Fecha={row['Fecha']}, Tema={row['Tema']} -> Matrícula: {number}")
    
    print()
    print("🔢 CONTADORES FINALES:")
    for key, value in export_manager.numeric_generator.counters.items():
        print(f"  {key}: {value}")
    
    # Verificar resultado
    unique_numbers = set()
    for idx, row in data.iterrows():
        number = export_manager._get_column_value(row, col_config, data)
        unique_numbers.add(number)
    
    print(f"\n📊 Números únicos generados: {len(unique_numbers)}")
    print(f"📊 Números: {sorted(unique_numbers)}")
    
    if len(unique_numbers) == 2:
        print("✅ ÉXITO: Se generaron 2 números diferentes para 2 grupos")
    else:
        print(f"❌ ERROR: Se esperaban 2 grupos, pero se generaron {len(unique_numbers)} números únicos")

if __name__ == "__main__":
    test_quick()

