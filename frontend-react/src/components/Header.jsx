import { useAppStore } from '../store/appStore'
import './Header.css'

const StatusDot = ({ status }) => {
  const getStatusClass = (status) => {
    if (typeof status === 'string') {
      if (status === 'healthy') return 'healthy'
      if (status.includes('healthy')) return 'healthy'
    }
    return 'unhealthy'
  }

  return <div className={`status-dot ${getStatusClass(status)}`} />
}

const Header = () => {
  const { healthStatus } = useAppStore()

  return (
    <header className="header">
      <div className="logo">
        <h1>🗺️ GeoMindIA</h1>
        <p>Intelligent geospatial analysis powered by AI</p>
      </div>
      
      <div className="status-indicators">
        <StatusDot status={healthStatus.api} title="API Status" />
        <StatusDot status={healthStatus.database} title="Database Status" />
        <StatusDot status={healthStatus.llm} title="LLM Status" />
        <StatusDot status={healthStatus.vision} title="Vision Status" />
        <StatusDot status={healthStatus.routing} title="Routing Status" />
      </div>
    </header>
  )
}

export default Header

