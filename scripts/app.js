// Elementy DOM
const countrySelect = document.getElementById('country-select');
const sectorSelect = document.getElementById('sector-select');
const gasSelect = document.getElementById('gas-select');
const chartCanvas = document.getElementById('emissionsChart');

// Wykres Chart.js
let emissionsChart;

// Ładowanie danych CSV
Papa.parse('data.csv', {
    download: true,
    header: true,
    complete: function (result) {
        const data = result.data;
        initializeFilters(data);
        createChart(data);
    }
});

// Inicjalizacja filtrów
function initializeFilters(data) {
    const countries = [...new Set(data.map(row => row.Country))];
    const sectors = [...new Set(data.map(row => row.Sector))];
    const gases = [...new Set(data.map(row => row.Gas))];

    populateSelect(countrySelect, countries);
    populateSelect(sectorSelect, sectors);
    populateSelect(gasSelect, gases);

    // Dodaj listener na zmiany w filtrach
    [countrySelect, sectorSelect, gasSelect].forEach(select => {
        select.addEventListener('change', () => updateChart(data));
    });
}

function populateSelect(select, options) {
    options.forEach(option => {
        const opt = document.createElement('option');
        opt.value = option;
        opt.textContent = option;
        select.appendChild(opt);
    });
}

// Tworzenie wykresu
function createChart(data) {
    const filteredData = filterData(data);
    const chartData = prepareChartData(filteredData);

    emissionsChart = new Chart(chartCanvas, {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top'
                }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Year' }
                },
                y: {
                    title: { display: true, text: 'Emissions (Mt CO2e)' }
                }
            }
        }
    });
}

// Aktualizacja wykresu
function updateChart(data) {
    const filteredData = filterData(data);
    const chartData = prepareChartData(filteredData);

    emissionsChart.data = chartData;
    emissionsChart.update();
}

// Filtracja danych
function filterData(data) {
    const country = countrySelect.value;
    const sector = sectorSelect.value;
    const gas = gasSelect.value;

    return data.filter(row =>
        (country === 'all' || row.Country === country) &&
        (sector === 'all' || row.Sector === sector) &&
        (gas === 'all' || row.Gas === gas)
    );
}

// Przygotowanie danych do Chart.js
function prepareChartData(data) {
    const years = Object.keys(data[0]).filter(key => !isNaN(key));
    const values = years.map(year =>
        data.reduce((sum, row) => sum + parseFloat(row[year] || 0), 0)
    );

    return {
        labels: years,
        datasets: [{
            label: 'Emissions (Mt CO2e)',
            data: values,
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2,
            fill: false
        }]
    };
}
