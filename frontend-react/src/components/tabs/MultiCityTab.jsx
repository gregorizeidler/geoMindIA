import { useState } from 'react'
import { useAppStore } from '../../store/appStore'
import { compareCities } from '../../services/advancedApi'
import './MultiCityTab.css'

const MultiCityTab = () => {
  const [cities, setCities] = useState('São Paulo,Rio de Janeiro,Porto Alegre')
  const [businessType, setBusinessType] = useState('general')
  const [results, setResults] = useState(null)
  
  const { setLoading } = useAppStore()

  const businessTypes = [
    { value: 'general', label: 'General Business' },
    { value: 'restaurant', label: 'Restaurant' },
    { value: 'retail', label: 'Retail Store' },
    { value: 'gym', label: 'Gym / Fitness' },
    { value: 'coworking', label: 'Coworking Space' },
    { value: 'cafe', label: 'Coffee Shop' },
    { value: 'tech', label: 'Tech Company' }
  ]

  const handleCompare = async () => {
    const cityArray = cities.split(',').map(c => c.trim()).filter(c => c)
    
    if (cityArray.length < 2) {
      alert('Please enter at least 2 cities separated by commas')
      return
    }

    setLoading(true, 'Comparing cities...')

    try {
      const result = await compareCities(cityArray, {}, businessType)
      setResults(result)
    } catch (error) {
      console.error('City comparison failed:', error)
      alert('Failed to compare cities. Check if backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const getMedalColor = (rank) => {
    switch(rank) {
      case 1: return 'gold'
      case 2: return 'silver'
      case 3: return 'bronze'
      default: return 'default'
    }
  }

  return (
    <div className="multicity-tab">
      <h2>🌐 Multi-City Comparison</h2>
      <p className="description">
        Compare multiple cities automatically for business potential
      </p>

      <div className="comparison-controls">
        <label>
          Cities (comma-separated):
          <input
            type="text"
            value={cities}
            onChange={(e) => setCities(e.target.value)}
            placeholder="São Paulo, Rio de Janeiro, Porto Alegre"
            className="cities-input"
          />
        </label>

        <label>
          Business Type:
          <select value={businessType} onChange={(e) => setBusinessType(e.target.value)}>
            {businessTypes.map(type => (
              <option key={type.value} value={type.value}>
                {type.label}
              </option>
            ))}
          </select>
        </label>

        <button onClick={handleCompare} className="primary-button">
          Compare Cities
        </button>
      </div>

      {/* Results */}
      {results && (
        <div className="comparison-results">
          <div className="results-header">
            <h3>Comparison Results</h3>
            <p>Business Type: <strong>{results.comparison_type}</strong></p>
            <p>Cities Analyzed: <strong>{results.cities_analyzed}</strong></p>
          </div>

          {results.summary && (
            <div className="summary-box">
              <h4>📊 Executive Summary</h4>
              <pre>{results.summary}</pre>
            </div>
          )}

          <div className="cities-ranking">
            {results.results?.map((city) => (
              <div key={city.city} className={`city-card rank-${getMedalColor(city.rank)}`}>
                <div className="city-header">
                  <span className="medal">{city.medal}</span>
                  <h4>#{city.rank} - {city.city}</h4>
                  <span className="score">{city.score}/100</span>
                </div>

                <div className="city-stats">
                  <div className="stat">
                    <span className="stat-label">Population:</span>
                    <span className="stat-value">{city.population}</span>
                  </div>
                  
                  <div className="stat">
                    <span className="stat-label">Avg Income:</span>
                    <span className="stat-value">{city.avg_income}</span>
                  </div>
                  
                  <div className="stat">
                    <span className="stat-label">GDP per Capita:</span>
                    <span className="stat-value">{city.gdp_per_capita}</span>
                  </div>
                  
                  <div className="stat">
                    <span className="stat-label">Competition:</span>
                    <span className={`stat-value competition-${city.competition_level}`}>
                      {city.competition_level}
                    </span>
                  </div>
                  
                  <div className="stat">
                    <span className="stat-label">Market Saturation:</span>
                    <span className="stat-value">{city.market_saturation}</span>
                  </div>
                  
                  <div className="stat">
                    <span className="stat-label">Growth Rate:</span>
                    <span className="stat-value">{city.growth_rate}</span>
                  </div>
                </div>

                {city.opportunity_areas && city.opportunity_areas.length > 0 && (
                  <div className="opportunity-areas">
                    <strong>🎯 Top Neighborhoods:</strong>
                    <div className="tags">
                      {city.opportunity_areas.map((area, i) => (
                        <span key={i} className="tag">{area}</span>
                      ))}
                    </div>
                  </div>
                )}

                {city.strengths && city.strengths.length > 0 && (
                  <div className="strengths">
                    <strong>✅ Strengths:</strong>
                    <ul>
                      {city.strengths.map((strength, i) => (
                        <li key={i}>{strength}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {city.challenges && city.challenges.length > 0 && (
                  <div className="challenges">
                    <strong>⚠️ Challenges:</strong>
                    <ul>
                      {city.challenges.map((challenge, i) => (
                        <li key={i}>{challenge}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {city.recommendation && (
                  <div className="recommendation">
                    <strong>💡 Recommendation:</strong>
                    <p>{city.recommendation}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default MultiCityTab

