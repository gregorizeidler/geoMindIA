import { useState } from 'react'
import { useAppStore } from '../../store/appStore'
import { analyzeSatellite, analyzeStreetView } from '../../services/api'
import './VisionTab.css'

const VisionTab = () => {
  const [analysisType, setAnalysisType] = useState('commercial_potential')
  const [viewType, setViewType] = useState('satellite')
  
  const { 
    selectedLocation, 
    setLoading, 
    visionResults, 
    setVisionResults 
  } = useAppStore()

  const handleAnalyze = async () => {
    if (!selectedLocation) {
      alert('Please click on the map to select a location first')
      return
    }

    setLoading(true, 'Analyzing imagery with AI...')

    try {
      const result = viewType === 'satellite'
        ? await analyzeSatellite(selectedLocation.lat, selectedLocation.lng, analysisType)
        : await analyzeStreetView(selectedLocation.lat, selectedLocation.lng, 0, analysisType)

      setVisionResults(result)
    } catch (error) {
      console.error('Vision analysis failed:', error)
      alert('Failed to analyze. Check if backend is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="vision-tab">
      <h2>AI Vision Analysis</h2>
      <p className="description">
        Click on the map to analyze satellite or street view imagery
      </p>

      <div className="vision-controls">
        <label>
          Analysis Type:
          <select value={analysisType} onChange={(e) => setAnalysisType(e.target.value)}>
            <option value="commercial_potential">Commercial Potential</option>
            <option value="infrastructure">Infrastructure Quality</option>
            <option value="green_space">Green Spaces</option>
            <option value="development">Development Level</option>
            <option value="storefront_quality">Storefront Quality</option>
            <option value="foot_traffic">Foot Traffic</option>
          </select>
        </label>

        <label>
          View Type:
          <select value={viewType} onChange={(e) => setViewType(e.target.value)}>
            <option value="satellite">Satellite View</option>
            <option value="streetview">Street View</option>
          </select>
        </label>

        <button 
          onClick={handleAnalyze}
          className="primary-button"
          disabled={!selectedLocation}
        >
          {selectedLocation ? 'Analyze Selected Location' : 'Select Location on Map'}
        </button>
      </div>

      {/* Results */}
      {visionResults && (
        <div className="vision-results">
          <h3>Analysis Results</h3>
          
          <div className="vision-image">
            <img src={visionResults.image_url} alt="Analysis" />
            <p className="image-caption">
              Location: {visionResults.location.lat.toFixed(4)}, {visionResults.location.lng.toFixed(4)}
            </p>
          </div>

          <div className="vision-insights">
            <h4>AI Insights</h4>
            <pre>{visionResults.insights}</pre>
            {visionResults.mock && (
              <p className="warning">
                ⚠️ Mock data - Enable Gemini API for real AI analysis
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default VisionTab

