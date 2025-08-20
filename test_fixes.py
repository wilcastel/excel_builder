#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar las correcciones del generador numérico y formato de fecha
"""

import sys
import pandas as pd
from pathlib import Path
from datetime import datetime

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
            'YULIED AREVALO',
            'SANDRA MILENA VALENCIA MA',
            'LUIS EDUARDO AMAYA',
            'SILVIA ADRIANA RUANO CORTE',
            'LETICIA CERDAS AMADO',
            'SANDRA ANYELY ARIAS CÁCER',
            'MARIANA NUÑEZ CARDENAS',
            'KAROL MORENO CAICEDO',
            'MELINA ANDREA LASSO ORTEC'
        ],
        'Documento': ['60350189', '40331200', '1090400427', '27105646', '60334558', '37272258', '1108599321', '1022418751', '1085661803'],
        'Correo': ['asistentesgi@jucamal.com', 'sami1129@hotmail.es', 'asistentesgi@jucamal.com', 'sarc1384@gmail.com', 'saludocupacional@transmateria', 'anyely_07_@hotmail.com', 'imporberaca05@gmail.com', 'karol.moreno@proyecformas.cc', 'elin1332@gmail.com'],
        'Telefono': ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
        'Nit': ['900409401.0', '892000435.0', '900409401.0', '901011594.0', '890500988.0', '900362666.0', '901489102.0', '830074655.0', '891201588.0'],
        'Razón Social': ['JUCAMAL SAS', 'COOPERATIVA DE TRANSPORT.', 'JUCAMAL SAS', 'GRUPO HERITAGE SAS', 'TRANSMATERIALES SA', 'CUCUTA MOTORS', 'IMPORTADORA FERRETERA BEF', 'PROYECFORMAS SAS', 'COACREMAT'],
        'Correo Empresa': ['asistentesgi@jucamal.com', 'Sgsst.cootransmeta01@gmail.co', 'asistentesgi@jucamal.com', 'sarc1384@gmail.com', 'saludocupacional@transmateria', 'anyely.arias@cucutamotors.con', 'imporberaca05@gmail.com', 'karol.moreno@proyecformas.cc', 'control.personal@coacremat.co'],
        'Teléfono Em': ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
        'Ciudad': ['VIRTUAL', 'VIRTUAL', 'VIRTUAL', 'VIRTUAL', 'VIRTUAL', 'VIRTUAL', 'VIRTUAL', 'VIRTUAL', 'VIRTUAL'],
        'Fecha': ['2025-02-18 00:00:00', '2025-02-18 00:00:00', '2025-02-18 00:00:00', '2025-02-18 00:00:00', '2025-02-18 00:00:00', '2025-02-21 00:00:00', '2025-02-21 00:00:00', '2025-02-21 00:00:00', '2025-02-21 00:00:00'],
        'Módulo': ['Marco Legal', 'Marco Legal', 'Marco Legal', 'Marco Legal', 'Marco Legal', 'Sostenibilidad Empresarial', 'Sostenibilidad Empresarial', 'Sostenibilidad Empresarial', 'Sostenibilidad Empresarial'],
        'Tema': ['DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST', 'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST', 'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST', 'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST', 'DECRETO 1072 DEL 2015: BASE FUNDAMENTAL DEL SG-SST', 'FUNCIONES Y RESPONSABILIDADES', 'FUNCIONES Y RESPONSABILIDADES', 'FUNCIONES Y RESPONSABILIDADES', 'FUNCIONES Y RESPONSABILIDADES'],
        'Estado': ['Asistio', 'Asistio', 'Asistio', 'Asistio', 'Asistio', 'Asistio', 'Asistio', 'Asistio', 'Asistio']
    }
    
    return pd.DataFrame(data)

def test_numeric_generator_fix():
    """Probar la corrección del generador numérico"""
    print("🧪 PRUEBA DEL GENERADOR NUMÉRICO (CORREGIDO)")
    print("=" * 60)
    
    # Crear datos de prueba
    data = create_test_data()
    print(f"Datos de prueba creados: {len(data)} filas")
    print()
    
    # Mostrar grupos esperados
    print("📊 GRUPOS ESPERADOS:")
    print("Grupo 1 (Filas 1-5): Fecha=2025-02-18, Módulo=Marco Legal, Tema=DECRETO 1072...")
    print("Grupo 2 (Filas 6-9): Fecha=2025-02-21, Módulo=Sostenibilidad Empresarial, Tema=FUNCIONES Y RESPONSABILIDADES")
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
        numeric_grouping_columns=['Fecha', 'Tema', 'Módulo']
    )
    
    # Crear configuración de columna de fecha
    fecha_config = ColumnConfig(
        name='fecha',
        display_name='Fecha',
        source_column='Fecha',
        data_type=DataType.DATE,
        required=False,
        is_generated=False,
        format_string='dd/mm/yy'
    )
    
    # Probar generación de números
    print("📝 RESULTADOS DE LA GENERACIÓN:")
    print("-" * 60)
    
    generated_numbers = []
    formatted_dates = []
    
    for idx, row in data.iterrows():
        # Generar número
        number = export_manager._get_column_value(row, col_config, data)
        generated_numbers.append(number)
        
        # Formatear fecha
        fecha_value = export_manager._get_column_value(row, fecha_config, data)
        formatted_fecha = export_manager._format_value(fecha_value, fecha_config)
        formatted_dates.append(formatted_fecha)
        
        print(f"Fila {idx + 1}: {row['Nombres'][:20]}... -> Matrícula: {number}, Fecha: {formatted_fecha}")
    
    print()
    
    # Analizar resultados
    unique_numbers = set(generated_numbers)
    print("📈 ANÁLISIS DE RESULTADOS:")
    print(f"Total de filas: {len(data)}")
    print(f"Números únicos generados: {len(unique_numbers)}")
    print(f"Números generados: {sorted(unique_numbers)}")
    
    # Verificar si la agrupación es correcta
    if len(unique_numbers) == 2:
        print("✅ ÉXITO: Se generaron 2 números diferentes para 2 grupos diferentes")
    else:
        print(f"❌ ERROR: Se esperaban 2 grupos, pero se generaron {len(unique_numbers)} números únicos")
    
    print()
    
    # Verificar formato de fecha
    print("📅 ANÁLISIS DEL FORMATO DE FECHA:")
    unique_dates = set(formatted_dates)
    print(f"Fechas únicas formateadas: {unique_dates}")
    
    # Verificar que las fechas están en formato dd/mm/yy
    correct_format = True
    for date in unique_dates:
        if not isinstance(date, str) or not date.count('/') == 2:
            correct_format = False
            break
    
    if correct_format:
        print("✅ ÉXITO: Las fechas están formateadas correctamente en dd/mm/yy")
    else:
        print("❌ ERROR: Las fechas no están en el formato esperado")
    
    print()
    
    # Mostrar contadores del generador
    print("🔢 CONTADORES DEL GENERADOR:")
    for key, value in export_manager.numeric_generator.counters.items():
        print(f"  {key}: {value}")
    
    return len(unique_numbers) == 2 and correct_format

def main():
    """Función principal de pruebas"""
    print("🧪 PRUEBAS DE CORRECCIONES - Excel Builder Pro")
    print("=" * 60)
    
    # Probar correcciones
    test_passed = test_numeric_generator_fix()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE PRUEBAS")
    print("=" * 60)
    print(f"Prueba de correcciones: {'✅ PASÓ' if test_passed else '❌ FALLÓ'}")
    
    if test_passed:
        print("\n🎉 ¡TODAS LAS CORRECCIONES FUNCIONAN! Los problemas han sido resueltos.")
        print("✅ Generador numérico: Agrupa correctamente por columnas")
        print("✅ Formato de fecha: Se aplica correctamente")
    else:
        print("\n⚠️  Algunas correcciones fallaron. Revisar la implementación.")

if __name__ == "__main__":
    main()

