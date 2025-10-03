import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Health check
export const checkHealth = async () => {
  const response = await api.get('/health')
  return response.data
}

// Query endpoints
export const processQuery = async (query, context = null) => {
  const response = await api.post('/query', { query, context })
  return response.data
}

export const getSampleQueries = async () => {
  const response = await api.get('/sample-queries')
  return response.data
}

// Vision analysis endpoints
export const analyzeSatellite = async (lat, lng, analysisType = 'commercial_potential', zoom = 18) => {
  const response = await api.post('/analyze/satellite', {
    lat,
    lng,
    analysis_type: analysisType,
    zoom
  })
  return response.data
}

export const analyzeStreetView = async (lat, lng, heading = 0, analysisFocus = 'storefront_quality') => {
  const response = await api.post('/analyze/streetview', {
    lat,
    lng,
    heading,
    analysis_focus: analysisFocus
  })
  return response.data
}

export const compareLocations = async (locations, analysisType = 'comparative') => {
  const response = await api.post('/analyze/compare-locations', {
    locations,
    analysis_type: analysisType
  })
  return response.data
}

export const analyzeSentiment = async (reviews, aspect = 'overall') => {
  const response = await api.post('/analyze/sentiment', {
    reviews,
    aspect
  })
  return response.data
}

// Routing endpoints
export const optimizeRoute = async (origin, destination, waypoints, mode = 'driving') => {
  const response = await api.post('/routing/optimize', {
    origin,
    destination,
    waypoints,
    mode
  })
  return response.data
}

export const calculateIsochrone = async (center, durationMinutes, mode = 'walking', intervals = null) => {
  const response = await api.post('/routing/isochrone', {
    center,
    duration_minutes: durationMinutes,
    mode,
    intervals
  })
  return response.data
}

export const analyzeAccessibility = async (location, poiTypes = null, maxDurationMinutes = 15) => {
  const response = await api.post('/routing/accessibility', {
    location,
    poi_types: poiTypes,
    max_duration_minutes: maxDurationMinutes
  })
  return response.data
}

export const findMeetingPoint = async (locations, mode = 'transit') => {
  const response = await api.post('/routing/meeting-point', {
    locations,
    mode
  })
  return response.data
}

export default api

