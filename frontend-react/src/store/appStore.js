import { create } from 'zustand'

export const useAppStore = create((set, get) => ({
  // Health status
  healthStatus: {
    api: 'unknown',
    database: 'unknown',
    llm: 'unknown',
    maps: 'unknown',
    vision: 'unknown',
    routing: 'unknown'
  },
  setHealthStatus: (status) => set({ healthStatus: status }),

  // Loading state
  loading: false,
  loadingMessage: 'Processing...',
  setLoading: (loading, message = 'Processing...') => 
    set({ loading, loadingMessage: message }),

  // Current tab
  activeTab: 'query',
  setActiveTab: (tab) => set({ activeTab: tab }),

  // Query results
  queryResults: [],
  currentQuery: '',
  interpretation: '',
  sqlQuery: '',
  setQueryResults: (results, query, interpretation, sqlQuery) => 
    set({ 
      queryResults: results, 
      currentQuery: query,
      interpretation,
      sqlQuery 
    }),

  // Map state
  selectedLocation: null,
  setSelectedLocation: (location) => set({ selectedLocation: location }),

  // Vision analysis
  visionResults: null,
  setVisionResults: (results) => set({ visionResults: results }),

  // Routing data
  routingResults: null,
  waypoints: [],
  setRoutingResults: (results) => set({ routingResults: results }),
  addWaypoint: (waypoint) => set((state) => ({
    waypoints: [...state.waypoints, waypoint]
  })),
  removeWaypoint: (index) => set((state) => ({
    waypoints: state.waypoints.filter((_, i) => i !== index)
  })),
  clearWaypoints: () => set({ waypoints: [] }),

  // Visualization type
  visualizationType: 'markers',
  setVisualizationType: (type) => set({ visualizationType: type }),

  // Query history
  queryHistory: JSON.parse(localStorage.getItem('queryHistory') || '[]'),
  addToHistory: (query) => set((state) => {
    const newHistory = [
      { query, timestamp: new Date().toISOString() },
      ...state.queryHistory
    ].slice(0, 10)
    localStorage.setItem('queryHistory', JSON.stringify(newHistory))
    return { queryHistory: newHistory }
  })
}))

