# -*- coding: utf-8 -*-
"""
Script de limpieza de datos - Observatorio DDHH Ecuador
Limpia datos2025.csv y genera version limpia para el dashboard
"""

import pandas as pd
import re
import json
from datetime import datetime

print("=" * 80)
print("LIMPIEZA DE DATOS - OBSERVATORIO DDHH ECUADOR")
print("=" * 80)

# 1. LEER DATOS ORIGINALES
print("\n1. Leyendo datos2025.csv...")
datos = pd.read_csv('datos2025.csv', encoding='utf-8')
print(f"   - Total de registros: {len(datos)}")

# 2. LIMPIAR COLUMNAS PRINCIPALES
print("\n2. Limpiando datos...")

# Columnas que se mantienen para el dashboard
columnas_dashboard = [
    'Fecha',
    'Dia',
    'Ubicación',
    'Evento',
    'Resumen narrativo',
    'Tipo de vulneración a DDHH\n(presunta vulneración)',
    'Fuente',
    'Fuente primaria',
    'Link'
]

# Crear dataframe limpio
datos_limpios = datos[columnas_dashboard].copy()

# Renombrar columnas para simplicidad
datos_limpios.columns = [
    'fecha',
    'dia',
    'ubicacion',
    'evento',
    'resumen',
    'tipo_vulneracion',
    'fuente',
    'fuente_primaria',
    'link'
]

# 3. ELIMINAR FILAS CON DATOS INCOMPLETOS CRITICOS
print("   - Eliminando filas sin fecha o ubicacion...")
datos_limpios = datos_limpios.dropna(subset=['fecha', 'ubicacion'])

# 4. LIMPIAR TEXTO DE RESUMENES
print("   - Limpiando resumenes narrativos...")

def limpiar_resumen(texto):
    """Limpia el texto del resumen"""
    if pd.isna(texto) or str(texto).strip() == '' or str(texto) == 'nan':
        return "[Resumen pendiente de completar]"

    texto = str(texto).strip()

    # Remover prefijo BN:
    if texto.startswith('BN:'):
        texto = texto[3:].strip()

    # Si contiene placeholders, marcar para revision manual
    if re.search(r'sofi|poner|TODO|PENDIENTE|agregar|completar', texto, re.IGNORECASE):
        # Intentar extraer lo que si esta completo
        partes = re.split(r'\(.*?sofi.*?\)|sofi.*', texto, flags=re.IGNORECASE)
        if len(partes) > 0 and len(partes[0].strip()) > 50:
            texto = partes[0].strip()
        else:
            texto = "[Resumen pendiente de completar - " + texto[:100] + "...]"

    return texto

datos_limpios['resumen'] = datos_limpios['resumen'].apply(limpiar_resumen)

# 5. LIMPIAR CAMPOS DE TEXTO
print("   - Limpiando eventos...")
datos_limpios['evento'] = datos_limpios['evento'].fillna('[Evento sin titulo]')
datos_limpios['evento'] = datos_limpios['evento'].apply(lambda x: str(x).strip())

print("   - Limpiando tipo de vulneracion...")
datos_limpios['tipo_vulneracion'] = datos_limpios['tipo_vulneracion'].fillna('No especificado')

print("   - Limpiando ubicaciones...")
datos_limpios['ubicacion'] = datos_limpios['ubicacion'].apply(lambda x: str(x).strip() if pd.notna(x) else 'No especificado')

# 6. ESTANDARIZAR FECHAS
print("   - Estandarizando fechas...")

def estandarizar_fecha(fecha):
    """Convierte fechas a formato YYYY-MM-DD"""
    if pd.isna(fecha):
        return None

    fecha_str = str(fecha).strip()

    # Ya esta en formato correcto
    if re.match(r'^\d{4}-\d{2}-\d{2}$', fecha_str):
        return fecha_str

    # Formato con barras
    if '/' in fecha_str:
        fecha_str = fecha_str.replace('/', '-')

    return fecha_str

datos_limpios['fecha'] = datos_limpios['fecha'].apply(estandarizar_fecha)

# 7. CATEGORIZAR AUTOMATICAMENTE
print("   - Categorizando eventos...")

