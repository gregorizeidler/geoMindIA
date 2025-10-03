// Advanced Features: Vision Analysis and Route Optimization
// Integrated into main GeoMindIA platform

let selectedLocation = null;
let waypoints = [];
let isochronePolygons = [];

// ========== TAB SWITCHING ==========

function setupTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.dataset.tab;
            
            // Update active states
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            button.classList.add('active');
            document.getElementById(`${tabName}-tab`).classList.add('active');
            
            // Update map interaction mode
            updateMapMode(tabName);
        });
    });
}

function updateMapMode(mode) {
    const mapInfo = document.getElementById('map-info');
    
    if (mode === 'vision') {
        mapInfo.classList.remove('hidden');
        mapInfo.innerHTML = '<p>👁️ Click on map to select location for vision analysis</p>';
        enableMapClickSelection();
    } else if (mode === 'routing') {
        mapInfo.classList.remove('hidden');
        mapInfo.innerHTML = '<p>📍 Click on map to set locations for routing</p>';
        enableMapClickSelection();
    } else {
        mapInfo.classList.add('hidden');
        disableMapClickSelection();
    }
}

// ========== MAP CLICK SELECTION ==========

let mapClickListener = null;

function enableMapClickSelection() {
    if (mapClickListener) return;
    
    mapClickListener = map.addListener('click', (event) => {
        const lat = event.latLng.lat();
        const lng = event.latLng.lng();
        
        selectedLocation = { lat, lng };
        
        // Add temporary marker
        const marker = new google.maps.Marker({
            position: { lat, lng },
            map: map,
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 10,
                fillColor: '#ef4444',
                fillOpacity: 0.8,
                strokeColor: 'white',
                strokeWeight: 2
            },
            title: 'Selected Location'
        });
        
        // Check which tab is active
        const activeTab = document.querySelector('.tab-button.active').dataset.tab;
        
        if (activeTab === 'routing') {
            const feature = document.getElementById('routing-feature').value;
            if (feature === 'optimize') {
                addWaypoint({ lat, lng }, marker);
            }
        }
    });
}

function disableMapClickSelection() {
    if (mapClickListener) {
        google.maps.event.removeListener(mapClickListener);
        mapClickListener = null;
    }
    selectedLocation = null;
}

// ========== VISION ANALYSIS ==========

async function analyzeVision() {
    if (!selectedLocation) {
        alert('Please click on the map to select a location first');
        return;
    }
    
    const analysisType = document.getElementById('vision-analysis-type').value;
    const viewType = document.getElementById('vision-view-type').value;
    
    showLoading(true);
    
    try {
        const endpoint = viewType === 'satellite' ? 
            '/analyze/satellite' : '/analyze/streetview';
        
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                lat: selectedLocation.lat,
                lng: selectedLocation.lng,
                analysis_type: analysisType,
                zoom: 18,
                heading: 0,
                analysis_focus: analysisType
            })
        });
        
        const result = await response.json();
        displayVisionResults(result);
        
    } catch (error) {
        console.error('Vision analysis failed:', error);
        alert('Failed to analyze. Check if backend is running.');
    } finally {
        showLoading(false);
    }
}

