import os
import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

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
    return render_template("index.html")


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
