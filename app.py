# =============================================================================
# Portal Web OSIGA — Backend Flask
# Oficina del Sistema de Información Geoespacial Agropecuaria
# Ministerio de Desarrollo Agropecuario · MIDA · Panamá
#
# Autor:      Manuel Ramos — Sección de Administración de Base de Datos
# GitHub:     https://github.com/AizPask13/PORTALWEB_TEST
# Licencia:   Uso institucional OSIGA / MIDA
# =============================================================================

import os
import requests
from flask import Flask, render_template, jsonify, abort

app = Flask(__name__)

# ── Secciones OSIGA ──────────────────────────────────────────────────────────
SECCIONES = [
    {
        "slug":        "levantamiento",
        "titulo":      "Levantamiento de Campo",
        "icono":       "gps",
        "color":       "#2e7d32",
        "descripcion_corta": "Captura y medición precisa de datos geoespaciales en campo mediante drones multiespectrales, GNSS de alta precisión y software fotogramétrico especializado.",
        "descripcion": (
            "La Sección de Levantamiento de Campo captura, mide y verifica datos geoespaciales "
            "directamente en el terreno utilizando drones RPA (DJI Mavic 3 Multiespectral) con "
            "antenas GNSS D-RTK2 para posicionamiento centimétrico. Los vuelos se procesan con "
            "Pix4D Field, Pix4D Mapper y Agisoft Metashape, generando ortofotomosaicos y modelos "
            "digitales de elevación de alta resolución que alimentan los análisis de toda la oficina."
        ),
        "herramientas": [
            "DJI Mavic 3 Multiespectral",
            "Antenas D-RTK2",
            "Pix4D Field",
            "Pix4D Mapper",
            "Agisoft Metashape",
            "GNSS SIRGAS-CON",
        ],
        "funciones": [
            {
                "titulo":      "Levantamiento Fotogramétrico con RPA",
                "descripcion": (
                    "Vuelos con drones DJI Mavic 3 Multiespectral —con estabilización por antenas "
                    "D-RTK2— para la captura de imágenes aéreas de alta precisión. Los datos se "
                    "procesan en Pix4D Mapper y Agisoft Metashape, generando ortofotomosaicos, "
                    "modelos digitales de superficie (DSM/DTM) y nubes de puntos 3D a escala de "
                    "parcela y finca."
                ),
            },
            {
                "titulo":      "Red Geodésica de Puntos Conocidos",
                "descripcion": (
                    "Establecimiento y mantenimiento de la red de puntos de control geodésico "
                    "SIRGAS-CON, procesados con Trimble RTX Post-Processing. Estos puntos de "
                    "coordenadas certificadas sirven de base de referencia para todos los "
                    "levantamientos ejecutados por OSIGA en el territorio nacional."
                ),
            },
            {
                "titulo":      "Características en Campo de Cultivos",
                "descripcion": (
                    "Determinación de parámetros agronómicos en campo mediante vuelos con cámara "
                    "multiespectral: estado fenológico, densidad de siembra, cobertura del dosel "
                    "y condiciones de estrés hídrico o fitosanitario. Los datos procesados en "
                    "Pix4D Field permiten mapas de variabilidad para la toma de decisiones."
                ),
            },
            {
                "titulo":      "Superficie Ocupada y Uso del Suelo",
                "descripcion": (
                    "Medición y delimitación de superficies agrícolas, determinación del uso "
                    "actual del suelo y estimación de áreas de producción. Los productos "
                    "fotogramétricos generados alimentan el catastro agropecuario y el "
                    "seguimiento estadístico del sector a escala nacional."
                ),
            },
        ],
    },
    {
        "slug":        "imagenes",
        "titulo":      "Imágenes Geoespaciales",
        "icono":       "satellite",
        "color":       "#1565c0",
        "descripcion_corta": "Monitoreo satelital del agro panameño con Google Earth Engine, SNAP Copernicus y datos NASA para índices vegetativos, anomalías climáticas y plataformas de visualización.",
        "descripcion": (
            "La Sección de Imágenes Geoespaciales adquiere, procesa y analiza imágenes de "
            "sensores remotos para el monitoreo continuo del territorio agropecuario. Trabaja "
            "con catálogos satelitales de Sentinel (Copernicus/ESA), Landsat y MODIS/NASA, "
            "procesados en Google Earth Engine y SNAP. Desarrolla aplicaciones de visualización "
            "geoespacial que ponen esta información al alcance de técnicos y tomadores de "
            "decisiones del sector agropecuario panameño."
        ),
        "herramientas": [
            "Google Earth Engine",
            "SNAP Copernicus",
            "Sentinel (ESA)",
            "Landsat (USGS)",
            "MODIS / NASA Earthdata",
        ],
        "funciones": [
            {
                "titulo":      "Monitoreo Geoespacial por Sensores Remotos",
                "descripcion": (
                    "Seguimiento continuo del territorio nacional mediante imágenes de Sentinel-2 "
                    "(óptico), Sentinel-1 (radar) y Landsat, procesadas en Google Earth Engine. "
                    "Permite análisis de cobertura, uso del suelo, dinámica territorial y "
                    "comparación de variables históricas a escala nacional."
                ),
            },
            {
                "titulo":      "Detección de Anomalías Climáticas",
                "descripcion": (
                    "Identificación de eventos adversos —sequías, inundaciones, anomalías de "
                    "temperatura— mediante series temporales satelitales y datos climáticos de "
                    "NASA Earthdata. Integrado en Google Earth Engine para alertas tempranas "
                    "que orientan la respuesta del sector agropecuario."
                ),
            },
            {
                "titulo":      "Índices Vegetativos en Cultivos",
                "descripcion": (
                    "Cálculo y seguimiento de índices espectrales (NDVI, EVI, SAVI, NDRE) "
                    "con imágenes Sentinel-2 y Landsat procesadas en GEE y SNAP. Evalúa el "
                    "vigor, estado y desarrollo de cultivos estratégicos, brindando insumos "
                    "para estimaciones de rendimiento y alertas fitosanitarias a escala regional."
                ),
            },
            {
                "titulo":      "Desarrollo de Plataformas de Visualización",
                "descripcion": (
                    "Construcción de aplicaciones web geoespaciales en Google Earth Engine "
                    "(GEE Apps) para la distribución interactiva de productos derivados del "
                    "procesamiento satelital: mapas de índices, series temporales y catálogos "
                    "de imágenes accesibles para técnicos del MIDA y actores del sector."
                ),
            },
        ],
    },
    {
        "slug":        "analisis",
        "titulo":      "Análisis y Calidad",
        "icono":       "chart",
        "color":       "#e65100",
        "descripcion_corta": "Control de calidad de ortomosaicos y productos fotogramétricos generados por Pix4D y Agisoft, con producción de informes técnicos para la toma de decisiones agropecuarias.",
        "descripcion": (
            "La Sección de Análisis y Calidad define los estándares que rigen todos los "
            "productos de OSIGA y verifica que los ortomosaicos, modelos digitales de elevación "
            "e índices generados por las plataformas fotogramétricas (Agisoft Metashape, Pix4D) "
            "cumplan criterios de exactitud geométrica y temática. Genera además informes "
            "analíticos que sustentan la toma de decisiones del MIDA y del sector agropecuario."
        ),
        "herramientas": [
            "Agisoft Metashape",
            "Pix4D Mapper",
            "Pix4D Field",
        ],
        "funciones": [
            {
                "titulo":      "Criterios de Calidad de Datos Geoespaciales",
                "descripcion": (
                    "Definición y aplicación de normas de calidad para datos geoespaciales "
                    "alineadas con ISO 19157. Establece los umbrales de error aceptable para "
                    "ortomosaicos y MDEs producidos por Agisoft y Pix4D, garantizando productos "
                    "comparables y confiables a lo largo del tiempo."
                ),
            },
            {
                "titulo":      "Evaluación de Productos Fotogramétricos",
                "descripcion": (
                    "Revisión y validación de los reportes de procesamiento generados por "
                    "Agisoft Metashape y Pix4D Mapper: análisis de error en puntos de control, "
                    "densidad de nube de puntos, resolución de ortofoto y exactitud posicional "
                    "de los modelos digitales de superficie."
                ),
            },
            {
                "titulo":      "Producción de Informes Técnicos",
                "descripcion": (
                    "Elaboración de reportes analíticos que sintetizan los hallazgos "
                    "geoespaciales para sustentar políticas agropecuarias, planificación "
                    "territorial, gestión de riesgos y evaluación de daños por eventos "
                    "climáticos, dirigidos a la alta dirección del MIDA."
                ),
            },
            {
                "titulo":      "Mejoramiento Continuo de la Calidad",
                "descripcion": (
                    "Implementación de procesos de control y mejora continua en la cadena "
                    "de producción de información geoespacial. Retroalimenta a las secciones "
                    "de Levantamiento e Imágenes con recomendaciones para optimizar la "
                    "precisión de los productos y reducir reprocesamientos."
                ),
            },
        ],
    },
    {
        "slug":        "cartografia",
        "titulo":      "Cartografía",
        "icono":       "map",
        "color":       "#5d4037",
        "descripcion_corta": "Producción y revisión de cartografía temática del sector agropecuario con QGIS, incluyendo mapas de uso del suelo, cobertura y levantamiento de polígonos de finca.",
        "descripcion": (
            "La Sección de Cartografía produce, revisa y actualiza la cartografía temática "
            "del sector agropecuario panameño utilizando QGIS como plataforma SIG principal. "
            "Genera mapas de uso del suelo, cobertura vegetal, infraestructura y zonificación "
            "agropecuaria, y ejecuta el levantamiento digital de polígonos de fincas y "
            "unidades territoriales que alimentan el catastro agropecuario del MIDA."
        ),
        "herramientas": [
            "QGIS",
        ],
        "funciones": [
            {
                "titulo":      "Revisión de Información Cartográfica",
                "descripcion": (
                    "Verificación, actualización y validación de capas cartográficas en QGIS, "
                    "asegurando coherencia espacial y temática con las fuentes del Instituto "
                    "Geográfico Nacional Tommy Guardia y organismos internacionales. Mantiene "
                    "la integridad topológica de los datos vectoriales y ráster institucionales."
                ),
            },
            {
                "titulo":      "Elaboración de Mapas Temáticos",
                "descripcion": (
                    "Diseño y producción de cartografía temática en QGIS sobre uso del suelo, "
                    "cobertura vegetal, aptitud agrícola, infraestructura agropecuaria y "
                    "distribución de cultivos a escalas nacional, provincial y de cuenca, "
                    "listos para publicación y consulta institucional."
                ),
            },
            {
                "titulo":      "Levantamiento de Polígonos Geoespaciales",
                "descripcion": (
                    "Digitalización y captura en QGIS de polígonos de parcelas agrícolas, "
                    "fincas y unidades territoriales. Los polígonos generados permiten calcular "
                    "superficies y perímetros precisos, ejecutar análisis de distribución "
                    "espacial y alimentar el catastro agropecuario del MIDA."
                ),
            },
        ],
    },
    {
        "slug":        "administracion",
        "titulo":      "Administración de Base de Datos",
        "icono":       "database",
        "color":       "#1a3a5c",
        "descripcion_corta": "Gestión integral de datos geoespaciales con PostgreSQL/PostGIS, KoboToolbox, Power BI, Machine Learning y Agentes de IA para brindar la información al MIDA para la toma de decisiones.",
        "descripcion": (
            "La Sección de Administración de Base de Datos es el eje tecnológico de OSIGA: "
            "administra la infraestructura de datos espaciales sobre PostgreSQL con las "
            "extensiones PostGIS y PGVector, integra formularios de campo vía KoboToolbox API, "
            "y centraliza toda la información generada por la oficina para garantizar su "
            "disponibilidad, integridad y trazabilidad. Automatiza flujos de trabajo con KNIME, "
            "visualiza indicadores en Power BI e integra modelos de Machine Learning (Random "
            "Forest, CNN) y Agentes de IA para apoyar la toma de decisiones del MIDA a favor "
            "del productor panameño."
        ),
        "herramientas": [
            "PostgreSQL",
            "PostGIS",
            "PGVector",
            "KoboToolbox",
            "Power BI",
            "KNIME",
            "Python",
            "Random Forest",
            "CNN",
        ],
        "funciones": [
            {
                "titulo":      "Administración de Datos Geoespaciales (PostgreSQL + PostGIS + PGVector)",
                "descripcion": (
                    "Gestión integral de la base de datos espacial sobre PostgreSQL con "
                    "extensiones PostGIS (análisis geoespacial SQL) y PGVector (embeddings "
                    "vectoriales para IA). Incluye modelado de esquemas, carga de capas, "
                    "respaldos, control de versiones y acceso centralizado a todos los datos "
                    "producidos por las secciones de OSIGA."
                ),
            },
            {
                "titulo":      "Gestión de Datos de Campo con KoboToolbox",
                "descripcion": (
                    "Diseño de Smart Forms en KoboToolbox para el registro estructurado de "
                    "datos agropecuarios en campo. Extracción automatizada vía API REST e "
                    "integración en la base de datos central, eliminando el papel y garantizando "
                    "trazabilidad desde el levantamiento hasta el análisis final."
                ),
            },
            {
                "titulo":      "Visualización con Business Intelligence (Power BI)",
                "descripcion": (
                    "Construcción de dashboards interactivos en Power BI que consolidan "
                    "indicadores geoespaciales, agrícolas y de calidad de datos de OSIGA. "
                    "Permite a la dirección del MIDA consultar el estado del sector "
                    "agropecuario en tiempo real con visualizaciones claras y accionables."
                ),
            },
            {
                "titulo":      "Machine Learning para Análisis Geoespacial",
                "descripcion": (
                    "Entrenamiento e implementación de modelos de clasificación y detección "
                    "con algoritmos de Machine Learning (Random Forest) y redes neuronales "
                    "convolucionales (CNN) aplicados a imágenes satelitales y fotogramétricas: "
                    "clasificación de coberturas, detección de áreas afectadas y estimación "
                    "de superficies de cultivo."
                ),
            },
            {
                "titulo":      "Automatización con KNIME y Agentes de IA",
                "descripcion": (
                    "Orquestación de flujos de trabajo ETL con KNIME para la integración "
                    "automática de datos entre fuentes heterogéneas (satélite, campo, cartografía). "
                    "Desarrollo de Agentes de IA y CLIs especializados que ejecutan consultas "
                    "inteligentes, generan reportes automáticos y reducen tiempos de análisis."
                ),
            },
        ],
    },
]

