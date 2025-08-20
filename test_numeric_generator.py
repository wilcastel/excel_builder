#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para el generador numérico
Verifica que la agrupación funcione correctamente
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

def create_test_data():
    """Crear datos de prueba similares al ejemplo del usuario"""
    data = {
        'Nombres': [
            'ALBA DAYANA ESPINOSA VERA',
            'CATALINA SANCHEZ GUACARI',
            'MARIA JOSE GARCIA',
            'JUAN CARLOS LOPEZ',
            'ANA MARIA RODRIGUEZ',
            'CARLOS ALBERTO MARTINEZ',
            'LUISA FERNANDA GONZALEZ',
            'PEDRO JOSE HERNANDEZ',
            'SANDRA MILENA TORRES'
        ],
        'Documento': ['12345678', '23456789', '34567890', '45678901', '56789012', '67890123', '78901234', '89012345', '90123456'],
        'Correo': ['alba@test.com', 'catalina@test.com', 'maria@test.com', 'juan@test.com', 'ana@test.com', 'carlos@test.com', 'luisa@test.com', 'pedro@test.com', 'sandra@test.com'],
        'Telefono': ['3001234567', '3002345678', '3003456789', '3004567890', '3005678901', '3006789012', '3007890123', '3008901234', '3009012345'],
        'Nit': ['900123456-1', '900234567-1', '900345678-1', '900456789-1', '900567890-1', '900678901-1', '900789012-1', '900890123-1', '900901234-1'],
        'Razón Social': ['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D', 'Empresa E', 'Empresa F', 'Empresa G', 'Empresa H', 'Empresa I'],
        'Correo Empresa': ['empresa_a@test.com', 'empresa_b@test.com', 'empresa_c@test.com', 'empresa_d@test.com', 'empresa_e@test.com', 'empresa_f@test.com', 'empresa_g@test.com', 'empresa_h@test.com', 'empresa_i@test.com'],
        'Teléfono Em': ['6011234567', '6012345678', '6013456789', '6014567890', '6015678901', '6016789012', '6017890123', '6018901234', '6019012345'],
        'Ciudad': ['VIRTUAL', 'VIRTUAL', 'VIRTUAL', 'VIRTUAL', 'VIRTUAL', 'VIRTUAL', 'VIRTUAL', 'VIRTUAL', 'VIRTUAL'],
        'Fecha': ['18/02/25', '18/02/25', '18/02/25', '18/02/25', '18/02/25', '18/02/25', '18/02/25', '18/02/25', '18/02/25'],
        'Módulo': ['Marco Legal', 'Marco Legal', 'Marco Legal', 'Marco Legal', 'Marco Legal', 'Marco Legal', 'Marco Legal', 'Marco Legal', 'Marco Legal'],
        'Tema': ['DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST', 'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST', 'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST', 'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST', 'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST', 'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST', 'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST', 'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST', 'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST'],
        'Estado': ['Asistio', 'Asistio', 'Asistio', 'Asistio', 'Asistio', 'Asistio', 'Asistio', 'Asistio', 'Asistio']
    }
    
    return pd.DataFrame(data)

def test_numeric_generator():
    """Probar el generador numérico con agrupación"""
    print("🧪 PRUEBA DEL GENERADOR NUMÉRICO")
    print("=" * 60)
    
    # Crear datos de prueba
    data = create_test_data()
    print(f"Datos de prueba creados: {len(data)} filas")
    print(f"Columnas: {list(data.columns)}")
    print()
    
    # Mostrar valores únicos de las columnas de agrupación
    print("📊 VALORES ÚNICOS EN COLUMNAS DE AGRUPACIÓN:")
    print(f"Fecha: {data['Fecha'].unique()}")
    print(f"Módulo: {data['Módulo'].unique()}")
    print(f"Tema: {data['Tema'].unique()}")
    print()
    
    # Configurar export manager
    settings = AppSettings()
    export_manager = ExportManager(settings)
    
    # Crear configuración de columna con generador numérico
    col_config = ColumnConfig(
        name='matricula',
        display_name='Matrícula',
        source_column='',
        data_type=DataType.TEXT,
        required=False,
        is_generated=True,
        is_numeric_generator=True,
        numeric_start=1,
        numeric_grouping_columns=['Fecha', 'Tema', 'Módulo']  # Columnas de agrupación
    )
    
    print("🔧 CONFIGURACIÓN DEL GENERADOR:")
    print(f"Columnas de agrupación: {col_config.numeric_grouping_columns}")
    print(f"Valor inicial: {col_config.numeric_start}")
    print()
    
    # Probar generación de números
    print("📝 RESULTADOS DE LA GENERACIÓN:")
    print("-" * 60)
    
    generated_numbers = []
    for idx, row in data.iterrows():
        number = export_manager._get_column_value(row, col_config, data)
        generated_numbers.append(number)
        print(f"Fila {idx + 1}: {row['Nombres'][:20]}... -> Matrícula: {number}")
    
    print()
    
    # Analizar resultados
    unique_numbers = set(generated_numbers)
    print("📈 ANÁLISIS DE RESULTADOS:")
    print(f"Total de filas: {len(data)}")
    print(f"Números únicos generados: {len(unique_numbers)}")
    print(f"Números generados: {sorted(unique_numbers)}")
    
    # Verificar si la agrupación es correcta
    if len(unique_numbers) == 1:
        print("✅ ÉXITO: Todas las filas tienen el mismo número (agrupación correcta)")
    else:
        print("❌ ERROR: Se generaron números diferentes cuando deberían ser iguales")
        print("   Esto indica que la agrupación no está funcionando correctamente")
    
    print()
    
    # Mostrar contadores del generador
    print("🔢 CONTADORES DEL GENERADOR:")
    for key, value in export_manager.numeric_generator.counters.items():
        print(f"  {key}: {value}")
    
    return len(unique_numbers) == 1

