# Observatorio de Derechos Humanos Ecuador 🇪🇨

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![GitHub Pages](https://img.shields.io/badge/deployed-GitHub%20Pages-brightgreen)](https://dianamosquera.github.io/ObservatoriodeDDHH/)

Plataforma interactiva para la documentación y visualización de vulneraciones a derechos humanos durante el **Paro Nacional Ecuador 2025**.

## 📋 Descripción

Este observatorio documenta de manera rigurosa y transparente las presuntas vulneraciones a derechos humanos ocurridas durante el Paro Nacional convocado por la CONAIE (Confederación de Nacionalidades Indígenas del Ecuador) en septiembre-octubre de 2025, en protesta por el retiro del subsidio al diésel.

### Objetivos

- 🔍 **Documentar** eventos de manera verificable y sistemática
- 📊 **Visualizar** patrones y tendencias en las vulneraciones documentadas
- 🌐 **Hacer accesible** la información al público general
- ⚖️ **Contribuir** a la memoria histórica y la rendición de cuentas

## 🎯 Características

- **Visualizaciones Interactivas**: Gráficos dinámicos con D3.js v7
- **Cronología Detallada**: Timeline interactivo con todos los eventos documentados
- **Distribución Geográfica**: Mapa de eventos por provincia
- **Filtros por Categoría**: Anuncios, detenciones, represión, violencia, censura
- **Metodología Transparente**: Basada en estándares de CEDHU
- **Diseño Responsivo**: Optimizado para móviles y escritorio
- **Código Abierto**: Totalmente transparente y auditable

## 📊 Estadísticas

Al 15 de diciembre de 2025:

- **41 eventos documentados**
- **33+ días de paro nacional**
- **10+ ubicaciones afectadas**
- **5 categorías de vulneraciones**

## 🛠️ Tecnologías

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Visualizaciones**: D3.js v7
- **Tipografía**: Inter (sans-serif), Fraunces (serif)
- **Procesamiento de Datos**: Python 3.x, Pandas
- **Deployment**: GitHub Pages

## 📁 Estructura del Proyecto

```
ObservatoriodeDDHH/
├── index.html                # Aplicación web principal
├── datos_procesados.json     # Datos de eventos procesados
├── README.md                 # Este archivo
├── LICENSE                   # Licencia CC BY-SA 4.0
└── .gitignore               # Archivos ignorados por Git
```

## 🚀 Uso

### Ver la aplicación en línea

Visita: **[https://dianamosquera.github.io/ObservatoriodeDDHH/](https://dianamosquera.github.io/ObservatoriodeDDHH/)**

### Ejecutar localmente

1. Clona el repositorio:
```bash
git clone https://github.com/DianaMosquera/ObservatoriodeDDHH.git
cd ObservatoriodeDDHH
```

2. Abre `index.html` en tu navegador web, o usa un servidor local:

```bash
# Con Python 3
python -m http.server 8000

# O con Node.js
npx http-server
```

3. Navega a `http://localhost:8000`

## 📖 Metodología

Este observatorio utiliza la metodología desarrollada por la **Comisión Ecuménica de Derechos Humanos (CEDHU)** para la documentación de vulneraciones a derechos humanos en contextos de protesta social.

### Principios Fundamentales

1. ✅ **Verificación de fuentes múltiples** e independientes
2. ✅ **Registro de testimonios directos** cuando sea posible
3. ✅ **Análisis de documentación** oficial y periodística
4. ✅ **Respeto a la presunción de inocencia**
5. ✅ **Protección de identidades** de víctimas y testigos

### Fuentes de Información

- Medios de comunicación verificados
- Organizaciones de derechos humanos
- Testimonios directos
- Registros oficiales
- Documentación audiovisual georreferenciada

### Categorías de Vulneraciones

- **Anuncios**: Declaraciones oficiales y medidas gubernamentales
- **Detenciones**: Detenciones arbitrarias o irregulares
- **Represión**: Uso desproporcionado de la fuerza
- **Violencia**: Lesiones, agresiones físicas, amenazas
- **Censura**: Restricciones a libertad de expresión y comunicación

## 🤝 Contribuir

Este es un proyecto de documentación ciudadana. Si tienes información verificable sobre eventos no documentados:

1. Asegúrate de tener **fuentes verificables**
2. Incluye **fecha, ubicación y descripción detallada**
3. Protege la **identidad de víctimas y testigos**
4. Contacta: contacto@observatorio-ddhh.ec (correo ilustrativo)

### Para desarrolladores

1. Fork este repositorio
2. Crea una rama para tu feature (`git checkout -b feature/MiFeature`)
3. Commit tus cambios (`git commit -m 'Añadir MiFeature'`)
4. Push a la rama (`git push origin feature/MiFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.

Esto significa que puedes:
- ✅ **Compartir** — copiar y redistribuir el material
- ✅ **Adaptar** — remezclar, transformar y construir sobre el material

Bajo los siguientes términos:
- 📝 **Atribución** — Debes dar crédito apropiado
- 🔄 **Compartir Igual** — Si remezclas, debes distribuir bajo la misma licencia
- 🚫 **Sin restricciones adicionales** — No puedes aplicar términos legales que restrinjan lo que la licencia permite

Ver [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- **CEDHU** (Comisión Ecuménica de Derechos Humanos) - Metodología
- **CONAIE** (Confederación de Nacionalidades Indígenas del Ecuador) - Contexto
- **Diversa Studio** - Desarrollo técnico
- **Comunidades y defensores de DDHH** - Documentación sobre el terreno

## 📧 Contacto

- **Email**: contacto@observatorio-ddhh.ec (ilustrativo)
- **GitHub**: [@DianaMosquera](https://github.com/DianaMosquera)
- **Issues**: [Reportar un problema](https://github.com/DianaMosquera/ObservatoriodeDDHH/issues)

## ⚠️ Aviso Legal

Este observatorio documenta **presuntas vulneraciones** a derechos humanos con fines informativos y de memoria histórica. La inclusión de un evento no implica determinación de responsabilidad penal o civil. Se respeta la presunción de inocencia de todas las personas mencionadas.

---

**Última actualización**: Diciembre 2025
**Versión**: 2.0
**Eventos documentados**: 41

---

<p align="center">
  <strong>Por la memoria, la verdad y la justicia</strong><br>
  🕊️ Observatorio DDHH Ecuador 2025
</p>
