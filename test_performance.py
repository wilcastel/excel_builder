#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba de rendimiento para Excel Builder Pro
Verifica las optimizaciones implementadas
"""

import sys
import os
import time
import pandas as pd
from pathlib import Path
import logging

# Agregar el directorio raíz al path para imports
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from core.export_manager import ExportManager
from config.settings import AppSettings
from models.column_config import ColumnConfig, DataType

def create_test_data(rows: int, columns: int = 10) -> pd.DataFrame:
    """Crear datos de prueba"""
    print(f"Creando datos de prueba: {rows} filas x {columns} columnas")
    
    data = {}
    for i in range(columns):
        if i == 0:
            # Columna de texto
            data[f'columna_{i}'] = [f'valor_{j}' for j in range(rows)]
        elif i == 1:
            # Columna numérica
            data[f'columna_{i}'] = list(range(1, rows + 1))
        elif i == 2:
            # Columna de fecha
            data[f'columna_{i}'] = pd.date_range('2025-01-01', periods=rows, freq='D')
        else:
            # Columnas mixtas
            data[f'columna_{i}'] = [f'dato_{j}_{i}' for j in range(rows)]
    
    return pd.DataFrame(data)

def create_test_columns(num_columns: int = 10) -> list:
    """Crear configuración de columnas de prueba"""
    columns = []
    
    for i in range(num_columns):
        col_config = ColumnConfig(
            name=f'columna_{i}',
            display_name=f'Columna {i}',
            source_column=f'columna_{i}',
            data_type=DataType.TEXT,
            required=False,
            is_generated=False
        )
        
        # Configurar tipos específicos
        if i == 1:
            col_config.data_type = DataType.NUMBER
        elif i == 2:
            col_config.data_type = DataType.DATE
        
        columns.append(col_config)
    
    return columns

def test_export_performance(rows: int, columns: int = 10, iterations: int = 3):
    """Probar rendimiento de exportación"""
    print(f"\n{'='*60}")
    print(f"PRUEBA DE RENDIMIENTO: {rows:,} filas x {columns} columnas")
    print(f"{'='*60}")
    
    # Crear datos de prueba
    data = create_test_data(rows, columns)
    column_configs = create_test_columns(columns)
    
    # Configurar export manager
    settings = AppSettings()
    export_manager = ExportManager(settings)
    
    # Configurar logging para prueba
    logging.getLogger().setLevel(logging.WARNING)
    
    # Realizar múltiples iteraciones
    times = []
    
    for i in range(iterations):
        print(f"\nIteración {i + 1}/{iterations}")
        
        # Limpiar cache
        export_manager.cleanup()
        
        # Medir tiempo de exportación
        start_time = time.time()
        
        try:
            result = export_manager.export_excel(
                source_data=data,
                column_configs=column_configs,
                export_config={'output_file': f'test_performance_{rows}_{i}.xlsx'}
            )
            
            end_time = time.time()
            export_time = end_time - start_time
            times.append(export_time)
            
            print(f"✅ Exportación completada en {export_time:.2f} segundos")
            print(f"   - Filas procesadas: {result['rows_processed']:,}")
            print(f"   - Archivos creados: {result['files_created']}")
            
            if 'split_info' in result:
                print(f"   - Archivo dividido en {result['split_info']['total_files']} partes")
            
        except Exception as e:
            print(f"❌ Error en exportación: {e}")
            return None
    
    # Calcular estadísticas
    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"\n📊 RESULTADOS:")
        print(f"   - Tiempo promedio: {avg_time:.2f} segundos")
        print(f"   - Tiempo mínimo: {min_time:.2f} segundos")
        print(f"   - Tiempo máximo: {max_time:.2f} segundos")
        print(f"   - Filas por segundo: {rows/avg_time:,.0f}")
        
        return avg_time
    
    return None

def main():
    """Función principal de pruebas"""
    print("🧪 PRUEBAS DE RENDIMIENTO - Excel Builder Pro")
    print("=" * 60)
    
    # Configurar logging
    logging.basicConfig(level=logging.WARNING)
    
    # Definir tamaños de prueba
    test_sizes = [
        (100, "Pequeño"),
        (1_000, "Mediano"),
        (5_000, "Mediano-Grande"),
        (10_000, "Grande"),
        (25_000, "Muy Grande")
    ]
    
    results = {}
    
    for rows, description in test_sizes:
        print(f"\n{'='*60}")
        print(f"PROBANDO: {description} ({rows:,} filas)")
        print(f"{'='*60}")
        
        try:
            avg_time = test_export_performance(rows, columns=10, iterations=2)
            if avg_time:
                results[rows] = {
                    'description': description,
                    'time': avg_time,
                    'rows_per_second': rows / avg_time
                }
        except Exception as e:
            print(f"❌ Error en prueba de {description}: {e}")
    
    # Mostrar resumen final
    print(f"\n{'='*60}")
    print("📈 RESUMEN DE RENDIMIENTO")
    print(f"{'='*60}")
    
    if results:
        print(f"{'Tamaño':<15} {'Filas':<10} {'Tiempo (s)':<12} {'Filas/s':<12}")
        print("-" * 60)
        
        for rows, data in results.items():
            print(f"{data['description']:<15} {rows:<10,} {data['time']:<12.2f} {data['rows_per_second']:<12,.0f}")
        
        # Calcular mejora estimada
        if len(results) >= 2:
            small_time = results[100]['time']
            large_time = results[10000]['time']
            
            # Estimación de mejora (tiempo esperado vs tiempo real)
            expected_time_large = small_time * (10000 / 100)  # Escalado lineal
            actual_time_large = large_time
            
            if expected_time_large > actual_time_large:
                improvement = ((expected_time_large - actual_time_large) / expected_time_large) * 100
                print(f"\n🚀 Mejora estimada en archivos grandes: {improvement:.1f}%")
    
    print(f"\n✅ Pruebas completadas")
    print(f"📁 Archivos de prueba creados en: {Path('exportados')}")

if __name__ == "__main__":
    main()