def test_different_groups():
    """Probar con grupos diferentes"""
    print("\n" + "=" * 60)
    print("🧪 PRUEBA CON GRUPOS DIFERENTES")
    print("=" * 60)
    
    # Crear datos con grupos diferentes
    data = create_test_data()
    
    # Modificar algunos valores para crear grupos diferentes
    data.loc[3:5, 'Fecha'] = '19/02/25'  # Grupo diferente
    data.loc[6:8, 'Tema'] = 'OTRO TEMA DIFERENTE'  # Otro grupo diferente
    
    print("📊 DATOS CON GRUPOS DIFERENTES:")
    print(f"Grupo 1 (Fila 1-3): Fecha=18/02/25, Tema=DECRETO 1072...")
    print(f"Grupo 2 (Fila 4-6): Fecha=19/02/25, Tema=DECRETO 1072...")
    print(f"Grupo 3 (Fila 7-9): Fecha=18/02/25, Tema=OTRO TEMA DIFERENTE")
    print()
    
    # Configurar export manager
    settings = AppSettings()
    export_manager = ExportManager(settings)
    
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
        numeric_grouping_columns=['Fecha', 'Tema']
    )
    
    # Probar generación
    print("📝 RESULTADOS CON GRUPOS DIFERENTES:")
    print("-" * 60)
    
    generated_numbers = []
    for idx, row in data.iterrows():
        number = export_manager._get_column_value(row, col_config, data)
        generated_numbers.append(number)
        print(f"Fila {idx + 1}: Fecha={row['Fecha']}, Tema={row['Tema'][:20]}... -> Matrícula: {number}")
    
    print()
    
    # Analizar resultados
    unique_numbers = set(generated_numbers)
    print("📈 ANÁLISIS DE RESULTADOS:")
    print(f"Total de filas: {len(data)}")
    print(f"Números únicos generados: {len(unique_numbers)}")
    print(f"Números generados: {sorted(unique_numbers)}")
    
    # Verificar si hay 3 grupos diferentes
    if len(unique_numbers) == 3:
        print("✅ ÉXITO: Se generaron 3 números diferentes para 3 grupos diferentes")
    else:
        print(f"❌ ERROR: Se esperaban 3 grupos, pero se generaron {len(unique_numbers)} números únicos")
    
    return len(unique_numbers) == 3

def main():
    """Función principal de pruebas"""
    print("🧪 PRUEBAS DEL GENERADOR NUMÉRICO - Excel Builder Pro")
    print("=" * 60)
    
    # Prueba 1: Mismo grupo
    test1_passed = test_numeric_generator()
    
    # Prueba 2: Grupos diferentes
    test2_passed = test_different_groups()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE PRUEBAS")
    print("=" * 60)
    print(f"Prueba 1 (Mismo grupo): {'✅ PASÓ' if test1_passed else '❌ FALLÓ'}")
    print(f"Prueba 2 (Grupos diferentes): {'✅ PASÓ' if test2_passed else '❌ FALLÓ'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON! El generador numérico funciona correctamente.")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisar la implementación del generador numérico.")

if __name__ == "__main__":
    main()

