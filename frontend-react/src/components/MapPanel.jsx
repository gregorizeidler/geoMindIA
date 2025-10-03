import { useEffect, useRef } from 'react'
import { useAppStore } from '../store/appStore'
import { useGoogleMap } from '../hooks/useGoogleMap'
import './MapPanel.css'

const MapPanel = () => {
  const mapRef = useRef(null)
  const { 
    activeTab, 
    selectedLocation, 
    setSelectedLocation,
    queryResults,
    visualizationType,
    setVisualizationType,
    waypoints,
    addWaypoint,
    routingResults
  } = useAppStore()

  // Initialize and manage Google Map
  const { map, visualizeResults, clearMap } = useGoogleMap(mapRef, {
    center: { lat: -30.0346, lng: -51.2177 }, // Porto Alegre
    zoom: 12
  })

  // Handle map click for location selection
  useEffect(() => {
    if (!map) return

    const clickListener = map.addListener('click', (event) => {
      const lat = event.latLng.lat()
      const lng = event.latLng.lng()
      
      setSelectedLocation({ lat, lng })

      // Add marker for selected location
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
      })

      // Handle waypoint adding for routing
      if (activeTab === 'routing') {
        addWaypoint({ location: { lat, lng }, marker })
      }
    })

    return () => {
      google.maps.event.removeListener(clickListener)
    }
  }, [map, activeTab, setSelectedLocation, addWaypoint])

  // Visualize query results
  useEffect(() => {
    if (map && queryResults && queryResults.length > 0) {
      visualizeResults(queryResults, visualizationType)
    }
  }, [map, queryResults, visualizationType, visualizeResults])

  // Visualize routing results
  useEffect(() => {
    if (map && routingResults) {
      // Handle isochrone visualization
      if (routingResults.isochrones) {
        routingResults.isochrones.forEach(iso => {
          new google.maps.Polygon({
            paths: iso.polygon.map(coord => ({ lat: coord[1], lng: coord[0] })),
            strokeColor: iso.color,
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: iso.color,
            fillOpacity: 0.25,
            map: map
          })
        })
      }
    }
  }, [map, routingResults])

  return (
    <div className="map-panel">
      <div ref={mapRef} className="map-container" />
      
      <div className="map-controls">
        <button onClick={clearMap} className="control-button">
          Clear Map
        </button>
        
        <select 
          value={visualizationType}
          onChange={(e) => setVisualizationType(e.target.value)}
          className="control-select"
        >
          <option value="markers">Markers</option>
          <option value="heatmap">Heatmap</option>
          <option value="polygons">Polygons</option>
          <option value="isochrone">Isochrone</option>
        </select>
      </div>

      {(activeTab === 'vision' || activeTab === 'routing') && (
        <div className="map-info">
          <p>
            {activeTab === 'vision' && '👁️ Click on map to select location for vision analysis'}
            {activeTab === 'routing' && '📍 Click on map to set locations for routing'}
          </p>
        </div>
      )}
    </div>
  )
}

export default MapPanel

