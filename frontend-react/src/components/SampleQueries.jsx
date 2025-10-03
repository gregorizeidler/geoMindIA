import { useState, useEffect } from 'react'
import { getSampleQueries } from '../services/api'
import { processQuery } from '../services/api'
import { useAppStore } from '../store/appStore'

const SampleQueries = () => {
  const [samples, setSamples] = useState([])
  const { setLoading, setQueryResults, addToHistory } = useAppStore()

  useEffect(() => {
    const loadSamples = async () => {
      try {
        const data = await getSampleQueries()
        setSamples(data.samples || [])
      } catch (error) {
        console.error('Failed to load sample queries:', error)
      }
    }

    loadSamples()
  }, [])

  const handleQueryClick = async (query) => {
    setLoading(true, 'Analyzing query...')

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
      }
    } catch (error) {
      console.error('Query failed:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="samples-section">
      <h3>Sample Queries</h3>
      
      <div className="sample-queries">
        {samples.map((category, catIndex) => (
          <div key={catIndex} className="sample-category">
            <h4>{category.category}</h4>
            
            {category.queries.map((query, queryIndex) => (
              <div
                key={queryIndex}
                className="sample-query"
                onClick={() => handleQueryClick(query)}
              >
                {query}
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}

export default SampleQueries

