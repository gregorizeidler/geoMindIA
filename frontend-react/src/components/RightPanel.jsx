import { useState } from 'react'
import { useAppStore } from '../store/appStore'
import './RightPanel.css'

const RightPanel = () => {
  const { queryResults, interpretation, sqlQuery } = useAppStore()
  const [showInterpretation, setShowInterpretation] = useState(false)
  const [showSQL, setShowSQL] = useState(false)

  return (
    <div className="right-panel">
      {/* Results Section */}
      <div className="results-section">
        <h2>Results</h2>
        
        {queryResults && queryResults.length > 0 ? (
          <div className="results-container">
            {queryResults.map((result, index) => (
              <div key={index} className="result-item">
                <h4>{result.name || `Result ${index + 1}`}</h4>
                
                <div className="result-stats">
                  {result.score !== undefined && (
                    <div className="stat">
                      <span className="stat-label">Score</span>
                      <span className="stat-value">{result.score}/100</span>
                    </div>
                  )}
                  
                  {result.population && (
                    <div className="stat">
                      <span className="stat-label">Population</span>
                      <span className="stat-value">{result.population.toLocaleString()}</span>
                    </div>
                  )}
                  
                  {result.density && (
                    <div className="stat">
                      <span className="stat-label">Density</span>
                      <span className="stat-value">{result.density}/km²</span>
                    </div>
                  )}
                  
                  {result.young_population_pct && (
                    <div className="stat">
                      <span className="stat-label">Young Pop</span>
                      <span className="stat-value">{result.young_population_pct}%</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <p>🎯 Ask a question to see results</p>
          </div>
        )}
      </div>

      {/* Interpretation Section */}
      {interpretation && (
        <div className="collapsible-section">
          <h3 
            className="collapsible-header"
            onClick={() => setShowInterpretation(!showInterpretation)}
          >
            Query Interpretation
            <span className={`toggle-icon ${showInterpretation ? 'open' : ''}`}>▼</span>
          </h3>
          
          {showInterpretation && (
            <div className="collapsible-content">
              <pre>{interpretation}</pre>
            </div>
          )}
        </div>
      )}

      {/* SQL Section */}
      {sqlQuery && (
        <div className="collapsible-section">
          <h3 
            className="collapsible-header"
            onClick={() => setShowSQL(!showSQL)}
          >
            Generated SQL
            <span className={`toggle-icon ${showSQL ? 'open' : ''}`}>▼</span>
          </h3>
          
          {showSQL && (
            <div className="collapsible-content">
              <pre>{sqlQuery}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default RightPanel

