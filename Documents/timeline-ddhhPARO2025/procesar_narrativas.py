import pandas as pd
import json
from datetime import datetime
from collections import Counter

print("=" * 60)
print("PROCESAMIENTO DE NARRATIVAS 2025")
print("=" * 60)

# 1. Cargar CSV de narrativas
print("\n1. Cargando narrativa2025.csv...")
df_narrativas = pd.read_csv('narrativa2025.csv', encoding='utf-8')

print(f"   - Total registros: {len(df_narrativas)}")
print(f"   - Columnas: {list(df_narrativas.columns)}")

# 2. Limpiar datos
print("\n2. Limpiando datos...")

# Renombrar columnas para facilitar manejo
df_narrativas.columns = ['index', 'cuenta', 'fecha', 'enlace', 'texto', 'lugar', 'idea_fuerza']

# Eliminar filas sin fecha o texto
df_narrativas = df_narrativas.dropna(subset=['fecha', 'texto'])

# Limpiar espacios
df_narrativas['cuenta'] = df_narrativas['cuenta'].str.strip()
df_narrativas['lugar'] = df_narrativas['lugar'].str.strip()
df_narrativas['idea_fuerza'] = df_narrativas['idea_fuerza'].str.strip()

print(f"   - Registros válidos: {len(df_narrativas)}")

# 3. Convertir fechas
print("\n3. Procesando fechas...")

def convertir_fecha(fecha_str):
    try:
        # Formato: 15/9/2025
        return datetime.strptime(fecha_str, '%d/%m/%Y').strftime('%Y-%m-%d')
    except:
        try:
            return datetime.strptime(fecha_str, '%d/%m/%y').strftime('%Y-%m-%d')
        except:
            return None

df_narrativas['fecha_iso'] = df_narrativas['fecha'].apply(convertir_fecha)
df_narrativas = df_narrativas.dropna(subset=['fecha_iso'])

print(f"   - Fechas convertidas: {len(df_narrativas)}")

# 4. Análisis de cuentas
print("\n4. Analizando narrativas por cuenta...")
cuentas = df_narrativas['cuenta'].value_counts()
print("\nNarrativas por cuenta:")
for cuenta, total in cuentas.items():
    print(f"   - {cuenta}: {total} narrativas")

# 5. Crear pares de comparación
print("\n5. Creando comparaciones narrativa oficial vs realidad...")

# Cargar datos procesados (realidad documentada)
with open('datos_procesados.json', 'r', encoding='utf-8') as f:
    datos_realidad = json.load(f)

comparaciones = []

# Agrupar narrativas por fecha
narrativas_por_fecha = {}
for _, row in df_narrativas.iterrows():
    fecha = row['fecha_iso']
    if fecha not in narrativas_por_fecha:
        narrativas_por_fecha[fecha] = []

    narrativas_por_fecha[fecha].append({
        'cuenta': row['cuenta'],
        'texto': row['texto'][:300] + '...' if len(str(row['texto'])) > 300 else row['texto'],
        'lugar': row['lugar'],
        'idea_fuerza': row['idea_fuerza'],
        'enlace': row['enlace']
    })

# Crear comparaciones con eventos documentados
for evento in datos_realidad['eventos']:
    fecha_evento = evento['date']

    # Buscar narrativas oficiales de esa fecha
    narrativas_fecha = narrativas_por_fecha.get(fecha_evento, [])

    # Si hay narrativas oficiales para esa fecha, crear comparación
    if narrativas_fecha:
        # Tomar la narrativa oficial más relevante (primera de gobierno/FFAA)
        narrativa_oficial = None
        for narr in narrativas_fecha:
            if narr['cuenta'] in ['FFAA', 'Gobierno', 'PoliciaNacional']:
                narrativa_oficial = narr
                break

        if not narrativa_oficial and narrativas_fecha:
            narrativa_oficial = narrativas_fecha[0]

        if narrativa_oficial:
            comparacion = {
                'fecha': fecha_evento,
                'dia': evento['day'],
                'lugar': evento['location'],
                'narrativa_oficial': {
                    'cuenta': narrativa_oficial['cuenta'],
                    'texto': narrativa_oficial['texto'],
                    'idea_fuerza': narrativa_oficial['idea_fuerza'],
                    'fuente': narrativa_oficial['enlace']
                },
                'realidad_documentada': {
                    'titulo': evento['title'],
                    'resumen': evento['summary'],
                    'categoria': evento['category'],
                    'violaciones': evento.get('violations', [])
                }
            }
            comparaciones.append(comparacion)

print(f"\n   - Comparaciones creadas: {len(comparaciones)}")

# 6. Crear datos adicionales de narrativas
print("\n6. Generando estadísticas de narrativas...")

# Top ideas fuerza
ideas_fuerza = df_narrativas['idea_fuerza'].value_counts().head(10)
top_ideas = [{'idea': idea, 'total': int(total)} for idea, total in ideas_fuerza.items()]

# Narrativas por lugar
lugares = df_narrativas['lugar'].value_counts().head(10)
top_lugares = [{'lugar': lugar, 'total': int(total)} for lugar, total in lugares.items()]

# 7. Generar JSON final
print("\n7. Generando narrativas_procesadas.json...")

output = {
    'metadata': {
        'generado': datetime.now().isoformat(),
        'version': '1.0',
        'fuente': 'narrativa2025.csv',
        'total_narrativas': len(df_narrativas),
        'total_comparaciones': len(comparaciones)
    },
    'estadisticas': {
        'por_cuenta': {cuenta: int(total) for cuenta, total in cuentas.items()},
        'top_ideas_fuerza': top_ideas,
        'top_lugares': top_lugares
    },
    'comparaciones': comparaciones,
    'todas_narrativas': narrativas_por_fecha
}

with open('narrativas_procesadas.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("   - Archivo creado exitosamente!")

# 8. Resumen final
print("\n" + "=" * 60)
print("RESUMEN FINAL")
print("=" * 60)
print(f"\nTotal narrativas procesadas: {len(df_narrativas)}")
print(f"Total comparaciones creadas: {len(comparaciones)}")
print(f"\nCuentas analizadas:")
for cuenta, total in cuentas.items():
    print(f"   - {cuenta}: {total}")
print(f"\nTop 5 ideas fuerza:")
for i, item in enumerate(top_ideas[:5], 1):
    print(f"   {i}. {item['idea']}: {item['total']}")

print("\n" + "=" * 60)
print("Archivo generado: narrativas_procesadas.json")
print("=" * 60)
