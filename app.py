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
        "descripcion_corta": "Captura y medición precisa de datos geoespaciales en campo mediante tecnología de posicionamiento y fotogrametría con drones.",
        "descripcion": (
            "La Sección de Levantamiento de Campo se encarga de la captura, medición y "
            "verificación de datos geoespaciales directamente en el terreno. Utiliza tecnología "
            "de vanguardia como sistemas GNSS de alta precisión, drones (RPA) y equipos "
            "topográficos para garantizar información confiable que soporte la toma de decisiones "
            "en el sector agropecuario nacional."
        ),
        "funciones": [
            {
                "titulo":      "Levantamiento Fotogramétrico con RPA",
                "descripcion": (
                    "Captura de imágenes aéreas mediante drones (Remotely Piloted Aircraft) "
                    "para la generación de ortofotomosaicos, modelos digitales de elevación y "
                    "análisis de superficie con alta precisión geométrica a escala de parcela y finca."
                ),
            },
            {
                "titulo":      "Red Geodésica de Puntos Conocidos",
                "descripcion": (
                    "Establecimiento y mantenimiento de la red de puntos de control geodésico "
                    "SIRGAS-CON, con coordenadas precisas en el marco de referencia geocéntrico "
                    "para Panamá. Estos puntos sirven de base para todos los levantamientos "
                    "ejecutados por OSIGA."
                ),
            },
            {
                "titulo":      "Características en Campo de Cultivos",
                "descripcion": (
                    "Determinación de parámetros agronómicos en campo: estado fenológico, "
                    "densidad de siembra, condición del cultivo y variables que inciden en el "
                    "desarrollo productivo, para alimentar los sistemas de información del sector."
                ),
            },
            {
                "titulo":      "Superficie Ocupada y Uso del Suelo",
                "descripcion": (
                    "Medición y delimitación de superficies agrícolas, determinación del uso "
                    "actual del suelo y estimación de áreas de producción para el seguimiento "
                    "estadístico del sector agropecuario nacional."
                ),
            },
        ],
    },
    {
        "slug":        "imagenes",
        "titulo":      "Imágenes Geoespaciales",
        "icono":       "satellite",
        "color":       "#1565c0",
        "descripcion_corta": "Adquisición, procesamiento y análisis de imágenes satelitales para el monitoreo continuo del territorio y los recursos agropecuarios.",
        "descripcion": (
            "La Sección de Imágenes Geoespaciales gestiona la adquisición y el procesamiento "
            "de imágenes de sensores remotos —satélites ópticos y radar— para el seguimiento "
            "de cultivos, la detección de eventos climáticos adversos y el desarrollo de "
            "plataformas de distribución de datos geoespaciales al servicio del agro panameño."
        ),
        "funciones": [
            {
                "titulo":      "Monitoreo Geoespacial por Sensores Remotos",
                "descripcion": (
                    "Seguimiento continuo del territorio nacional mediante imágenes satelitales "
                    "multiespectrales y de radar, integrando plataformas Sentinel, Landsat y MODIS "
                    "para el análisis de cobertura, uso del suelo y dinámica territorial."
                ),
            },
            {
                "titulo":      "Detección de Anomalías Climáticas",
                "descripcion": (
                    "Identificación y análisis de eventos climáticos adversos —sequías, inundaciones, "
                    "anomalías de temperatura— mediante series temporales de imágenes satelitales "
                    "combinadas con datos meteorológicos para alertas tempranas en el agro."
                ),
            },
            {
                "titulo":      "Índices Vegetativos en Cultivos",
                "descripcion": (
                    "Cálculo y seguimiento de índices espectrales (NDVI, EVI, SAVI) para evaluar "
                    "el estado, vigor y desarrollo de los cultivos estratégicos a escala regional, "
                    "brindando insumos para estimaciones de rendimiento y alertas fitosanitarias."
                ),
            },
            {
                "titulo":      "Plataformas de Datos Geoespaciales",
                "descripcion": (
                    "Diseño e implementación de plataformas para la distribución, visualización "
                    "y acceso a catálogos de imágenes y productos derivados del procesamiento "
                    "satelital, facilitando el uso de la información por parte de técnicos y "
                    "tomadores de decisiones."
                ),
            },
        ],
    },
    {
        "slug":        "analisis",
        "titulo":      "Análisis y Calidad",
        "icono":       "chart",
        "color":       "#e65100",
        "descripcion_corta": "Garantiza la integridad y exactitud de los datos geoespaciales, estableciendo estándares y generando informes técnicos para la toma de decisiones.",
        "descripcion": (
            "La Sección de Análisis y Calidad define los estándares que rigen la producción "
            "de información geoespacial en OSIGA y vela porque todos los productos cumplan "
            "criterios de exactitud, completitud y consistencia. Genera además informes "
            "analíticos que sustentan las políticas agropecuarias nacionales."
        ),
        "funciones": [
            {
                "titulo":      "Criterios de Calidad de Datos",
                "descripcion": (
                    "Definición y aplicación de normas y estándares de calidad para datos "
                    "geoespaciales, alineados con la norma ISO 19157 y las directrices del "
                    "marco nacional de información geográfica, garantizando datos confiables "
                    "y comparables a lo largo del tiempo."
                ),
            },
            {
                "titulo":      "Producción de Informes Técnicos",
                "descripcion": (
                    "Elaboración de reportes analíticos que sintetizan hallazgos geoespaciales "
                    "para sustentar la toma de decisiones en políticas agropecuarias, "
                    "planificación territorial, gestión de riesgos y declaratoria de emergencias."
                ),
            },
            {
                "titulo":      "Medición y Mejoramiento de la Calidad",
                "descripcion": (
                    "Implementación de procesos de control, medición de métricas de calidad "
                    "y mejora continua en la producción de información geoespacial, asegurando "
                    "que los datos generados por OSIGA sean oportunos, exactos y útiles para "
                    "los usuarios finales."
                ),
            },
        ],
    },
    {
        "slug":        "cartografia",
        "titulo":      "Cartografía",
        "icono":       "map",
        "color":       "#5d4037",
        "descripcion_corta": "Producción y revisión de cartografía temática del sector agropecuario, con levantamiento espacial para análisis y planificación del territorio.",
        "descripcion": (
            "La Sección de Cartografía se encarga de la producción, revisión y actualización "
            "de la cartografía temática del sector agropecuario panameño. Genera mapas de "
            "uso del suelo, cobertura, infraestructura y zonificación que orientan la "
            "planificación estratégica y la gestión territorial del MIDA."
        ),
        "funciones": [
            {
                "titulo":      "Revisión de Información Cartográfica",
                "descripcion": (
                    "Verificación, actualización y validación de datos cartográficos existentes, "
                    "asegurando la coherencia espacial y temática de los productos con las "
                    "fuentes oficiales del Instituto Geográfico Nacional Tommy Guardia y "
                    "organismos internacionales."
                ),
            },
            {
                "titulo":      "Elaboración de Mapas Temáticos",
                "descripcion": (
                    "Diseño y producción de cartografía temática sobre uso del suelo, cobertura "
                    "vegetal, aptitud agrícola, infraestructura agropecuaria y distribución de "
                    "cultivos a escala nacional, provincial y de cuenca."
                ),
            },
            {
                "titulo":      "Levantamiento de Polígonos Geoespaciales",
                "descripcion": (
                    "Digitalización y captura de polígonos de parcelas agrícolas, fincas y "
                    "unidades territoriales para el cálculo de superficies, perímetros y "
                    "análisis de distribución espacial que alimentan el catastro agropecuario."
                ),
            },
        ],
    },
    {
        "slug":        "administracion",
        "titulo":      "Administración de Base de Datos",
        "icono":       "database",
        "color":       "#1a3a5c",
        "descripcion_corta": "Diseño, mantenimiento y evolución tecnológica de los sistemas de información geoespacial de OSIGA, integrando IA y bases de datos espaciales.",
        "descripcion": (
            "La Sección de Administración de Base de Datos gestiona la infraestructura de "
            "datos geoespaciales de OSIGA, asegurando la disponibilidad, integridad y "
            "accesibilidad de la información. Lidera además el desarrollo tecnológico del "
            "portal web institucional y la integración de modelos de inteligencia artificial "
            "y agentes autónomos para la automatización de flujos de datos geoespaciales."
        ),
        "funciones": [
            {
                "titulo":      "Administración de Datos Geoespaciales",
                "descripcion": (
                    "Gestión integral de bases de datos espaciales, incluyendo modelado, "
                    "carga, mantenimiento, respaldo y control de versiones de la información "
                    "geoespacial institucional. Garantiza la disponibilidad y consistencia "
                    "de los datos para todas las secciones de OSIGA."
                ),
            },
            {
                "titulo":      "Desarrollo del Portal Web OSIGA",
                "descripcion": (
                    "Diseño e implementación del Portal Web OSIGA, plataforma de acceso "
                    "público a los datos geoespaciales del sector agropecuario. Incluye "
                    "el visor de la Red Geodésica, integración con KoboToolbox y la "
                    "arquitectura Flask/Leaflet sobre Render.com."
                ),
            },
            {
                "titulo":      "Tecnología con Modelos de IA",
                "descripcion": (
                    "Integración de modelos de inteligencia artificial para el análisis de "
                    "datos geoespaciales: clasificación de coberturas, detección de cambios, "
                    "predicción de rendimientos agrícolas y procesamiento automatizado de "
                    "imágenes satelitales con modelos de visión computacional."
                ),
            },
            {
                "titulo":      "Desarrollo de Agentes Inteligentes",
                "descripcion": (
                    "Construcción de agentes de IA especializados en la automatización de "
                    "flujos de datos geoespaciales, consultas inteligentes a bases de datos "
                    "espaciales y soporte a la toma de decisiones en tiempo real para "
                    "técnicos y gestores del sector agropecuario."
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
