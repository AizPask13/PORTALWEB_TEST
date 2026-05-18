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
map.setView([9.0, -80.0], 7);

L.control.layers(
  { 'Mapa base (OSM)': osmLayer, 'Satélite (Esri)': satelliteGroup },
  {},
  { position: 'topright' }
).addTo(map);

// ── Helpers ──────────────────────────────────────────────────────────────────
const COLORS = ['#1565c0', '#2e7d32', '#e65100', '#6a1b9a'];

function fmt(n, dec) {
  return n.toLocaleString('es-PA', {
    minimumFractionDigits: dec,
    maximumFractionDigits: dec
  });
}

function makeIcon(color, label) {
  return L.divIcon({
    className: '',
    html: `<div style="
      width:32px; height:32px;
      background:${color};
      border:3px solid #fff;
      border-radius:50%;
      box-shadow:0 2px 8px rgba(0,0,0,0.40);
      display:flex; align-items:center; justify-content:center;
      font-size:11px; font-weight:800; color:#fff;
      font-family:'Segoe UI',sans-serif;
    ">${label}</div>`,
    iconSize:    [32, 32],
    iconAnchor:  [16, 16],
    popupAnchor: [0, -18]
  });
}

function buildPopup(p, color) {
  return `
    <div class="popup-wrap">
      <div class="popup-header">
        <div class="popup-header-dot"></div>
        ${p.nombre}
      </div>
      <table class="popup-table">
        <tr><td class="attr-label">Latitud</td>      <td class="attr-value">${p.lat_dms}</td></tr>
        <tr><td class="attr-label">Longitud</td>     <td class="attr-value">${p.lon_dms}</td></tr>
        <tr><td class="attr-label">Lat. Decimal</td> <td class="attr-value">${fmt(p.lat, 6)}°</td></tr>
        <tr><td class="attr-label">Lon. Decimal</td> <td class="attr-value">${fmt(p.lng, 6)}°</td></tr>
        <tr><td class="attr-label">Altura Elip.</td>
            <td class="attr-value"><span class="popup-value-highlight">${fmt(p.altura, 3)} m</span></td></tr>
        <tr><td class="attr-label">X — ECEF</td>    <td class="attr-value">${fmt(p.x, 3)} m</td></tr>
        <tr><td class="attr-label">Y — ECEF</td>    <td class="attr-value">${fmt(p.y, 3)} m</td></tr>
        <tr><td class="attr-label">Z — ECEF</td>    <td class="attr-value">${fmt(p.z, 3)} m</td></tr>
        <tr><td class="attr-label">Marco Ref.</td>
            <td class="attr-value"><span class="popup-badge">${p.marco_ref}</span></td></tr>
        <tr><td class="attr-label">Época</td>        <td class="attr-value">${p.epoca}</td></tr>
        <tr><td class="attr-label">Fecha Obs.</td>   <td class="attr-value">${p.fecha}</td></tr>
      </table>
    </div>`;
}

function buildTableRow(p, color) {
  return `
    <td class="col-num">
      <span style="
        display:inline-block; width:20px; height:20px;
        background:${color}; color:#fff; border-radius:50%;
        font-size:10px; font-weight:800; line-height:20px; text-align:center;
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
    <td>${p.fecha}</td>`;
}

// ── Cargar puntos desde Flask /api/puntos ────────────────────────────────────
fetch('/api/puntos')
  .then(res => res.json())
  .then(puntos => {
    const markers  = {};
    const tbody    = document.getElementById('table-body');
    let   activeRow = null;

    puntos.forEach((p, i) => {
      const color = COLORS[i] || '#1565c0';

      // Marcador en el mapa
      const marker = L.marker([p.lat, p.lng], { icon: makeIcon(color, i + 1) })
        .bindPopup(buildPopup(p, color), { maxWidth: 320, minWidth: 290 })
        .addTo(map);

      marker.bindTooltip(
        `<strong>${p.nombre}</strong><br>Alt: ${p.altura} m`,
        { direction: 'top', offset: [0, -18] }
      );

      markers[p.id] = marker;

      // Fila en la tabla
      const tr = document.createElement('tr');
      tr.dataset.id = p.id;
      tr.innerHTML  = buildTableRow(p, color);

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

    // Ajustar vista para incluir todos los puntos
    if (puntos.length > 0) {
      map.fitBounds(puntos.map(p => [p.lat, p.lng]), { padding: [50, 50] });
    }
  })
  .catch(err => {
    console.error('Error cargando puntos:', err);
    document.getElementById('table-body').innerHTML =
      `<tr><td colspan="13" style="text-align:center;color:#e53935;padding:20px;">
         Error al cargar los datos. Por favor recarga la página.
       </td></tr>`;
  });
