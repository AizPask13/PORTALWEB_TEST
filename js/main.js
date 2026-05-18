// ── Datos: Red Geodésica OSIGA — SIRGAS-CON Época 2005.0 ────────────────────
const PUNTOS = [
  {
    id: 1,
    nombre:   "BOCAS",
    lat:       9.541495,
    lng:      -82.590638,
    lat_dms:  "9° 32' 29.38237\" N",
    lon_dms:  "82° 35' 26.29887\" W",
    altura:    14.907,
    x:         811207.135,
    y:        -6237968.955,
    z:         1050273.253,
    marco_ref: "SIRGAS-CON",
    epoca:     "2005.0",
    fecha:     "2026-05-06"
  },
  {
    id: 2,
    nombre:   "CEIAPE PC3",
    lat:       9.230777,
    lng:      -78.850730,
    lat_dms:  "9° 13' 50.79461\" N",
    lon_dms:  "78° 51' 2.62672\" W",
    altura:    211.334,
    x:         1217487.261,
    y:        -6177461.042,
    z:         1016398.149,
    marco_ref: "SIRGAS-CON",
    epoca:     "2005.0",
    fecha:     "2026-03-24"
  },
  {
    id: 3,
    nombre:   "CEIAPE 260324",
    lat:       9.205572,
    lng:      -78.840770,
    lat_dms:  "9° 12' 20.06007\" N",
    lon_dms:  "78° 50' 26.77411\" W",
    altura:    147.108,
    x:         1218635.158,
    y:        -6177625.262,
    z:         1013836.147,
    marco_ref: "SIRGAS-CON",
    epoca:     "2005.0",
    fecha:     "2026-03-24"
  },
  {
    id: 4,
    nombre:   "MIDA-UP",
    lat:       9.217065,
    lng:      -78.848868,
    lat_dms:  "9° 13' 1.43282\" N",
    lon_dms:  "78° 50' 55.92538\" W",
    altura:    38.176,
    x:         1217701.919,
    y:        -6177492.300,
    z:         1014873.432,
    marco_ref: "SIRGAS-CON",
    epoca:     "2005.0",
    fecha:     "2026-03-04"
  }
];

// ── Inicializar mapa ─────────────────────────────────────────────────────────
const map = L.map('map', { zoomControl: true });

const osmLayer = L.tileLayer(
  'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  { attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>', maxZoom: 19 }
);

const esriLayer = L.tileLayer(
  'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
  { attribution: 'Esri World Imagery', maxZoom: 19 }
);

const esriLabels = L.tileLayer(
  'https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}',
  { attribution: '', maxZoom: 19, opacity: 0.8 }
);

const satelliteGroup = L.layerGroup([esriLayer, esriLabels]);

osmLayer.addTo(map);

L.control.layers(
  { 'Mapa base (OSM)': osmLayer, 'Satélite (Esri)': satelliteGroup },
  {},
  { position: 'topright' }
).addTo(map);

// ── Icono personalizado ──────────────────────────────────────────────────────
function makeIcon(color, label) {
  return L.divIcon({
    className: '',
    html: `
      <div style="
        position:relative;
        width:32px; height:32px;
        background:${color};
        border:3px solid #fff;
        border-radius:50%;
        box-shadow:0 2px 8px rgba(0,0,0,0.40);
        display:flex; align-items:center; justify-content:center;
        font-size:11px; font-weight:800;
        color:#fff;
        font-family:'Segoe UI',sans-serif;
      ">${label}</div>
    `,
    iconSize:   [32, 32],
    iconAnchor: [16, 16],
    popupAnchor:[0, -18]
  });
}

const COLORS = ['#1565c0', '#2e7d32', '#e65100', '#6a1b9a'];

// ── Marcadores con popup ─────────────────────────────────────────────────────
const markers = {};

function fmt(n, dec) {
  return n.toLocaleString('es-PA', {
    minimumFractionDigits: dec,
    maximumFractionDigits: dec
  });
}

