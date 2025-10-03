import { useState } from 'react'
import { useAppStore } from '../../store/appStore'
import { simulateWhatIf } from '../../services/advancedApi'
import './WhatIfTab.css'

const WhatIfTab = () => {
  const [scenario, setScenario] = useState('new_metro_station')
  const [parameters, setParameters] = useState({})
  const [results, setResults] = useState(null)
  
  const { selectedLocation, setLoading } = useAppStore()

  const scenarios = [
    { value: 'new_metro_station', label: '🚇 New Metro Station', icon: '🚇' },
    { value: 'new_shopping_mall', label: '🏬 New Shopping Mall', icon: '🏬' },
    { value: 'population_increase', label: '📈 Population Increase', icon: '📈' },
    { value: 'new_park', label: '🌳 New Park', icon: '🌳' },
    { value: 'commercial_zone', label: '🏢 Commercial Zone', icon: '🏢' }
  ]

  const handleSimulate = async () => {
    if (!selectedLocation) {
      alert('Please click on the map to select a location first')
      return
    }

    setLoading(true, 'Running simulation...')

    try {
      const result = await simulateWhatIf(
        selectedLocation.lat,
        selectedLocation.lng,
        scenario,
        parameters
      )
      
      setResults(result)
    } catch (error) {
      console.error('Simulation failed:', error)
      alert('Failed to simulate. Check if backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const renderParametersInput = () => {
    switch (scenario) {
      case 'new_shopping_mall':
        return (
          <label>
            Mall Size:
            <select 
              value={parameters.size || 'medium'}
              onChange={(e) => setParameters({ ...parameters, size: e.target.value })}
            >
              <option value="small">Small</option>
              <option value="medium">Medium</option>
              <option value="large">Large</option>
            </select>
          </label>
        )
      case 'population_increase':
        return (
          <label>
            Growth Percentage:
            <input
              type="number"
              value={parameters.growth_percentage || 30}
              onChange={(e) => setParameters({ ...parameters, growth_percentage: parseInt(e.target.value) })}
              min="5"
              max="100"
            />
            %
          </label>
        )
      case 'new_park':
        return (
          <label>
            Park Size (hectares):
            <input
              type="number"
              value={parameters.size_hectares || 5}
              onChange={(e) => setParameters({ ...parameters, size_hectares: parseInt(e.target.value) })}
              min="1"
              max="50"
            />
          </label>
        )
      default:
        return null
    }
  }

  const renderImpacts = (impacts) => {
    if (!impacts) return null

    return Object.entries(impacts).map(([category, data]) => (
      <div key={category} className="impact-category">
        <h4>{category.replace(/_/g, ' ').toUpperCase()}</h4>
        <div className="impact-details">
          {typeof data === 'object' && !Array.isArray(data) ? (
            Object.entries(data).map(([key, value]) => (
              <div key={key} className="impact-item">
                <span className="impact-key">{key.replace(/_/g, ' ')}:</span>
                <span className="impact-value">{Array.isArray(value) ? value.join(', ') : String(value)}</span>
              </div>
            ))
          ) : (
            <p>{String(data)}</p>
          )}
        </div>
      </div>
    ))
  }

  return (
    <div className="whatif-tab">
      <h2>🎲 What-If Simulator</h2>
      <p className="description">
        Simulate urban changes and see predicted impacts
      </p>

      <div className="whatif-controls">
        <label>
          Scenario Type:
          <select value={scenario} onChange={(e) => setScenario(e.target.value)}>
            {scenarios.map(s => (
              <option key={s.value} value={s.value}>
                {s.label}
              </option>
            ))}
          </select>
        </label>

        {renderParametersInput()}

        <button
          onClick={handleSimulate}
          className="primary-button"
          disabled={!selectedLocation}
        >
          {selectedLocation ? 'Run Simulation' : 'Select Location on Map'}
        </button>
      </div>

      {/* Results */}
      {results && (
        <div className="simulation-results">
          <div className="result-header">
            <h3>{scenarios.find(s => s.value === scenario)?.icon} {results.scenario}</h3>
            <p className="location-info">
              📍 Location: {results.location?.lat.toFixed(4)}, {results.location?.lng.toFixed(4)}
            </p>
          </div>

          {results.timeline && (
            <div className="timeline-info">
              <strong>⏱️ Timeline:</strong> {results.timeline}
            </div>
          )}

          {results.impacts && (
            <div className="impacts-section">
              <h4>📊 Predicted Impacts</h4>
              {renderImpacts(results.impacts)}
            </div>
          )}

          {results.mall_details && (
            <div className="extra-details">
              <h4>🏬 Mall Details</h4>
              {Object.entries(results.mall_details).map(([key, value]) => (
                <div key={key} className="detail-item">
                  <strong>{key.replace(/_/g, ' ')}:</strong> {value}
                </div>
              ))}
            </div>
          )}

          {results.risks && results.risks.length > 0 && (
            <div className="risks-section">
              <h4>⚠️ Risks</h4>
              <ul>
                {results.risks.map((risk, i) => (
                  <li key={i} className="risk-item">{risk}</li>
                ))}
              </ul>
            </div>
          )}

          {results.opportunities && results.opportunities.length > 0 && (
            <div className="opportunities-section">
              <h4>✅ Opportunities</h4>
              <ul>
                {results.opportunities.map((opp, i) => (
                  <li key={i} className="opportunity-item">{opp}</li>
                ))}
              </ul>
            </div>
          )}

          {results.winners && results.winners.length > 0 && (
            <div className="winners-section">
              <h4>🏆 Winners</h4>
              <ul>
                {results.winners.map((winner, i) => (
                  <li key={i}>{winner}</li>
                ))}
              </ul>
            </div>
          )}

          {results.losers && results.losers.length > 0 && (
            <div className="losers-section">
              <h4>⚠️ Losers</h4>
              <ul>
                {results.losers.map((loser, i) => (
                  <li key={i}>{loser}</li>
                ))}
              </ul>
            </div>
          )}

          {results.roi_estimate && (
            <div className="roi-section">
              <h4>💰 ROI Estimates</h4>
              {Object.entries(results.roi_estimate).map(([key, value]) => (
                <div key={key} className="roi-item">
                  <strong>{key.replace(/_/g, ' ')}:</strong> {value}
                </div>
              ))}
            </div>
          )}

          {results.recommendation && (
            <div className="recommendation">
              <strong>💡 Recommendation:</strong>
              <p>{results.recommendation}</p>
            </div>
          )}

          {results.recommendations && results.recommendations.length > 0 && (
            <div className="recommendations-list">
              <h4>💡 Recommendations</h4>
              <ul>
                {results.recommendations.map((rec, i) => (
                  <li key={i}>{rec}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default WhatIfTab

