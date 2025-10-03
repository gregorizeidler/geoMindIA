// GeoMindIA - Frontend Application

const API_BASE_URL = 'http://localhost:8000';
let map;
let markers = [];
let polygons = [];
let heatmap = null;
let currentResults = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', async () => {
    initializeMap();
    await checkHealth();
    await loadSampleQueries();
    setupEventListeners();
    loadQueryHistory();
});

// Initialize Google Maps
function initializeMap() {
    // Porto Alegre coordinates
    const center = { lat: -30.0346, lng: -51.2177 };
    
    map = new google.maps.Map(document.getElementById('map'), {
        center: center,
        zoom: 12,
        styles: [
            {
                featureType: 'poi',
                elementType: 'labels',
                stylers: [{ visibility: 'off' }]
            }
        ],
        mapTypeControl: true,
        streetViewControl: false,
        fullscreenControl: true
    });
}

// Check API and services health
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const health = await response.json();
        
        updateStatusIndicator('api-status', health.api === 'healthy');
        updateStatusIndicator('db-status', health.database.includes('healthy'));
        updateStatusIndicator('llm-status', health.llm === 'healthy');
    } catch (error) {
        console.error('Health check failed:', error);
        updateStatusIndicator('api-status', false);
        updateStatusIndicator('db-status', false);
        updateStatusIndicator('llm-status', false);
    }
}

function updateStatusIndicator(id, healthy) {
    const element = document.getElementById(id);
    element.className = `status-dot ${healthy ? 'healthy' : 'unhealthy'}`;
}

// Load sample queries
async function loadSampleQueries() {
    try {
        const response = await fetch(`${API_BASE_URL}/sample-queries`);
        const data = await response.json();
        
        const container = document.getElementById('sample-queries');
        container.innerHTML = '';
        
        data.samples.forEach(category => {
            const categoryDiv = document.createElement('div');
            categoryDiv.className = 'sample-category';
            
            const categoryTitle = document.createElement('h4');
            categoryTitle.textContent = category.category;
            categoryDiv.appendChild(categoryTitle);
            
            category.queries.forEach(query => {
                const queryDiv = document.createElement('div');
                queryDiv.className = 'sample-query';
                queryDiv.textContent = query;
                queryDiv.onclick = () => useSampleQuery(query);
                categoryDiv.appendChild(queryDiv);
            });
            
            container.appendChild(categoryDiv);
        });
    } catch (error) {
        console.error('Failed to load sample queries:', error);
    }
}

// Setup event listeners
function setupEventListeners() {
    // Submit query
    document.getElementById('submit-query').addEventListener('click', submitQuery);
    
    // Enter key in textarea
    document.getElementById('query-input').addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
            submitQuery();
        }
    });
    
    // Clear map
    document.getElementById('clear-map').addEventListener('click', clearMap);
    
    // Visualization type change
    document.getElementById('visualization-type').addEventListener('change', (e) => {
        if (currentResults.length > 0) {
            visualizeResults(currentResults, e.target.value);
        }
    });
    
    // Collapsible sections
    document.getElementById('interpretation-header').addEventListener('click', () => {
        toggleCollapsible('interpretation-section');
    });
    
    document.getElementById('sql-header').addEventListener('click', () => {
        toggleCollapsible('sql-section');
    });
}

function toggleCollapsible(className) {
    const section = document.querySelector(`.${className}`);
    section.classList.toggle('collapsed');
}

// Use sample query
function useSampleQuery(query) {
    document.getElementById('query-input').value = query;
}

// Submit query
async function submitQuery() {
    const queryInput = document.getElementById('query-input');
    const query = queryInput.value.trim();
    
    if (!query) {
        alert('Please enter a query');
        return;
    }
    
    // Show loading
    showLoading(true);
    setSubmitButtonLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentResults = data.results;
            displayResults(data);
            visualizeResults(data.results, data.visualization_type);
            addToHistory(query);
            
            // Show interpretation and SQL
            document.getElementById('interpretation-text').textContent = data.interpretation;
            document.getElementById('sql-text').textContent = data.sql_query;
        } else {
            alert(`Query failed: ${data.error}`);
        }
    } catch (error) {
        console.error('Query failed:', error);
        alert('Failed to process query. Please check if the backend is running.');
    } finally {
        showLoading(false);
        setSubmitButtonLoading(false);
    }
}

