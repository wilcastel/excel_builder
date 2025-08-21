#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para el mapeo dinámico mejorado
"""

import pandas as pd
import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.mapping_manager import MappingManager
from models.column_config import ColumnConfig, DataType

def create_test_data():
    """Crear datos de prueba similares a los archivos reales"""
    
    # Archivo fuente (datos de capacitaciones)
    source_data = {
        'Código módulo': [1, 2, 3, 4, 5],
        'Nombre programa': [
            'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST',
            'FUNCIONES Y RESPONSABILIDADES COPASST',
            'RECONOCIENDO Y PREVIENDO LOS RIESGOS PSIQ',
            'GESTIÓN DE INDEPENDIENTES Y SU IMPORTANCIA',
            'ASPECTOS BÁSICOS DEL SG-SST'
        ],
        'Verificac': ['Equidad', 'Equidad', 'Equidad', 'Equidad', 'Equidad'],
        'Ciudad': ['Virtual', 'Virtual', 'Virtual', 'Virtual', 'Virtual'],
        'Fecha (DD/MM/AA)': ['18/02/25', '21/02/25', '25/02/25', '28/02/25', '04/03/25'],
        'Direcci': ['Virtual', 'Virtual', 'Virtual', 'Virtual', 'Virtual'],
        'Cupos': [631, 886, 732, 675, 240],
        'Hora inicio (24h)': ['14:00:00', '10:00:00', '14:00:00', '10:00:00', '14:00:00'],
        'nal (24h)': ['16:00:00', '12:00:00', '16:00:00', '12:00:00', '16:00:00'],
        'Dirigido': ['Interés Gel', 'Directivos', 'Responsal', 'Jefes de pr', 'Interés Gel'],
        'Objetivos': ['Objetivo 1', 'Objetivo 2', 'Objetivo 3', 'Objetivo 4', 'Objetivo 5']
    }
    
    # Archivo base (temas y módulos)
    base_data = {
        'Tema': [
            'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST',
            'FUNCIONES Y RESPONSABILIDADES COPASST',
            'RECONOCIENDO Y PREVIENDO LOS RIESGOS PSIQ',
            'GESTIÓN DE INDEPENDIENTES Y SU IMPORTANCIA',
            'ASPECTOS BÁSICOS DEL SG-SST',
            'AUDITORÍA INTERNA DENTRO DEL SG-SST',
            'BRIGADISTA INTERMEDIO',
            'COACHING EN INTELIGENCIA EMOCIONAL'
        ],
        'Módulo': [
            'Marco Legal',
            'Componentes del Sistema de Gestión en Segu',
            'Psicoergonomia',
            'Marco Legal',
            'Componentes del Sistema de Gestión en Segu',
            'Especializados',
            'Brigadista Integral',
            'Sostenibilidad Empresarial'
        ],
        'id': [11, 2, 14, 4, 2, 12, 10, 6],
        'mid': [1, 2, 3, 4, 5, 6, 7, 8],
        'nameMod': [
            'Marco Legal',
            'Componentes del Sistema de Gestión en Segu',
            'Psicoergonomia',
            'Marco Legal',
            'Componentes del Sistema de Gestión en Segu',
            'Especializados',
            'Brigadista Integral',
            'Sostenibilidad Empresarial'
        ]
    }
    
    return pd.DataFrame(source_data), pd.DataFrame(base_data)

def test_simple_mapping():
    """Probar mapeo simple (una columna de referencia)"""
    print("=== PRUEBA: Mapeo Simple ===")
    
    # Crear datos de prueba
    source_df, base_df = create_test_data()
    
    # Crear MappingManager
    mapping_manager = MappingManager()
    mapping_manager.set_base_dataframe(base_df)
    
    # Crear mapeo simple: Nombre programa -> Tema -> id
    mapping_id = mapping_manager.create_dynamic_mapping(
        source_column='Nombre programa',
        base_key_column='Tema',
        base_value_column='id'
    )
    
    print(f"Mapeo creado con ID: {mapping_id}")
    
    # Aplicar mapeo
    mapped_values = mapping_manager.apply_dynamic_mapping(
        source_df=source_df,
        mapping_id=mapping_id,
        default_value='NO_ENCONTRADO'
    )
    
    # Mostrar resultados
    print("\nResultados del mapeo simple:")
    for i, (programa, mapped_id) in enumerate(zip(source_df['Nombre programa'], mapped_values)):
        print(f"  {i+1}. '{programa}' -> {mapped_id}")
    
    # Obtener estadísticas
    stats = mapping_manager.validate_mapping(mapping_id)
    print(f"\nEstadísticas del mapeo: {stats}")
    
    return mapped_values

def test_multi_column_mapping():
    """Probar mapeo multi-columna (múltiples columnas de referencia)"""
    print("\n=== PRUEBA: Mapeo Multi-Columna ===")
    
    # Crear datos de prueba con ambigüedades
    source_data = {
        'Nombre programa': [
            'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST',
            'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST',  # Duplicado
            'FUNCIONES Y RESPONSABILIDADES COPASST',
            'ASPECTOS BÁSICOS DEL SG-SST',
            'ASPECTOS BÁSICOS DEL SG-SST'  # Duplicado
        ],
        'Ciudad': ['Virtual', 'Presencial', 'Virtual', 'Virtual', 'Presencial'],
        'Fecha (DD/MM/AA)': ['18/02/25', '18/02/25', '21/02/25', '25/02/25', '25/02/25']
    }
    
    base_data = {
        'Tema': [
            'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST',
            'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST',
            'FUNCIONES Y RESPONSABILIDADES COPASST',
            'ASPECTOS BÁSICOS DEL SG-SST',
            'ASPECTOS BÁSICOS DEL SG-SST'
        ],
        'Ciudad': ['Virtual', 'Presencial', 'Virtual', 'Virtual', 'Presencial'],
        'Fecha (DD/MM/AA)': ['18/02/25', '18/02/25', '21/02/25', '25/02/25', '25/02/25'],
        'id': [11, 12, 2, 2, 3]  # IDs diferentes para distinguir
    }
    
    source_df = pd.DataFrame(source_data)
    base_df = pd.DataFrame(base_data)
    
    # Crear MappingManager
    mapping_manager = MappingManager()
    mapping_manager.set_base_dataframe(base_df)
    
    # Crear mapeo multi-columna usando Nombre programa + Ciudad + Fecha
    mapping_id = mapping_manager.create_dynamic_mapping(
        source_column='Nombre programa',
        base_key_column='Tema',
        base_value_column='id',
        additional_keys=['Ciudad', 'Fecha (DD/MM/AA)']
    )
    
    print(f"Mapeo multi-columna creado con ID: {mapping_id}")
    
    # Aplicar mapeo
    mapped_values = mapping_manager.apply_dynamic_mapping(
        source_df=source_df,
        mapping_id=mapping_id,
        default_value='NO_ENCONTRADO'
    )
    
    # Mostrar resultados
    print("\nResultados del mapeo multi-columna:")
    for i, (programa, ciudad, fecha, mapped_id) in enumerate(
        zip(source_df['Nombre programa'], source_df['Ciudad'], 
            source_df['Fecha (DD/MM/AA)'], mapped_values)):
        print(f"  {i+1}. '{programa}' + '{ciudad}' + '{fecha}' -> {mapped_id}")
    
    # Obtener estadísticas
    stats = mapping_manager.validate_mapping(mapping_id)
    print(f"\nEstadísticas del mapeo multi-columna: {stats}")
    
    return mapped_values

def test_date_normalization():
    """Probar normalización de fechas"""
    print("\n=== PRUEBA: Normalización de Fechas ===")
    
    # Crear datos con diferentes formatos de fecha
    source_data = {
        'Nombre programa': ['Programa 1', 'Programa 2', 'Programa 3'],
        'Fecha (DD/MM/AA)': ['2025-02-18', '18/02/2025', '18-02-25']
    }
    
    base_data = {
        'Tema': ['Programa 1', 'Programa 2', 'Programa 3'],
        'Fecha (DD/MM/AA)': ['18/02/25', '18/02/25', '18/02/25'],
        'id': [1, 2, 3]
    }
    
    source_df = pd.DataFrame(source_data)
    base_df = pd.DataFrame(base_data)
    
    # Crear MappingManager
    mapping_manager = MappingManager()
    mapping_manager.set_base_dataframe(base_df)
    
    # Crear mapeo usando fecha
    mapping_id = mapping_manager.create_dynamic_mapping(
        source_column='Fecha (DD/MM/AA)',
        base_key_column='Fecha (DD/MM/AA)',
        base_value_column='id'
    )
    
    print(f"Mapeo de fechas creado con ID: {mapping_id}")
    
    # Aplicar mapeo
    mapped_values = mapping_manager.apply_dynamic_mapping(
        source_df=source_df,
        mapping_id=mapping_id,
        default_value='NO_ENCONTRADO'
    )
    
    # Mostrar resultados
    print("\nResultados de normalización de fechas:")
    for i, (fecha, mapped_id) in enumerate(zip(source_df['Fecha (DD/MM/AA)'], mapped_values)):
        print(f"  {i+1}. '{fecha}' -> {mapped_id}")
    
    return mapped_values

def test_column_config_integration():
    """Probar integración con ColumnConfig"""
    print("\n=== PRUEBA: Integración con ColumnConfig ===")
    
    # Crear datos de prueba
    source_df, base_df = create_test_data()
    
    # Crear configuración de columna con mapeo dinámico
    col_config = ColumnConfig(
        name='codigo_modulo',
        display_name='Código Módulo',
        data_type=DataType.NUMBER,
        is_generated=True,
        mapping_source='Nombre programa',
        mapping_key_column='Tema',
        mapping_value_column='id',
        mapping_additional_keys=[]  # Sin columnas adicionales para mapeo simple
    )
    
    print(f"Configuración de columna creada: {col_config.display_name}")
    print(f"  - Tipo: {col_config.data_type.value}")
    print(f"  - Es generada: {col_config.is_generated}")
    print(f"  - Mapeo: {col_config.mapping_source} -> {col_config.mapping_key_column} -> {col_config.mapping_value_column}")
    
    # Crear MappingManager
    mapping_manager = MappingManager()
    mapping_manager.set_base_dataframe(base_df)
    
    # Crear mapeo usando la configuración de columna
    mapping_id = mapping_manager.create_dynamic_mapping(
        source_column=col_config.mapping_source,
        base_key_column=col_config.mapping_key_column,
        base_value_column=col_config.mapping_value_column,
        additional_keys=col_config.mapping_additional_keys
    )
    
    print(f"Mapeo creado con ID: {mapping_id}")
    
    # Aplicar mapeo
    mapped_values = mapping_manager.apply_dynamic_mapping(
        source_df=source_df,
        mapping_id=mapping_id,
        default_value=0
    )
    
    # Mostrar resultados
    print("\nResultados de integración con ColumnConfig:")
    for i, (programa, mapped_id) in enumerate(zip(source_df['Nombre programa'], mapped_values)):
        print(f"  {i+1}. '{programa}' -> {mapped_id}")
    
    return mapped_values

def main():
    """Función principal de pruebas"""
    print("🧪 PRUEBAS DEL MAPEO DINÁMICO MEJORADO")
    print("=" * 50)
    
    try:
        # Ejecutar todas las pruebas
        test_simple_mapping()
        test_multi_column_mapping()
        test_date_normalization()
        test_column_config_integration()
        
        print("\n✅ Todas las pruebas completadas exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error en las pruebas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
