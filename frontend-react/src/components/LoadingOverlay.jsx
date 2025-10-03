import { useAppStore } from '../store/appStore'
import './LoadingOverlay.css'

const LoadingOverlay = ({ message }) => {
  const { loading, loadingMessage } = useAppStore()

  if (!loading && !message) return null

  return (
    <div className="loading-overlay">
      <div className="loading-spinner" />
      <p>{message || loadingMessage}</p>
    </div>
  )
}

export default LoadingOverlay

