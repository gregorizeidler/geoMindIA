import { useState, useEffect, useCallback } from 'react'

export const useGoogleMap = (mapRef, options) => {
  const [map, setMap] = useState(null)
  const [markers, setMarkers] = useState([])
  const [polygons, setPolygons] = useState([])
  const [heatmap, setHeatmap] = useState(null)

  // Initialize map
  useEffect(() => {
    if (!mapRef.current || !window.google) return

    const newMap = new google.maps.Map(mapRef.current, {
      ...options,
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
    })

    setMap(newMap)
  }, [mapRef])

  // Clear all visualizations
  const clearMap = useCallback(() => {
    // Clear markers
    markers.forEach(marker => marker.setMap(null))
    setMarkers([])

    // Clear polygons
    polygons.forEach(polygon => polygon.setMap(null))
    setPolygons([])

    // Clear heatmap
    if (heatmap) {
      heatmap.setMap(null)
      setHeatmap(null)
    }
  }, [markers, polygons, heatmap])

  // Visualize results
  const visualizeResults = useCallback((results, type) => {
    if (!map || !results || results.length === 0) return

    clearMap()

    switch (type) {
      case 'markers':
        visualizeAsMarkers(results)
        break
      case 'heatmap':
        visualizeAsHeatmap(results)
        break
      case 'polygons':
        visualizeAsPolygons(results)
        break
      default:
        visualizeAsMarkers(results)
    }

    fitMapBounds(results)
  }, [map, clearMap])

  const visualizeAsMarkers = (results) => {
    const newMarkers = results.map((result, index) => {
      const position = result.center || getCenterFromGeometry(result.geometry)
      
      if (!position) return null

      const marker = new google.maps.Marker({
        position,
        map,
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
      })

      const infoWindow = new google.maps.InfoWindow({
        content: createInfoWindowContent(result, index)
      })

      marker.addListener('click', () => {
        infoWindow.open(map, marker)
      })

      return marker
    }).filter(Boolean)

    setMarkers(newMarkers)
  }

  const visualizeAsPolygons = (results) => {
    const newPolygons = results.map((result) => {
      if (!result.geometry || result.geometry.type !== 'Polygon') return null

      const coords = result.geometry.coordinates[0].map(coord => ({
        lat: coord[1],
        lng: coord[0]
      }))

      const polygon = new google.maps.Polygon({
        paths: coords,
        strokeColor: getColorForScore(result.score),
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: getColorForScore(result.score),
        fillOpacity: 0.35,
        map
      })

      return polygon
    }).filter(Boolean)

    setPolygons(newPolygons)
  }

  const visualizeAsHeatmap = (results) => {
    const heatmapData = results.map(result => {
      const position = result.center || getCenterFromGeometry(result.geometry)
      return position ? new google.maps.LatLng(position.lat, position.lng) : null
    }).filter(Boolean)

    const newHeatmap = new google.maps.visualization.HeatmapLayer({
      data: heatmapData,
      map,
      radius: 50,
      opacity: 0.6
    })

    setHeatmap(newHeatmap)
  }

  const fitMapBounds = (results) => {
    const bounds = new google.maps.LatLngBounds()
    
    results.forEach(result => {
      const position = result.center || getCenterFromGeometry(result.geometry)
      if (position) {
        bounds.extend(position)
      }
    })
    
    map.fitBounds(bounds)
  }

  return { map, visualizeResults, clearMap }
}

// Helper functions
const getCenterFromGeometry = (geometry) => {
  if (!geometry || !geometry.coordinates) return null
  
  if (geometry.type === 'Point') {
    return { lat: geometry.coordinates[1], lng: geometry.coordinates[0] }
  } else if (geometry.type === 'Polygon') {
    const coords = geometry.coordinates[0]
    const sumLat = coords.reduce((sum, coord) => sum + coord[1], 0)
    const sumLng = coords.reduce((sum, coord) => sum + coord[0], 0)
    return {
      lat: sumLat / coords.length,
      lng: sumLng / coords.length
    }
  }
  
  return null
}

const getColorForScore = (score) => {
  if (!score) return '#3b82f6'
  
  if (score >= 80) return '#10b981' // Green
  if (score >= 60) return '#3b82f6' // Blue
  if (score >= 40) return '#f59e0b' // Yellow
  return '#ef4444' // Red
}

const createInfoWindowContent = (result, index) => {
  return `
    <div style="padding: 10px; max-width: 250px;">
      <h3 style="margin: 0 0 10px 0; font-size: 16px;">${result.name || `Area ${index + 1}`}</h3>
      ${result.score ? `<p><strong>Score:</strong> ${result.score}/100</p>` : ''}
      ${result.population ? `<p><strong>Population:</strong> ${result.population.toLocaleString()}</p>` : ''}
      ${result.density ? `<p><strong>Density:</strong> ${result.density}/km²</p>` : ''}
      ${result.young_population_pct ? `<p><strong>Young Pop:</strong> ${result.young_population_pct}%</p>` : ''}
    </div>
  `
}