function showLoading(show) {
    const overlay = document.getElementById('loading-overlay');
    if (show) {
        overlay.classList.remove('hidden');
    } else {
        overlay.classList.add('hidden');
    }
}

function setSubmitButtonLoading(loading) {
    const button = document.getElementById('submit-query');
    const text = document.getElementById('submit-text');
    const loader = document.getElementById('submit-loader');
    
    if (loading) {
        text.classList.add('hidden');
        loader.classList.remove('hidden');
        button.disabled = true;
    } else {
        text.classList.remove('hidden');
        loader.classList.add('hidden');
        button.disabled = false;
    }
}

// Display results
function displayResults(data) {
    const container = document.getElementById('results-container');
    container.innerHTML = '';
    
    if (!data.results || data.results.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>No results found</p></div>';
        return;
    }
    
    data.results.forEach((result, index) => {
        const resultDiv = document.createElement('div');
        resultDiv.className = 'result-item';
        resultDiv.onclick = () => focusOnResult(result, index);
        
        const title = document.createElement('h4');
        title.textContent = result.name || `Result ${index + 1}`;
        resultDiv.appendChild(title);
        
        const stats = document.createElement('div');
        stats.className = 'result-stats';
        
        // Dynamic stats based on available data
        const statsToShow = [
            { label: 'Score', value: result.score, suffix: '/100' },
            { label: 'Population', value: result.population?.toLocaleString() },
            { label: 'Density', value: result.density, suffix: '/km²' },
            { label: 'Young Population', value: result.young_population_pct, suffix: '%' }
        ].filter(stat => stat.value !== undefined);
        
        statsToShow.forEach(stat => {
            const statDiv = document.createElement('div');
            statDiv.className = 'stat';
            statDiv.innerHTML = `
                <span class="stat-label">${stat.label}</span>
                <span class="stat-value">${stat.value}${stat.suffix || ''}</span>
            `;
            stats.appendChild(statDiv);
        });
        
        resultDiv.appendChild(stats);
        container.appendChild(resultDiv);
    });
}

// Visualize results on map
function visualizeResults(results, type) {
    clearMap();
    
    if (!results || results.length === 0) return;
    
    switch (type) {
        case 'markers':
            visualizeAsMarkers(results);
            break;
        case 'heatmap':
            visualizeAsHeatmap(results);
            break;
        case 'polygons':
        default:
            visualizeAsPolygons(results);
            break;
    }
    
    // Fit bounds to show all results
    fitMapBounds(results);
}

function visualizeAsMarkers(results) {
    results.forEach((result, index) => {
        const position = result.center || getCenterFromGeometry(result.geometry);
        
        if (position) {
            const marker = new google.maps.Marker({
                position: position,
                map: map,
                title: result.name || `Result ${index + 1}`,
                label: {
                    text: `${index + 1}`,
                    color: 'white',
                    fontSize: '14px',
                    fontWeight: 'bold'
                },
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    scale: 20,
                    fillColor: getColorForScore(result.score),
                    fillOpacity: 0.8,
                    strokeColor: 'white',
                    strokeWeight: 2
                }
            });
            
            const infoWindow = new google.maps.InfoWindow({
                content: createInfoWindowContent(result, index)
            });
            
            marker.addListener('click', () => {
                infoWindow.open(map, marker);
            });
            
            markers.push(marker);
        }
    });
}

function visualizeAsPolygons(results) {
    results.forEach((result, index) => {
        if (result.geometry && result.geometry.type === 'Polygon') {
            const coords = result.geometry.coordinates[0].map(coord => ({
                lat: coord[1],
                lng: coord[0]
            }));
            
            const polygon = new google.maps.Polygon({
                paths: coords,
                strokeColor: getColorForScore(result.score),
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: getColorForScore(result.score),
                fillOpacity: 0.35,
                map: map
            });
            
            const infoWindow = new google.maps.InfoWindow({
                content: createInfoWindowContent(result, index),
                position: result.center || getCenterFromGeometry(result.geometry)
            });
            
            polygon.addListener('click', () => {
                infoWindow.open(map);
            });
            
            polygons.push(polygon);
        }
    });
}