SECCIONES_MAP = {s["slug"]: s for s in SECCIONES}

# ── Paleta institucional (referencia) ────────────────────────────────────────
# AZUL_OSCURO = "#1a3a5c" | VERDE_MIDA = "#2e7d32" | AMARILLO = "#f9a825"

# ── Red Geodésica — SIRGAS-CON Época 2005.0 ─────────────────────────────────
PUNTOS_CONOCIDOS = [
    {
        "id": 1,
        "nombre":    "BOCAS",
        "lat":        9.541495,
        "lng":       -82.590638,
        "lat_dms":   "9° 32' 29.38237\" N",
        "lon_dms":   "82° 35' 26.29887\" W",
        "altura":     14.907,
        "x":          811207.135,
        "y":         -6237968.955,
        "z":          1050273.253,
        "marco_ref": "SIRGAS-CON",
        "epoca":     "2005.0",
        "fecha":     "2026-05-06",
    },
    {
        "id": 2,
        "nombre":    "CEIAPE PC3",
        "lat":        9.230777,
        "lng":       -78.850730,
        "lat_dms":   "9° 13' 50.79461\" N",
        "lon_dms":   "78° 51' 2.62672\" W",
        "altura":     211.334,
        "x":          1217487.261,
        "y":         -6177461.042,
        "z":          1016398.149,
        "marco_ref": "SIRGAS-CON",
        "epoca":     "2005.0",
        "fecha":     "2026-03-24",
    },
    {
        "id": 3,
        "nombre":    "CEIAPE 260324",
        "lat":        9.205572,
        "lng":       -78.840770,
        "lat_dms":   "9° 12' 20.06007\" N",
        "lon_dms":   "78° 50' 26.77411\" W",
        "altura":     147.108,
        "x":          1218635.158,
        "y":         -6177625.262,
        "z":          1013836.147,
        "marco_ref": "SIRGAS-CON",
        "epoca":     "2005.0",
        "fecha":     "2026-03-24",
    },
    {
        "id": 4,
        "nombre":    "MIDA-UP",
        "lat":        9.217065,
        "lng":       -78.848868,
        "lat_dms":   "9° 13' 1.43282\" N",
        "lon_dms":   "78° 50' 55.92538\" W",
        "altura":     38.176,
        "x":          1217701.919,
        "y":         -6177492.300,
        "z":          1014873.432,
        "marco_ref": "SIRGAS-CON",
        "epoca":     "2005.0",
        "fecha":     "2026-03-04",
    },
]