def categorizar_evento(row):
    """Categoriza el evento basado en palabras clave"""
    texto = f"{row['evento']} {row['resumen']} {row['tipo_vulneracion']}".lower()

    if any(palabra in texto for palabra in ['anuncio', 'anuncia', 'declara', 'aprueba', 'gobierno decide']):
        return 'anuncio'
    elif any(palabra in texto for palabra in ['detenci', 'arrest', 'captur', 'prisi']):
        return 'detenciones'
    elif any(palabra in texto for palabra in ['represi', 'golpe', 'agresi', 'violenci policial']):
        return 'represion'
    elif any(palabra in texto for palabra in ['muert', 'fallec', 'ejecut', 'disparo', 'herid', 'lesion']):
        return 'violencia'
    elif any(palabra in texto for palabra in ['censura', 'suspendi', 'prohib', 'bloque']):
        return 'censura'
    else:
        return 'represion'  # categoria por defecto

datos_limpios['categoria'] = datos_limpios.apply(categorizar_evento, axis=1)

# 8. GUARDAR CSV LIMPIO
print("\n3. Guardando datos limpios...")
datos_limpios.to_csv('datos2025_limpio.csv', index=False, encoding='utf-8')
print(f"   - Archivo guardado: datos2025_limpio.csv")
print(f"   - Registros finales: {len(datos_limpios)}")

# 9. GENERAR JSON PARA EL DASHBOARD
print("\n4. Generando datos_procesados.json...")

eventos = []
for _, row in datos_limpios.iterrows():
    if pd.notna(row['fecha']) and pd.notna(row['ubicacion']):
        eventos.append({
            'date': row['fecha'],
            'day': str(row['dia']),
            'location': row['ubicacion'],
            'title': row['evento'],
            'summary': row['resumen'],
            'category': row['categoria'],
            'source': row['fuente'] if pd.notna(row['fuente']) else '',
            'link': row['link'] if pd.notna(row['link']) else ''
        })

# Calcular estadisticas
estadisticas = {
    'total_eventos': len(eventos),
    'dias_paro': len(datos_limpios['dia'].unique()),
    'categorias': datos_limpios['categoria'].value_counts().to_dict(),
    'ubicaciones': datos_limpios['ubicacion'].value_counts().to_dict()
}

datos_json = {
    'metadata': {
        'generado': datetime.now().isoformat(),
        'version': '2.1',
        'fuente': 'datos2025_limpio.csv'
    },
    'eventos': eventos,
    'estadisticas': estadisticas
}

with open('datos_procesados.json', 'w', encoding='utf-8') as f:
    json.dump(datos_json, f, ensure_ascii=False, indent=2)

print(f"   - Archivo JSON generado con {len(eventos)} eventos")

# 10. EXTRAER REFERENCIAS Y CITAS
print("\n5. Extrayendo referencias...")

referencias = []
ref_id = 1

for idx, row in datos_limpios.iterrows():
    if pd.notna(row['fuente']) and str(row['fuente']).strip() != '':
        ref = {
            'id': ref_id,
            'fecha_evento': row['fecha'],
            'ubicacion': row['ubicacion'],
            'fuente': row['fuente'],
            'fuente_primaria': row['fuente_primaria'] if pd.notna(row['fuente_primaria']) else '',
            'link': row['link'] if pd.notna(row['link']) else ''
        }
        referencias.append(ref)
        ref_id += 1

# Guardar referencias
with open('referencias.json', 'w', encoding='utf-8') as f:
    json.dump({
        'metadata': {
            'total_referencias': len(referencias),
            'generado': datetime.now().isoformat()
        },
        'referencias': referencias
    }, f, ensure_ascii=False, indent=2)

print(f"   - {len(referencias)} referencias extraidas y guardadas en referencias.json")

# 11. REPORTE FINAL
print("\n" + "=" * 80)
print("RESUMEN DE LIMPIEZA")
print("=" * 80)
print(f"Registros originales:     {len(datos)}")
print(f"Registros limpios:        {len(datos_limpios)}")
print(f"Registros eliminados:     {len(datos) - len(datos_limpios)}")
print(f"\nEventos por categoria:")
for cat, count in datos_limpios['categoria'].value_counts().items():
    print(f"  - {cat:15} {count}")
print(f"\nEventos por ubicacion:")
for ubi, count in datos_limpios['ubicacion'].value_counts().head(10).items():
    print(f"  - {ubi:15} {count}")
print("\n" + "=" * 80)
print("ARCHIVOS GENERADOS:")
print("=" * 80)
print("  1. datos2025_limpio.csv     - CSV limpio para respaldo")
print("  2. datos_procesados.json    - JSON para el dashboard")
print("  3. referencias.json         - Referencias y citas")
print("\nLimpieza completada exitosamente!")
print("=" * 80)