PUNTOS.forEach((p, i) => {
  const popup = `
    <div class="popup-wrap">
      <div class="popup-header">
        <div class="popup-header-dot"></div>
        ${p.nombre}
      </div>
      <table class="popup-table">
        <tr>
          <td class="attr-label">Latitud</td>
          <td class="attr-value">${p.lat_dms}</td>
        </tr>
        <tr>
          <td class="attr-label">Longitud</td>
          <td class="attr-value">${p.lon_dms}</td>
        </tr>
        <tr>
          <td class="attr-label">Lat. Decimal</td>
          <td class="attr-value">${fmt(p.lat, 6)}°</td>
        </tr>
        <tr>
          <td class="attr-label">Lon. Decimal</td>
          <td class="attr-value">${fmt(p.lng, 6)}°</td>
        </tr>
        <tr>
          <td class="attr-label">Altura Elip.</td>
          <td class="attr-value"><span class="popup-value-highlight">${fmt(p.altura, 3)} m</span></td>
        </tr>
        <tr>
          <td class="attr-label">X — ECEF</td>
          <td class="attr-value">${fmt(p.x, 3)} m</td>
        </tr>
        <tr>
          <td class="attr-label">Y — ECEF</td>
          <td class="attr-value">${fmt(p.y, 3)} m</td>
        </tr>
        <tr>
          <td class="attr-label">Z — ECEF</td>
          <td class="attr-value">${fmt(p.z, 3)} m</td>
        </tr>
        <tr>
          <td class="attr-label">Marco Ref.</td>
          <td class="attr-value"><span class="popup-badge">${p.marco_ref}</span></td>
        </tr>
        <tr>
          <td class="attr-label">Época</td>
          <td class="attr-value">${p.epoca}</td>
        </tr>
        <tr>
          <td class="attr-label">Fecha Obs.</td>
          <td class="attr-value">${p.fecha}</td>
        </tr>
      </table>
    </div>
  `;

  const marker = L.marker([p.lat, p.lng], { icon: makeIcon(COLORS[i], i + 1) })
    .bindPopup(popup, { maxWidth: 320, minWidth: 290 })
    .addTo(map);

  marker.bindTooltip(`<strong>${p.nombre}</strong><br>Alt: ${p.altura} m`, {
    direction: 'top',
    offset: [0, -18]
  });

  markers[p.id] = marker;
});

// Ajustar vista para mostrar todos los puntos
const bounds = PUNTOS.map(p => [p.lat, p.lng]);
map.fitBounds(bounds, { padding: [50, 50] });

// ── Tabla de puntos ──────────────────────────────────────────────────────────
const tbody = document.getElementById('table-body');
let activeRow = null;

PUNTOS.forEach((p, i) => {
  const tr = document.createElement('tr');
  tr.dataset.id = p.id;
  tr.innerHTML = `
    <td class="col-num">
      <span style="
        display:inline-block;
        width:20px; height:20px;
        background:${COLORS[i]};
        color:#fff; border-radius:50%;
        font-size:10px; font-weight:800;
        line-height:20px; text-align:center;
      ">${p.id}</span>
    </td>
    <td class="col-nombre">${p.nombre}</td>
    <td>${p.lat_dms}</td>
    <td>${p.lon_dms}</td>
    <td>${fmt(p.lat, 6)}</td>
    <td>${fmt(p.lng, 6)}</td>
    <td>${fmt(p.altura, 3)}</td>
    <td>${fmt(p.x, 3)}</td>
    <td>${fmt(p.y, 3)}</td>
    <td>${fmt(p.z, 3)}</td>
    <td class="col-ref"><span class="popup-badge">${p.marco_ref}</span></td>
    <td>${p.epoca}</td>
    <td>${p.fecha}</td>
  `;

  tr.addEventListener('click', () => {
    if (activeRow) activeRow.classList.remove('active-row');
    tr.classList.add('active-row');
    activeRow = tr;
    map.setView([p.lat, p.lng], 14);
    markers[p.id].openPopup();
    document.getElementById('map').scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  tbody.appendChild(tr);
});
