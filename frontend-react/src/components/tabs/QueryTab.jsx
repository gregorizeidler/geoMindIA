import { useState } from 'react'
import { useAppStore } from '../../store/appStore'
import { processQuery } from '../../services/api'
import './QueryTab.css'

const QueryTab = () => {
  const [query, setQuery] = useState('')
  const { setLoading, setQueryResults, addToHistory } = useAppStore()

  const handleSubmit = async () => {
    if (!query.trim()) {
      alert('Please enter a query')
      return
    }

    setLoading(true, 'Analyzing your query...')

    try {
      const result = await processQuery(query)
      
      if (result.success) {
        setQueryResults(
          result.results,
          result.query,
          result.interpretation,
          result.sql_query
        )
        addToHistory(query)
      } else {
        alert(`Query failed: ${result.error}`)
      }
    } catch (error) {
      console.error('Query failed:', error)
      alert('Failed to process query. Check if backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
      handleSubmit()
    }
  }

  return (
    <div className="query-tab">
      <h2>Ask a Question</h2>
      <p className="description">
        Use natural language to query geospatial data
      </p>

      <div className="query-input-container">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Example: Show me areas in Porto Alegre with high potential for coffee shops, considering young population density, no competitors within 500 meters, and within 10 minutes walk from business centers."
          rows={4}
        />
        
        <button 
          onClick={handleSubmit}
          className="primary-button"
        >
          Analyze
        </button>
      </div>

      <p className="tip">
        💡 Tip: Press Cmd/Ctrl + Enter to submit
      </p>
    </div>
  )
}

export default QueryTab

