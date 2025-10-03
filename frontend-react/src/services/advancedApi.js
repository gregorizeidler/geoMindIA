import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Photo Analysis
export const analyzePhoto = async (imageData, analysisType = 'location') => {
  const response = await api.post('/advanced/photo-analysis', {
    image_data: imageData,
    analysis_type: analysisType
  })
  return response.data
}

// Time Travel
export const getTimeTravelAnalysis = async (lat, lng, years = null) => {
  const response = await api.post('/advanced/time-travel', {
    lat,
    lng,
    years
  })
  return response.data
}

// What-If Simulator
export const simulateWhatIf = async (lat, lng, scenarioType, parameters = {}) => {
  const response = await api.post('/advanced/what-if', {
    lat,
    lng,
    scenario_type: scenarioType,
    parameters
  })
  return response.data
}

// Multi-City Comparison
export const compareCities = async (cities, criteria = {}, businessType = 'general') => {
  const response = await api.post('/advanced/compare-cities', {
    cities,
    criteria,
    business_type: businessType
  })
  return response.data
}

// Get Advanced Features Info
export const getAdvancedFeaturesInfo = async () => {
  const response = await api.get('/advanced/features')
  return response.data
}

export default {
  analyzePhoto,
  getTimeTravelAnalysis,
  simulateWhatIf,
  compareCities,
  getAdvancedFeaturesInfo
}

