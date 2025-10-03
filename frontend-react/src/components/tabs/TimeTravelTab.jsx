import { useState } from 'react'
import { useAppStore } from '../../store/appStore'
import { getTimeTravelAnalysis } from '../../services/advancedApi'
import './TimeTravelTab.css'

const TimeTravelTab = () => {
  const [years, setYears] = useState('2010,2015,2020,2024')
  const [results, setResults] = useState(null)
  const [selectedYear, setSelectedYear] = useState(null)
  
  const { selectedLocation, setLoading } = useAppStore()

  const handleAnalyze = async () => {
    if (!selectedLocation) {
      alert('Please click on the map to select a location first')
      return
    }

    setLoading(true, 'Traveling through time...')

    try {
      const yearArray = years.split(',').map(y => parseInt(y.trim())).filter(y => !isNaN(y))
      
      const result = await getTimeTravelAnalysis(
        selectedLocation.lat,
        selectedLocation.lng,
        yearArray
      )
      
      setResults(result)
      if (result.images && result.images.length > 0) {
        setSelectedYear(result.images[0].year)
      }
    } catch (error) {
      console.error('Time travel analysis failed:', error)
      alert('Failed to analyze. Check if backend is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="time-travel-tab">
      <h2>🎬 Time Travel</h2>
      <p className="description">
        See how a location changed over time with historical satellite imagery
      </p>

      <div className="time-travel-controls">
        <label>
          Years to Compare (comma-separated):
          <input
            type="text"
            value={years}
            onChange={(e) => setYears(e.target.value)}
            placeholder="2010,2015,2020,2024"
            className="years-input"
          />
        </label>

        <button
          onClick={handleAnalyze}
          className="primary-button"
          disabled={!selectedLocation}
        >
          {selectedLocation ? 'Analyze Time Evolution' : 'Select Location on Map'}
        </button>
      </div>

      {/* Results */}
      {results && (
        <div className="time-travel-results">
          <h3>Time Travel Analysis</h3>
          
          <div className="timeline-slider">
            <div className="year-buttons">
              {results.images?.map((img) => (
                <button
                  key={img.year}
                  className={`year-button ${selectedYear === img.year ? 'active' : ''}`}
                  onClick={() => setSelectedYear(img.year)}
                >
                  {img.year}
                </button>
              ))}
            </div>
          </div>

          {selectedYear && (
            <div className="year-view">
              <h4>Year: {selectedYear}</h4>
              {results.images?.find(img => img.year === selectedYear) && (
                <div className="satellite-image">
                  <img
                    src={results.images.find(img => img.year === selectedYear).image_url}
                    alt={`Satellite view ${selectedYear}`}
                    className="historical-image"
                  />
                  <p className="image-description">
                    {results.images.find(img => img.year === selectedYear).description}
                  </p>
                </div>
              )}
            </div>
          )}

          <div className="change-analysis">
            <h4>📊 Change Analysis</h4>
            <div className="analysis-grid">
              {Object.entries(results.change_analysis || {}).map(([key, value]) => (
                <div key={key} className="analysis-item">
                  <strong>{key.replace(/_/g, ' ').toUpperCase()}:</strong>
                  <p>{Array.isArray(value) ? value.join(', ') : value}</p>
                </div>
              ))}
            </div>
          </div>

          {results.key_changes && (
            <div className="key-changes">
              <h4>🔑 Key Changes</h4>
              <ul>
                {results.key_changes.map((change, i) => (
                  <li key={i}>{change}</li>
                ))}
              </ul>
            </div>
          )}

          {results.growth_rate && (
            <div className="growth-rate">
              <strong>📈 Average Growth Rate:</strong> {results.growth_rate}% per year
            </div>
          )}

          {results.predictions && (
            <div className="predictions">
              <h4>🔮 Future Predictions</h4>
              {Object.entries(results.predictions).map(([year, prediction]) => (
                <div key={year} className="prediction-item">
                  <strong>{year}:</strong> {prediction}
                </div>
              ))}
            </div>
          )}

          {results.mock && (
            <p className="warning">
              ⚠️ Mock data - Enable Google Earth Engine API for real historical imagery
            </p>
          )}
        </div>
      )}
    </div>
  )
}

export default TimeTravelTab