function displayVisionResults(result) {
    const resultsDiv = document.getElementById('vision-results');
    const imageDiv = document.getElementById('vision-image');
    const insightsDiv = document.getElementById('vision-insights');
    
    resultsDiv.classList.remove('hidden');
    
    // Display image
    imageDiv.innerHTML = `
        <img src="${result.image_url}" alt="Analysis Image" style="width: 100%; border-radius: 8px;">
        <p class="image-caption">Location: ${result.location.lat.toFixed(4)}, ${result.location.lng.toFixed(4)}</p>
    `;
    
    // Display insights
    insightsDiv.innerHTML = `
        <div class="insight-box">
            <h4>AI Analysis</h4>
            <pre style="white-space: pre-wrap; font-size: 0.9rem;">${result.insights}</pre>
            ${result.mock ? '<p class="warning">⚠️ Mock data - Enable Gemini API for real analysis</p>' : ''}
        </div>
    `;
    
    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ========== ISOCHRONE MAPS ==========

async function calculateIsochrone() {
    if (!selectedLocation) {
        alert('Please click on the map to select a center point first');
        return;
    }
    
    const duration = parseInt(document.getElementById('isochrone-duration').value);
    const mode = document.getElementById('isochrone-mode').value;
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/routing/isochrone`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                center: selectedLocation,
                duration_minutes: duration,
                mode: mode,
                intervals: [duration / 3, duration * 2 / 3, duration]
            })
        });
        
        const result = await response.json();
        displayIsochrone(result);
        
    } catch (error) {
        console.error('Isochrone calculation failed:', error);
        alert('Failed to calculate. Check if backend is running.');
    } finally {
        showLoading(false);
    }
}

function displayIsochrone(result) {
    // Clear previous isochrones
    isochronePolygons.forEach(poly => poly.setMap(null));
    isochronePolygons = [];
    
    // Draw isochrone polygons
    result.isochrones.forEach(iso => {
        const polygon = new google.maps.Polygon({
            paths: iso.polygon.map(coord => ({ lat: coord[1], lng: coord[0] })),
            strokeColor: iso.color,
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: iso.color,
            fillOpacity: 0.25,
            map: map
        });
        
        isochronePolygons.push(polygon);
        
        // Add info window
        const infoWindow = new google.maps.InfoWindow({
            content: `<div style="padding: 10px;">
                <strong>${iso.duration_minutes} minutes</strong><br>
                Reachable area by ${result.mode}
            </div>`,
            position: result.center
        });
        
        polygon.addListener('click', () => {
            infoWindow.open(map);
        });
    });
    
    // Add center marker
    new google.maps.Marker({
        position: result.center,
        map: map,
        icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 15,
            fillColor: '#2563eb',
            fillOpacity: 1,
            strokeColor: 'white',
            strokeWeight: 3
        },
        title: 'Center Point'
    });
    
    // Show results
    document.getElementById('routing-results').innerHTML = `
        <div class="result-box success">
            <h3>Isochrone Map Generated</h3>
            <p><strong>Mode:</strong> ${result.mode}</p>
            <p><strong>Max Duration:</strong> ${result.max_duration_minutes} minutes</p>
            <p><strong>Intervals:</strong> ${result.isochrones.length} zones calculated</p>
            ${result.mock ? '<p class="warning">⚠️ Mock data - Enable Google Maps API for accurate calculations</p>' : ''}
        </div>
    `;
}

// ========== ACCESSIBILITY ANALYSIS ==========

async function calculateAccessibility() {
    if (!selectedLocation) {
        alert('Please click on the map to select a location first');
        return;
    }
    
    // Get selected POI types
    const checkboxes = document.querySelectorAll('#accessibility-controls input[type="checkbox"]:checked');
    const poiTypes = Array.from(checkboxes).map(cb => cb.value);
    
    if (poiTypes.length === 0) {
        alert('Please select at least one amenity type');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/routing/accessibility`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                location: selectedLocation,
                poi_types: poiTypes,
                max_duration_minutes: 15
            })
        });
        
        const result = await response.json();
        displayAccessibility(result);
        
    } catch (error) {
        console.error('Accessibility analysis failed:', error);
        alert('Failed to calculate. Check if backend is running.');
    } finally {
        showLoading(false);
    }
}

function displayAccessibility(result) {
    let html = `
        <div class="result-box success">
            <h3>Accessibility Score: ${result.overall_score}/10</h3>
            <div class="accessibility-scores">
    `;
    
    for (const [type, score] of Object.entries(result.accessibility_scores)) {
        const icon = score.accessible ? '✅' : '❌';
        html += `
            <div class="accessibility-item">
                ${icon} <strong>${score.name}:</strong> 
                ${score.duration_minutes} min walk (Score: ${score.score}/10)
            </div>
        `;
        
        // Add marker for each POI
        new google.maps.Marker({
            position: score.location,
            map: map,
            title: score.name,
            icon: {
                url: `http://maps.google.com/mapfiles/ms/icons/${score.accessible ? 'green' : 'red'}-dot.png`
            }
        });
    }
    
    html += `
            </div>
            ${result.mock ? '<p class="warning">⚠️ Mock data - Enable Google Maps API for real analysis</p>' : ''}
        </div>
    `;
    
    document.getElementById('routing-results').innerHTML = html;
}

