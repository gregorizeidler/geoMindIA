import { useState } from 'react'
import { useAppStore } from '../../store/appStore'
import { calculateIsochrone, analyzeAccessibility, optimizeRoute } from '../../services/api'
import './RoutingTab.css'

const RoutingTab = () => {
  const [feature, setFeature] = useState('isochrone')
  const [duration, setDuration] = useState(10)
  const [mode, setMode] = useState('walking')
  const [poiTypes, setPoiTypes] = useState({
    transit_station: true,
    hospital: true,
    school: true,
    supermarket: true
  })

  const { 
    selectedLocation,
    waypoints,
    clearWaypoints,
    setLoading,
    routingResults,
    setRoutingResults
  } = useAppStore()

  const handleCalculateIsochrone = async () => {
    if (!selectedLocation) {
      alert('Please click on the map to select a center point')
      return
    }

    setLoading(true, 'Calculating isochrone map...')

    try {
      const result = await calculateIsochrone(
        selectedLocation,
        duration,
        mode,
        [duration / 3, duration * 2 / 3, duration]
      )
      setRoutingResults(result)
    } catch (error) {
      console.error('Failed to calculate isochrone:', error)
      alert('Failed to calculate. Check if backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const handleCalculateAccessibility = async () => {
    if (!selectedLocation) {
      alert('Please click on the map to select a location')
      return
    }

    const selectedTypes = Object.keys(poiTypes).filter(key => poiTypes[key])
    
    if (selectedTypes.length === 0) {
      alert('Please select at least one amenity type')
      return
    }

    setLoading(true, 'Analyzing accessibility...')

    try {
      const result = await analyzeAccessibility(selectedLocation, selectedTypes, 15)
      setRoutingResults(result)
    } catch (error) {
      console.error('Failed to analyze accessibility:', error)
      alert('Failed to calculate. Check if backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const handleOptimizeRoute = async () => {
    if (waypoints.length < 2) {
      alert('Please add at least 2 waypoints on the map')
      return
    }

    setLoading(true, 'Optimizing route...')

    try {
      const locations = waypoints.map(wp => wp.location)
      const result = await optimizeRoute(
        locations[0],
        locations[locations.length - 1],
        locations.slice(1, -1),
        'driving'
      )
      setRoutingResults(result)
    } catch (error) {
      console.error('Failed to optimize route:', error)
      alert('Failed to optimize. Check if backend is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="routing-tab">
      <h2>Route & Accessibility</h2>

      <div className="routing-controls">
        <label>
          Feature:
          <select value={feature} onChange={(e) => setFeature(e.target.value)}>
            <option value="isochrone">Isochrone Map</option>
            <option value="accessibility">Accessibility Score</option>
            <option value="optimize">Route Optimization</option>
          </select>
        </label>

        {/* Isochrone Controls */}
        {feature === 'isochrone' && (
          <div className="feature-controls">
            <label>
              Travel Time (minutes):
              <input 
                type="number" 
                value={duration}
                onChange={(e) => setDuration(parseInt(e.target.value))}
                min="5"
                max="60"
              />
            </label>

            <label>
              Travel Mode:
              <select value={mode} onChange={(e) => setMode(e.target.value)}>
                <option value="walking">Walking</option>
                <option value="driving">Driving</option>
                <option value="bicycling">Bicycling</option>
                <option value="transit">Transit</option>
              </select>
            </label>

            <button 
              onClick={handleCalculateIsochrone}
              className="primary-button"
              disabled={!selectedLocation}
            >
              Calculate Isochrone
            </button>
          </div>
        )}

        {/* Accessibility Controls */}
        {feature === 'accessibility' && (
          <div className="feature-controls">
            <label>Check accessibility to:</label>
            <div className="checkbox-group">
              {Object.keys(poiTypes).map(type => (
                <label key={type}>
                  <input 
                    type="checkbox"
                    checked={poiTypes[type]}
                    onChange={(e) => setPoiTypes({
                      ...poiTypes,
                      [type]: e.target.checked
                    })}
                  />
                  {type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </label>
              ))}
            </div>

            <button 
              onClick={handleCalculateAccessibility}
              className="primary-button"
              disabled={!selectedLocation}
            >
              Analyze Accessibility
            </button>
          </div>
        )}

        {/* Route Optimization Controls */}
        {feature === 'optimize' && (
          <div className="feature-controls">
            <p>Click on map to add waypoints, then optimize route</p>
            
            <div className="waypoint-list">
              {waypoints.map((wp, i) => (
                <div key={i} className="waypoint-item">
                  <span>📍 Point {i + 1}: {wp.location.lat.toFixed(4)}, {wp.location.lng.toFixed(4)}</span>
                </div>
              ))}
            </div>

            <div className="button-group">
              <button 
                onClick={clearWaypoints}
                className="secondary-button"
                disabled={waypoints.length === 0}
              >
                Clear Waypoints
              </button>
              
              <button 
                onClick={handleOptimizeRoute}
                className="primary-button"
                disabled={waypoints.length < 2}
              >
                Optimize Route
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Results Display */}
      {routingResults && (
        <div className="routing-results">
          {feature === 'isochrone' && (
            <div className="result-box success">
              <h3>Isochrone Map Generated</h3>
              <p><strong>Mode:</strong> {routingResults.mode}</p>
              <p><strong>Max Duration:</strong> {routingResults.max_duration_minutes} minutes</p>
              <p><strong>Intervals:</strong> {routingResults.isochrones?.length} zones</p>
            </div>
          )}

          {feature === 'accessibility' && (
            <div className="result-box success">
              <h3>Accessibility Score: {routingResults.overall_score}/10</h3>
              <div className="accessibility-scores">
                {Object.entries(routingResults.accessibility_scores || {}).map(([type, score]) => (
                  <div key={type} className="accessibility-item">
                    {score.accessible ? '✅' : '❌'} <strong>{score.name}:</strong> {score.duration_minutes} min (Score: {score.score}/10)
                  </div>
                ))}
              </div>
            </div>
          )}

          {feature === 'optimize' && (
            <div className="result-box success">
              <h3>Optimized Route</h3>
              <p><strong>Total Distance:</strong> {routingResults.total_distance_km} km</p>
              <p><strong>Total Duration:</strong> {routingResults.total_duration_minutes} minutes</p>
              <p><strong>Waypoints:</strong> {routingResults.waypoints?.length}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default RoutingTab

