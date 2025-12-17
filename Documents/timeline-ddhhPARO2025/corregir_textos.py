# -*- coding: utf-8 -*-
"""
Script para corregir tildes y resumir textos largos
Observatorio DDHH Ecuador
"""

import json
import re

print("=" * 80)
print("CORRECCION DE TILDES Y RESUMEN DE TEXTOS")
print("=" * 80)

# 1. Leer JSON actual
print("\n1. Leyendo datos_procesados.json...")
with open('datos_procesados.json', 'r', encoding='utf-8') as f:
    datos = json.load(f)

print(f"   - Total eventos: {len(datos['eventos'])}")

# 2. Correcciones de tildes
print("\n2. Corrigiendo tildes...")

correcciones_tildes = {
    'represion': 'represión',
    'Represion': 'Represión',
    'violacion': 'violación',
    'Violacion': 'Violación',
    'manifestacion': 'manifestación',
    'Manifestacion': 'Manifestación',
    'detencion': 'detención',
    'Detencion': 'Detención',
    'nacion': 'nación',
    'Nacion': 'Nación',
    'organizacion': 'organización',
    'Organizacion': 'Organización'
}

tildes_corregidas = 0

for evento in datos['eventos']:
    # Corregir en título
    for sin_tilde, con_tilde in correcciones_tildes.items():
        if sin_tilde in evento['title']:
            evento['title'] = evento['title'].replace(sin_tilde, con_tilde)
            tildes_corregidas += 1
        if sin_tilde in evento['summary']:
            evento['summary'] = evento['summary'].replace(sin_tilde, con_tilde)
            tildes_corregidas += 1

    # Corregir categoría
    if evento['category'] == 'represion':
        evento['category'] = 'represión'
        tildes_corregidas += 1

print(f"   - Correcciones realizadas: {tildes_corregidas}")

# 3. Actualizar categorías con tildes
if 'represion' in datos['estadisticas']['categorias']:
    datos['estadisticas']['categorias']['represión'] = datos['estadisticas']['categorias'].pop('represion')

# 4. Resumir textos muy largos (más de 600 caracteres)
print("\n3. Resumiendo textos largos...")

def resumir_texto(texto, max_chars=550):
    """Resumen inteligente: corta en punto más cercano"""
    if len(texto) <= max_chars:
        return texto

    # Buscar el último punto antes de max_chars
    texto_corto = texto[:max_chars]
    ultimo_punto = texto_corto.rfind('.')

    if ultimo_punto > 300:  # Si hay un punto razonable
        return texto[:ultimo_punto + 1]
    else:
        # Si no, buscar el primer punto después de 300 chars
        resto = texto[300:max_chars + 100]
        primer_punto = resto.find('.')
        if primer_punto != -1:
            return texto[:300 + primer_punto + 1]
        else:
            # Último recurso: cortar en max_chars
            return texto[:max_chars] + '...'

textos_resumidos = 0

for evento in datos['eventos']:
    longitud_original = len(evento['summary'])

    if longitud_original > 600:
        evento['summary'] = resumir_texto(evento['summary'])
        textos_resumidos += 1
        print(f"   - Evento '{evento['title'][:50]}...'")
        print(f"     {longitud_original} -> {len(evento['summary'])} caracteres")

print(f"\n   - Total textos resumidos: {textos_resumidos}")

# 5. Guardar JSON actualizado
print("\n4. Guardando datos_procesados.json actualizado...")

with open('datos_procesados.json', 'w', encoding='utf-8') as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)

print("   - Archivo guardado correctamente")

# 6. Resumen final
print("\n" + "=" * 80)
print("RESUMEN DE CAMBIOS")
print("=" * 80)
print(f"Tildes corregidas:     {tildes_corregidas}")
print(f"Textos resumidos:      {textos_resumidos}")
print(f"Total eventos:         {len(datos['eventos'])}")
print("\nCambios guardados en datos_procesados.json")
print("=" * 80)