// ========== ROUTE OPTIMIZATION ==========

function addWaypoint(location, marker) {
    waypoints.push({ location, marker });
    updateWaypointList();
}

function updateWaypointList() {
    const list = document.getElementById('waypoint-list');
    list.innerHTML = waypoints.map((wp, i) => `
        <div class="waypoint-item">
            <span>📍 Point ${i + 1}: ${wp.location.lat.toFixed(4)}, ${wp.location.lng.toFixed(4)}</span>
            <button onclick="removeWaypoint(${i})" class="remove-btn">×</button>
        </div>
    `).join('');
}

function removeWaypoint(index) {
    waypoints[index].marker.setMap(null);
    waypoints.splice(index, 1);
    updateWaypointList();
}

function clearWaypoints() {
    waypoints.forEach(wp => wp.marker.setMap(null));
    waypoints = [];
    updateWaypointList();
}

async function optimizeRoute() {
    if (waypoints.length < 2) {
        alert('Please add at least 2 waypoints on the map');
        return;
    }
    
    const locations = waypoints.map(wp => wp.location);
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/routing/optimize`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                origin: locations[0],
                destination: locations[locations.length - 1],
                waypoints: locations.slice(1, -1),
                mode: 'driving'
            })
        });
        
        const result = await response.json();
        displayOptimizedRoute(result);
        
    } catch (error) {
        console.error('Route optimization failed:', error);
        alert('Failed to optimize. Check if backend is running.');
    } finally {
        showLoading(false);
    }
}

function displayOptimizedRoute(result) {
    document.getElementById('routing-results').innerHTML = `
        <div class="result-box success">
            <h3>Optimized Route</h3>
            <p><strong>Total Distance:</strong> ${result.total_distance_km} km</p>
            <p><strong>Total Duration:</strong> ${result.total_duration_minutes} minutes</p>
            <p><strong>Waypoints:</strong> ${result.waypoints.length}</p>
            <p><strong>Optimized Order:</strong> ${result.optimized_order.join(' → ')}</p>
            ${result.mock ? '<p class="warning">⚠️ Mock data - Enable Google Maps API for real optimization</p>' : ''}
        </div>
    `;
}

// ========== ROUTING FEATURE SWITCHING ==========

function setupRoutingControls() {
    const featureSelect = document.getElementById('routing-feature');
    
    featureSelect.addEventListener('change', () => {
        // Hide all feature controls
        document.querySelectorAll('.feature-controls').forEach(el => el.classList.add('hidden'));
        
        // Show selected feature controls
        const feature = featureSelect.value;
        document.getElementById(`${feature}-controls`).classList.remove('hidden');
    });
}

// ========== EVENT LISTENERS ==========

function setupAdvancedFeatureListeners() {
    // Vision analysis
    document.getElementById('analyze-vision')?.addEventListener('click', analyzeVision);
    
    // Isochrone
    document.getElementById('calculate-isochrone')?.addEventListener('click', calculateIsochrone);
    
    // Accessibility
    document.getElementById('calculate-accessibility')?.addEventListener('click', calculateAccessibility);
    
    // Route optimization
    document.getElementById('clear-waypoints')?.addEventListener('click', clearWaypoints);
    document.getElementById('optimize-route')?.addEventListener('click', optimizeRoute);
    
    // Setup tabs and routing controls
    setupTabs();
    setupRoutingControls();
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupAdvancedFeatureListeners);
} else {
    setupAdvancedFeatureListeners();
}