# ── KoboToolbox — variables de entorno (configurar en Render.com) ────────────
KOBO_TOKEN     = os.getenv("KOBO_TOKEN", "")
KOBO_ASSET_UID = os.getenv("KOBO_ASSET_UID", "")


# ── Rutas ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html", secciones=SECCIONES)


@app.route("/seccion/<slug>")
def seccion(slug):
    info = SECCIONES_MAP.get(slug)
    if not info:
        abort(404)
    return render_template("seccion.html", seccion=info, secciones=SECCIONES)


@app.route("/api/puntos")
def api_puntos():
    """Devuelve los puntos geodésicos de la Red OSIGA como JSON."""
    return jsonify(PUNTOS_CONOCIDOS)


@app.route("/api/kobo")
def api_kobo():
    """
    Proxy seguro a la API de KoboToolbox.
    El token nunca queda expuesto en el navegador.

    Configura en Render.com → Environment:
        KOBO_TOKEN     = tu token de KoboToolbox
        KOBO_ASSET_UID = UID del formulario/asset
    """
    if not KOBO_TOKEN or not KOBO_ASSET_UID:
        return jsonify({
            "status":  "no_configurado",
            "mensaje": "Define KOBO_TOKEN y KOBO_ASSET_UID en las variables de entorno.",
            "data":    [],
            "count":   0,
        })

    headers = {"Authorization": f"Token {KOBO_TOKEN}"}
    url = (
        f"https://kf.kobotoolbox.org/api/v2/assets/"
        f"{KOBO_ASSET_UID}/data/?format=json&limit=5000"
    )
    results = []
    while url:
        try:
            r = requests.get(url, headers=headers, timeout=30)
            r.raise_for_status()
        except requests.RequestException as exc:
            return jsonify({"status": "error", "error": str(exc), "data": [], "count": 0}), 502
        data = r.json()
        results.extend(data.get("results", []))
        url = data.get("next")

    return jsonify({"status": "ok", "data": results, "count": len(results)})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG") == "1")
