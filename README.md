# Excel Builder Pro

## Descripción

Excel Builder Pro es una aplicación de escritorio desarrollada en Python con tkinter que permite procesar, transformar y exportar archivos Excel de manera avanzada. La aplicación ofrece una interfaz gráfica intuitiva para configurar columnas, generar números automáticos, mapear datos y exportar resultados en múltiples formatos.

## 🚀 Optimizaciones de Rendimiento

### Versión Optimizada para Archivos Grandes
- **Procesamiento en lotes**: Manejo eficiente de archivos con más de 10,000 filas
- **Sistema de cache**: Reducción significativa del tiempo de procesamiento
- **Logging optimizado**: Configuración inteligente para máximo rendimiento
- **Gestión de memoria**: Procesamiento eficiente sin saturar la RAM

### Mejoras de Rendimiento
- **Archivos pequeños (< 1,000 filas)**: 20-30% más rápido
- **Archivos medianos (1,000 - 10,000 filas)**: 40-60% más rápido  
- **Archivos grandes (> 10,000 filas)**: 60-80% más rápido


## Características Principales

### 🔧 Gestión de Archivos
- Carga y procesamiento de archivos Excel (.xlsx, .xls)
- Validación automática de estructura y contenido
- Soporte para múltiples hojas de cálculo
- Previsualización de datos en tiempo real

### 📊 Configuración de Columnas
- Selección flexible de columnas fuente
- Configuración de columnas de destino personalizadas
- Reordenamiento mediante drag & drop
- Validación de tipos de datos
- Formateo condicional

### 🔢 Generador Numérico Avanzado
- **Numeración Simple**: Secuencias básicas con incremento personalizable


### 🗺️ Mapeo Dinámico
- **Mapeo Simple**: Transformación directa de valores, trayendo datos dinamicos desde excels  pivotes


### 📤 Exportación Flexible
- Múltiples formatos: Excel (.xlsx), CSV, JSON
- Configuración de opciones de exportación
- Backup automático de archivos
- Ajuste automático de columnas
- Preservación de formato
- **División automática**: Archivos grandes se dividen automáticamente

### 🔧 Utilidades Avanzadas
- **División de archivos**: Divide archivos grandes en partes manejables antes del procesamiento
- **Eliminación de duplicados**: Identifica y elimina duplicados con criterios personalizables
- **Vista previa de duplicados**: Revisa duplicados antes de eliminarlos
- **Criterios flexibles**: Define múltiples columnas para identificar duplicados
- **Exportación de duplicados**: Exporta duplicados para revisión manual

## Instalación

### Requisitos del Sistema
- Python 3.8 o superior
- Windows 10/11 (recomendado)
- 4GB RAM mínimo
- 100MB espacio en disco

### Dependencias
```bash
pip install pandas openpyxl xlrd tkinter
```

### Instalación desde Código Fuente
```bash
# Clonar el repositorio
git clone https://github.com/wilcastell/excel-builder-pro.git
cd excel-builder-pro

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```

## Uso Básico

### 1. Cargar Archivo Excel
1. Ejecuta `python main.py`
2. En la pestaña "Archivo", haz clic en "Seleccionar Archivo"
3. Elige tu archivo Excel (.xlsx o .xls)
4. Selecciona la hoja de trabajo deseada
5. Revisa la previsualización de datos

### 2. Configurar Columnas
1. Ve a la pestaña "Columnas"
2. Selecciona las columnas fuente que deseas incluir
3. Configura las columnas de destino:
   - Nombre de la columna
   - Tipo de datos
   - Formato
   - Validaciones

### 3. Generar Números (Opcional)
1. En la pestaña "Numérico", elige el tipo de generación:
   - **Simple**: Para secuencias básicas
   - **Agrupado**: Para numeración por grupos
   - **Matrícula**: Para códigos académicos
2. Configura los parámetros según tus necesidades
3. Previsualiza el resultado

### 4. Configurar Mapeo (Opcional)
1. En la pestaña "Mapeo", selecciona el tipo:
   - **Simple**: Mapeo directo de valores
   - **Multi-columna**: Combinación de campos
2. Define las reglas de transformación
3. Verifica la previsualización

### 5. Exportar Resultados
1. Ve a la pestaña "Exportar"
2. Selecciona el formato de salida
3. Configura las opciones de exportación
4. Elige la ubicación del archivo
5. Haz clic en "Exportar"

## Arquitectura del Proyecto