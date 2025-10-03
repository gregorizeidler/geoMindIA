import { useState, useRef } from 'react'
import { useAppStore } from '../../store/appStore'
import { analyzePhoto } from '../../services/advancedApi'
import './PhotoAnalysisTab.css'

const PhotoAnalysisTab = () => {
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [analysisType, setAnalysisType] = useState('location')
  const [results, setResults] = useState(null)
  const fileInputRef = useRef(null)
  
  const { setLoading } = useAppStore()

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      setSelectedFile(file)
      
      // Create preview
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreviewUrl(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleAnalyze = async () => {
    if (!selectedFile) {
      alert('Please select a photo first')
      return
    }

    setLoading(true, 'Analyzing photo with AI...')

    try {
      // Convert to base64
      const reader = new FileReader()
      reader.onloadend = async () => {
        const base64 = reader.result.split(',')[1] // Remove data:image/...;base64,
        
        const result = await analyzePhoto(base64, analysisType)
        setResults(result)
      }
      reader.readAsDataURL(selectedFile)
      
    } catch (error) {
      console.error('Photo analysis failed:', error)
      alert('Failed to analyze photo. Check if backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setSelectedFile(null)
    setPreviewUrl(null)
    setResults(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  return (
    <div className="photo-analysis-tab">
      <h2>📸 Photo Analysis</h2>
      <p className="description">
        Upload a photo and AI will identify the location and provide insights
      </p>

      <div className="upload-section">
        <div className="file-input-wrapper">
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            className="file-input"
            id="photo-upload"
          />
          <label htmlFor="photo-upload" className="file-input-label">
            {selectedFile ? '📷 Change Photo' : '📁 Choose Photo'}
          </label>
        </div>

        {previewUrl && (
          <div className="preview-container">
            <img src={previewUrl} alt="Preview" className="preview-image" />
          </div>
        )}
      </div>

      <div className="analysis-controls">
        <label>
          Analysis Type:
          <select value={analysisType} onChange={(e) => setAnalysisType(e.target.value)}>
            <option value="location">📍 Identify Location</option>
            <option value="property_value">💰 Property Value Estimate</option>
            <option value="similar_places">🔍 Find Similar Places</option>
            <option value="urban_features">🏙️ Urban Features Analysis</option>
          </select>
        </label>

        <div className="button-group">
          <button
            onClick={handleAnalyze}
            className="primary-button"
            disabled={!selectedFile}
          >
            Analyze Photo
          </button>
          
          {selectedFile && (
            <button onClick={handleClear} className="secondary-button">
              Clear
            </button>
          )}
        </div>
      </div>

      {/* Results */}
      {results && (
        <div className="analysis-results">
          <h3>Analysis Results</h3>
          
          <div className="result-box">
            {results.identified_location && (
              <div className="result-item">
                <strong>📍 Identified Location:</strong>
                <p>{results.identified_location}</p>
              </div>
            )}

            {results.city && (
              <div className="result-item">
                <strong>🏙️ City:</strong>
                <p>{results.city}</p>
              </div>
            )}

            {results.neighborhood && (
              <div className="result-item">
                <strong>🏘️ Neighborhood:</strong>
                <p>{results.neighborhood}</p>
              </div>
            )}

            {results.characteristics && results.characteristics.length > 0 && (
              <div className="result-item">
                <strong>✨ Characteristics:</strong>
                <div className="tags">
                  {results.characteristics.map((char, i) => (
                    <span key={i} className="tag">{char}</span>
                  ))}
                </div>
              </div>
            )}

            {results.property_value_estimate && (
              <div className="result-item">
                <strong>💰 Property Value:</strong>
                <p>{results.property_value_estimate}</p>
              </div>
            )}

            {results.confidence_score && (
              <div className="result-item">
                <strong>🎯 Confidence Score:</strong>
                <div className="confidence-bar">
                  <div 
                    className="confidence-fill"
                    style={{ width: `${results.confidence_score * 100}%` }}
                  />
                  <span className="confidence-text">
                    {(results.confidence_score * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            )}

            {results.similar_locations && results.similar_locations.length > 0 && (
              <div className="result-item">
                <strong>🔍 Similar Locations:</strong>
                <ul>
                  {results.similar_locations.map((loc, i) => (
                    <li key={i}>{loc}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className="result-item full-analysis">
              <strong>📋 Full Analysis:</strong>
              <pre>{results.full_analysis}</pre>
            </div>

            {results.mock && (
              <p className="warning">
                ⚠️ Mock data - Enable Gemini API for real AI-powered analysis
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default PhotoAnalysisTab

