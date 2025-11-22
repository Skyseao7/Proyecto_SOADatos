const map = L.map('map').setView([-9.19, -75.01], 5);

L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '© OpenStreetMap'
}).addTo(map);

const markers = {
    "Lima": [-12.04, -77.04],
    "Arequipa": [-16.40, -71.53],
    "Cusco": [-13.53, -71.96],
    "Loreto": [-3.74, -73.25],
    "Piura": [-5.19, -80.63]
};

for (const [region, coords] of Object.entries(markers)) {
    L.marker(coords).addTo(map)
        .bindPopup(`<b>${region}</b><br>Click para ver datos`)
        .on('click', () => {
            document.getElementById('regionSelect').value = region;
            actualizarDashboard();
        });
}
let chartClimaInstance = null;
let chartSocialInstance = null;

async function actualizarDashboard() {
    const region = document.getElementById('regionSelect').value;
    
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/dashboard/${region}`);
        const data = await response.json();
        
        console.log("Datos recibidos:", data);

        // A. Actualizar KPIs (Tarjetas superiores)
        document.getElementById('tempValue').innerText = `${data.clima.temp} °C`;
        document.getElementById('pobValue').innerText = data.social.pob.toLocaleString();
        document.getElementById('pbiValue').innerText = `${data.social.pbi} %`;

        // B. Actualizar Tabla
        document.getElementById('tblClima').innerText = data.clima.estado;
        document.getElementById('tblViento').innerText = `${data.clima.velocidad_viento} km/h`;
        document.getElementById('tblSalud').innerText = `${data.social.hospitales} Hospitales`;

        // C. Actualizar Gráficos
        actualizarGraficos(data);
        
        // D. Mover mapa a la región
        if(markers[region]) {
            map.setView(markers[region], 8);
        }

    } catch (error) {
        console.error("Error conectando al sistema SOA:", error);
        alert("Error de conexión con el Backend. Revisa la consola.");
    }
}

function actualizarGraficos(data) {
    const ctxClima = document.getElementById('chartClima').getContext('2d');
    const ctxSocial = document.getElementById('chartSocial').getContext('2d');

    if (chartClimaInstance) chartClimaInstance.destroy();
    if (chartSocialInstance) chartSocialInstance.destroy();

    chartClimaInstance = new Chart(ctxClima, {
        type: 'bar',
        data: {
            labels: ['Temperatura Actual', 'Velocidad Viento'],
            datasets: [{
                label: `Condiciones en ${data.region}`,
                data: [data.clima.temp, data.clima.velocidad_viento],
                backgroundColor: ['#3c6e9b', '#1a4f8a']
            }]
        },
        options: { responsive: true, plugins: { title: { display: true, text: 'Variables Climáticas (Tiempo Real)' } } }
    });

    chartSocialInstance = new Chart(ctxSocial, {
        type: 'doughnut',
        data: {
            labels: ['Población', 'Resto del País'],
            datasets: [{
                data: [data.social.pob, 33000000 - data.social.pob],
                backgroundColor: ['#d32f2f', '#e0e0e0']
            }]
        },
        options: { responsive: true, plugins: { title: { display: true, text: 'Distribución Demográfica Nacional' } } }
    });
}

actualizarDashboard();