function visualizeAsHeatmap(results) {
    const heatmapData = results.map(result => {
        const position = result.center || getCenterFromGeometry(result.geometry);
        return position ? new google.maps.LatLng(position.lat, position.lng) : null;
    }).filter(point => point !== null);
    
    heatmap = new google.maps.visualization.HeatmapLayer({
        data: heatmapData,
        map: map,
        radius: 50,
        opacity: 0.6
    });
}

function getCenterFromGeometry(geometry) {
    if (!geometry || !geometry.coordinates) return null;
    
    if (geometry.type === 'Point') {
        return { lat: geometry.coordinates[1], lng: geometry.coordinates[0] };
    } else if (geometry.type === 'Polygon') {
        const coords = geometry.coordinates[0];
        const sumLat = coords.reduce((sum, coord) => sum + coord[1], 0);
        const sumLng = coords.reduce((sum, coord) => sum + coord[0], 0);
        return {
            lat: sumLat / coords.length,
            lng: sumLng / coords.length
        };
    }
    
    return null;
}

function createInfoWindowContent(result, index) {
    return `
        <div style="padding: 10px; max-width: 250px;">
            <h3 style="margin: 0 0 10px 0; font-size: 16px;">${result.name || `Area ${index + 1}`}</h3>
            ${result.score ? `<p><strong>Score:</strong> ${result.score}/100</p>` : ''}
            ${result.population ? `<p><strong>Population:</strong> ${result.population.toLocaleString()}</p>` : ''}
            ${result.density ? `<p><strong>Density:</strong> ${result.density}/km²</p>` : ''}
            ${result.young_population_pct ? `<p><strong>Young Pop:</strong> ${result.young_population_pct}%</p>` : ''}
        </div>
    `;
}

function getColorForScore(score) {
    if (!score) return '#3b82f6';
    
    if (score >= 80) return '#10b981'; // Green
    if (score >= 60) return '#3b82f6'; // Blue
    if (score >= 40) return '#f59e0b'; // Yellow
    return '#ef4444'; // Red
}

function fitMapBounds(results) {
    const bounds = new google.maps.LatLngBounds();
    
    results.forEach(result => {
        const position = result.center || getCenterFromGeometry(result.geometry);
        if (position) {
            bounds.extend(position);
        }
    });
    
    map.fitBounds(bounds);
}

function focusOnResult(result, index) {
    const position = result.center || getCenterFromGeometry(result.geometry);
    
    if (position) {
        map.setCenter(position);
        map.setZoom(14);
        
        // Highlight the result
        document.querySelectorAll('.result-item').forEach((item, i) => {
            if (i === index) {
                item.classList.add('selected');
            } else {
                item.classList.remove('selected');
            }
        });
    }
}

function clearMap() {
    // Clear markers
    markers.forEach(marker => marker.setMap(null));
    markers = [];
    
    // Clear polygons
    polygons.forEach(polygon => polygon.setMap(null));
    polygons = [];
    
    // Clear heatmap
    if (heatmap) {
        heatmap.setMap(null);
        heatmap = null;
    }
}

// Query history management
function addToHistory(query) {
    let history = JSON.parse(localStorage.getItem('queryHistory') || '[]');
    history.unshift({
        query: query,
        timestamp: new Date().toISOString()
    });
    history = history.slice(0, 10); // Keep only last 10
    localStorage.setItem('queryHistory', JSON.stringify(history));
    loadQueryHistory();
}

function loadQueryHistory() {
    const history = JSON.parse(localStorage.getItem('queryHistory') || '[]');
    const container = document.getElementById('query-history');
    
    if (history.length === 0) {
        container.innerHTML = '<p class="empty-state">No queries yet</p>';
        return;
    }
    
    container.innerHTML = '';
    history.forEach(item => {
        const historyDiv = document.createElement('div');
        historyDiv.className = 'history-item';
        historyDiv.innerHTML = `
            <div>${item.query}</div>
            <div class="timestamp">${new Date(item.timestamp).toLocaleString()}</div>
        `;
        historyDiv.onclick = () => useSampleQuery(item.query);
        container.appendChild(historyDiv);
    });
}

// Periodic health check
setInterval(checkHealth, 30000); // Check every 30 seconds

