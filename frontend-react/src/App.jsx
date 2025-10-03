import { useState, useEffect } from 'react'
import Header from './components/Header'
import LeftPanel from './components/LeftPanel'
import MapPanel from './components/MapPanel'
import RightPanel from './components/RightPanel'
import LoadingOverlay from './components/LoadingOverlay'
import { useAppStore } from './store/appStore'
import { checkHealth } from './services/api'
import './App.css'

function App() {
  const { setHealthStatus, setLoading } = useAppStore()
  const [initialized, setInitialized] = useState(false)

  useEffect(() => {
    // Check API health on mount
    const initializeApp = async () => {
      try {
        const health = await checkHealth()
        setHealthStatus(health)
      } catch (error) {
        console.error('Failed to check health:', error)
      } finally {
        setInitialized(true)
      }
    }

    initializeApp()

    // Periodic health check
    const interval = setInterval(async () => {
      try {
        const health = await checkHealth()
        setHealthStatus(health)
      } catch (error) {
        console.error('Health check failed:', error)
      }
    }, 30000)

    return () => clearInterval(interval)
  }, [setHealthStatus])

  if (!initialized) {
    return <LoadingOverlay message="Initializing..." />
  }

  return (
    <div className="app-container">
      <Header />
      
      <main className="main-content">
        <LeftPanel />
        <MapPanel />
        <RightPanel />
      </main>

      <LoadingOverlay />
    </div>
  )
}

export default App

