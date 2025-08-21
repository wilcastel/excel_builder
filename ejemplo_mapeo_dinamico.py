#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplo Práctico: Mapeo Dinámico para ExcelBuilderPro
Caso específico: Mapear 'Nombre programa' → 'Tema' → 'id'
"""

import pandas as pd
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.mapping_manager import MappingManager
from models.column_config import ColumnConfig, DataType

def crear_datos_ejemplo():
    """Crear datos de ejemplo basados en las imágenes proporcionadas"""
    
    # Archivo fuente (capacitaciones virtuales 2025)
    source_data = {
        'Código módulo': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'Nombre programa': [
            'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST',
            'FUNCIONES Y RESPONSABILIDADES COPASST',
            'RECONOCIENDO Y PREVIENDO LOS RIESGOS PSIQ',
            'GESTIÓN DE INDEPENDIENTES Y SU IMPORTANCIA',
            'ASPECTOS BÁSICOS DEL SG-SST',
            'AUDITORÍA INTERNA DENTRO DEL SG-SST',
            'BRIGADISTA INTERMEDIO',
            'COACHING EN INTELIGENCIA EMOCIONAL',
            'COACHING EN SBC',
            'COACHING PARA LA SEGURIDAD Y SALUD EN EL TRABAJO'
        ],
        'Verificac': ['Equidad'] * 10,
        'Ciudad': ['Virtual'] * 10,
        'Fecha (DD/MM/AA)': ['18/02/25', '21/02/25', '25/02/25', '28/02/25', '04/03/25', 
                            '07/03/25', '11/03/25', '14/03/25', '18/03/25', '21/03/25'],
        'Direcci': ['Virtual'] * 10,
        'Cupos': [631, 886, 732, 675, 240, 560, 183, 291, 408, 807],
        'Hora inicio (24h)': ['14:00:00', '10:00:00', '14:00:00', '10:00:00', '14:00:00',
                              '10:00:00', '14:00:00', '10:00:00', '14:00:00', '10:00:00'],
        'nal (24h)': ['16:00:00', '12:00:00', '16:00:00', '12:00:00', '16:00:00',
                      '12:00:00', '16:00:00', '12:00:00', '16:00:00', '12:00:00'],
        'Dirigido': ['Interés Gel', 'Directivos', 'Responsal', 'Jefes de pr', 'Interés Gel',
                     'Directivos', 'Responsal', 'Jefes de pr', 'Interés Gel', 'Directivos'],
        'Objetivos': [f'Objetivo {i}' for i in range(1, 11)]
    }
    
    # Archivo base (temas y módulos 2018-24)
    base_data = {
        'Tema': [
            'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST',
            'FUNCIONES Y RESPONSABILIDADES COPASST',
            'RECONOCIENDO Y PREVIENDO LOS RIESGOS PSIQ',
            'GESTIÓN DE INDEPENDIENTES Y SU IMPORTANCIA',
            'ASPECTOS BÁSICOS DEL SG-SST',
            'AUDITORÍA INTERNA DENTRO DEL SG-SST',
            'BRIGADISTA INTERMEDIO',
            'COACHING EN INTELIGENCIA EMOCIONAL',
            'COACHING EN SBC',
            'COACHING PARA LA SEGURIDAD Y SALUD EN EL TRABAJO',
            'COMITÉS DE CONVIVENCIA EFECTIVOS',
            'CÓMO ACTUAR FRENTE AL RIESGO PÚBLICO',
            'COMPORTAMIENTO SEGURO FRENTE AL RIESGO BIOLÓGICO',
            'COMUNICACIÓN ASERTIVA EN SST',
            'CONCIENCIA Y CUIDADO: POLÍTICA DE PREVENCIÓN DE CONSUM'
        ],
        'Módulo': [
            'Marco Legal',
            'Componentes del Sistema de Gestión en Segu',
            'Psicoergonomia',
            'Marco Legal',
            'Componentes del Sistema de Gestión en Segu',
            'Especializados',
            'Brigadista Integral',
            'Sostenibilidad Empresarial',
            'Seguridad Industrial',
            'Salud Laboral',
            'Psicoergonomia',
            'Biomecánico',
            'Higiene y seguridad industrial',
            'Prevención integral en emergencias',
            'Riesgo público'
        ],
        'id': [11, 2, 14, 4, 2, 12, 10, 6, 4, 8, 15, 16, 17, 18, 19],
        'mid': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        'nameMod': [
            'Marco Legal',
            'Componentes del Sistema de Gestión en Segu',
            'Psicoergonomia',
            'Marco Legal',
            'Componentes del Sistema de Gestión en Segu',
            'Especializados',
            'Brigadista Integral',
            'Sostenibilidad Empresarial',
            'Seguridad Industrial',
            'Salud Laboral',
            'Psicoergonomia',
            'Biomecánico',
            'Higiene y seguridad industrial',
            'Prevención integral en emergencias',
            'Riesgo público'
        ]
    }
    
    return pd.DataFrame(source_data), pd.DataFrame(base_data)

def ejemplo_mapeo_simple():
    """Ejemplo 1: Mapeo simple como se describe en el caso del usuario"""
    print("🎯 EJEMPLO 1: Mapeo Simple (Tu Caso Principal)")
    print("=" * 60)
    
    # Crear datos de ejemplo
    source_df, base_df = crear_datos_ejemplo()
    
    print("📁 Archivo Fuente (capacitaciones_virtuales_2025.xlsx):")
    print(f"   - Filas: {len(source_df)}")
    print(f"   - Columnas: {list(source_df.columns)}")
    print()
    
    print("📁 Archivo Base (temas_modulos_2018_24.xlsx):")
    print(f"   - Filas: {len(base_df)}")
    print(f"   - Columnas: {list(base_df.columns)}")
    print()
    
    # Crear MappingManager
    mapping_manager = MappingManager()
    mapping_manager.set_base_dataframe(base_df)
    
    # PASO 1: Crear mapeo dinámico
    print("🔧 PASO 1: Crear mapeo dinámico")
    print("   Configuración:")
    print("   - Columna de referencia (archivo fuente): 'Nombre programa'")
    print("   - Columna clave (archivo base): 'Tema'")
    print("   - Columna valor (archivo base): 'id'")
    print()
    
    mapping_id = mapping_manager.create_dynamic_mapping(
        source_column='Nombre programa',
        base_key_column='Tema',
        base_value_column='id'
    )
    
    print(f"   ✅ Mapeo creado con ID: {mapping_id}")
    
    # PASO 2: Aplicar mapeo
    print("\n🔧 PASO 2: Aplicar mapeo al archivo fuente")
    mapped_values = mapping_manager.apply_dynamic_mapping(
        source_df=source_df,
        mapping_id=mapping_id,
        default_value='NO_ENCONTRADO'
    )
    
    # PASO 3: Mostrar resultados
    print("\n📊 RESULTADOS DEL MAPEO:")
    print("-" * 80)
    print(f"{'#':<3} {'Nombre Programa':<50} {'ID Mapeado':<12}")
    print("-" * 80)
    
    for i, (programa, mapped_id) in enumerate(zip(source_df['Nombre programa'], mapped_values), 1):
        programa_short = programa[:47] + "..." if len(programa) > 50 else programa
        print(f"{i:<3} {programa_short:<50} {mapped_id:<12}")
    
    # PASO 4: Estadísticas
    print("\n📈 ESTADÍSTICAS:")
    stats = mapping_manager.validate_mapping(mapping_id)
    print(f"   - Total de entradas en mapeo: {stats['total_entries']}")
    print(f"   - Valores únicos encontrados: {stats['unique_values']}")
    print(f"   - Tipos de valores: {stats['value_types']}")
    
    return mapped_values

def ejemplo_mapeo_multi_columna():
    """Ejemplo 2: Mapeo multi-columna para casos con ambigüedades"""
    print("\n\n🎯 EJEMPLO 2: Mapeo Multi-Columna (Para Evitar Ambigüedades)")
    print("=" * 70)
    
    # Crear datos con ambigüedades (mismo programa en diferentes fechas)
    source_data = {
        'Nombre programa': [
            'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST',
            'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST',  # Duplicado
            'ASPECTOS BÁSICOS DEL SG-SST',
            'ASPECTOS BÁSICOS DEL SG-SST'  # Duplicado
        ],
        'Ciudad': ['Virtual', 'Presencial', 'Virtual', 'Presencial'],
        'Fecha (DD/MM/AA)': ['18/02/25', '18/02/25', '25/02/25', '25/02/25']
    }
    
    base_data = {
        'Tema': [
            'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST',
            'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST',
            'ASPECTOS BÁSICOS DEL SG-SST',
            'ASPECTOS BÁSICOS DEL SG-SST'
        ],
        'Ciudad': ['Virtual', 'Presencial', 'Virtual', 'Presencial'],
        'Fecha (DD/MM/AA)': ['18/02/25', '18/02/25', '25/02/25', '25/02/25'],
        'id': [11, 12, 2, 3]  # IDs diferentes para distinguir
    }
    
    source_df = pd.DataFrame(source_data)
    base_df = pd.DataFrame(base_data)
    
    # Crear MappingManager
    mapping_manager = MappingManager()
    mapping_manager.set_base_dataframe(base_df)
    
    print("🔧 Configuración de mapeo multi-columna:")
    print("   - Columna principal: 'Nombre programa'")
    print("   - Columnas adicionales: ['Ciudad', 'Fecha (DD/MM/AA)']")
    print("   - Objetivo: Evitar ambigüedades cuando el mismo programa aparece en diferentes fechas")
    print()
    
    # Crear mapeo multi-columna
    mapping_id = mapping_manager.create_dynamic_mapping(
        source_column='Nombre programa',
        base_key_column='Tema',
        base_value_column='id',
        additional_keys=['Ciudad', 'Fecha (DD/MM/AA)']
    )
    
    # Aplicar mapeo
    mapped_values = mapping_manager.apply_dynamic_mapping(
        source_df=source_df,
        mapping_id=mapping_id,
        default_value='NO_ENCONTRADO'
    )
    
    # Mostrar resultados
    print("📊 RESULTADOS DEL MAPEO MULTI-COLUMNA:")
    print("-" * 90)
    print(f"{'#':<3} {'Programa':<40} {'Ciudad':<10} {'Fecha':<10} {'ID':<5}")
    print("-" * 90)
    
    for i, (programa, ciudad, fecha, mapped_id) in enumerate(
        zip(source_df['Nombre programa'], source_df['Ciudad'], 
            source_df['Fecha (DD/MM/AA)'], mapped_values), 1):
        programa_short = programa[:37] + "..." if len(programa) > 40 else programa
        print(f"{i:<3} {programa_short:<40} {ciudad:<10} {fecha:<10} {mapped_id:<5}")
    
    print("\n💡 Observación: Ahora cada combinación única tiene su propio ID")
    
    return mapped_values

def ejemplo_integracion_column_config():
    """Ejemplo 3: Integración completa con ColumnConfig"""
    print("\n\n🎯 EJEMPLO 3: Integración con ColumnConfig (Como en la UI)")
    print("=" * 60)
    
    # Crear datos de ejemplo
    source_df, base_df = crear_datos_ejemplo()
    
    # Crear configuración de columna como se haría en la interfaz
    col_config = ColumnConfig(
        name='codigo_modulo',
        display_name='Código Módulo',
        data_type=DataType.NUMBER,
        is_generated=True,
        position=1,
        mapping_source='Nombre programa',
        mapping_key_column='Tema',
        mapping_value_column='id',
        mapping_additional_keys=[]  # Sin columnas adicionales para mapeo simple
    )
    
    print("🔧 Configuración de columna creada:")
    print(f"   - Nombre: {col_config.display_name}")
    print(f"   - Tipo: {col_config.data_type.value}")
    print(f"   - Es generada: {col_config.is_generated}")
    print(f"   - Posición: {col_config.position}")
    print(f"   - Mapeo: {col_config.mapping_source} → {col_config.mapping_key_column} → {col_config.mapping_value_column}")
    print()
    
    # Crear MappingManager
    mapping_manager = MappingManager()
    mapping_manager.set_base_dataframe(base_df)
    
    # Crear mapeo usando la configuración
    mapping_id = mapping_manager.create_dynamic_mapping(
        source_column=col_config.mapping_source,
        base_key_column=col_config.mapping_key_column,
        base_value_column=col_config.mapping_value_column,
        additional_keys=col_config.mapping_additional_keys
    )
    
    # Aplicar mapeo
    mapped_values = mapping_manager.apply_dynamic_mapping(
        source_df=source_df,
        mapping_id=mapping_id,
        default_value=0
    )
    
    # Crear DataFrame de resultado
    result_df = source_df.copy()
    result_df[col_config.display_name] = mapped_values
    
    print("📊 RESULTADO FINAL (DataFrame con columna mapeada):")
    print("-" * 100)
    print(result_df[['Nombre programa', col_config.display_name]].head(10))
    
    print(f"\n✅ Columna '{col_config.display_name}' agregada exitosamente con {len(mapped_values)} valores")
    
    return result_df

def main():
    """Función principal del ejemplo"""
    print("🚀 EJEMPLO PRÁCTICO: MAPEO DINÁMICO EN EXCELBUILDERPRO")
    print("=" * 70)
    print("Este ejemplo muestra cómo usar el mapeo dinámico mejorado")
    print("para el caso específico descrito en las imágenes.")
    print()
    
    try:
        # Ejecutar ejemplos
        ejemplo_mapeo_simple()
        ejemplo_mapeo_multi_columna()
        ejemplo_integracion_column_config()
        
        print("\n" + "=" * 70)
        print("✅ TODOS LOS EJEMPLOS COMPLETADOS EXITOSAMENTE!")
        print("\n💡 Para usar en ExcelBuilderPro:")
        print("   1. Cargar archivo fuente (capacitaciones_virtuales_2025.xlsx)")
        print("   2. Cargar archivo base (temas_modulos_2018_24.xlsx)")
        print("   3. Ir a pestaña 'Columnas'")
        print("   4. Configurar columna 'Código módulo' como generada")
        print("   5. Activar mapeo dinámico con la configuración mostrada")
        print("   6. Exportar y verificar resultados")
        
    except Exception as e:
        print(f"\n❌ Error en los ejemplos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
