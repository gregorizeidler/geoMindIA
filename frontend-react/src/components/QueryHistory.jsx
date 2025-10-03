import { processQuery } from '../services/api'
import { useAppStore } from '../store/appStore'

const QueryHistory = () => {
  const { queryHistory, setLoading, setQueryResults, addToHistory } = useAppStore()

  const handleHistoryClick = async (query) => {
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
    <div className="history-section">
      <h3>Recent Queries</h3>
      
      <div className="query-history">
        {queryHistory.length === 0 ? (
          <p className="empty-state">No queries yet</p>
        ) : (
          queryHistory.map((item, index) => (
            <div
              key={index}
              className="history-item"
              onClick={() => handleHistoryClick(item.query)}
            >
              <div className="history-query">{item.query}</div>
              <div className="history-timestamp">
                {new Date(item.timestamp).toLocaleString()}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default QueryHistory

