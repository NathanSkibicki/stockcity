import { useState, useEffect } from 'react'
import './App.css'
import { LineChart } from '@mui/x-charts/LineChart'

function App() {
  const [chartData, setChartData] = useState({
    dates: [],
    values: []
  })
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const response = await fetch('http://localhost:5000/api/data')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data = await response.json()
        
        // Convert string dates to Date objects
        const formattedData = {
          dates: data.dates.map(dateStr => new Date(dateStr)),
          values: data.values
        }
        
        setChartData(formattedData)
        setError(null)
      } catch (error) {
        console.error('Error fetching data:', error)
        setError('Failed to connect to the server. Please make sure the Flask backend is running.')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  return (
    <div className="App">
      <h1>FRED Data Visualization</h1>
      {loading && <p>Loading data...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {!loading && !error && chartData.dates.length > 0 && (
        <LineChart
          xAxis={[{
            data: chartData.dates,
            scaleType: 'time',
            valueFormatter: (date) => date.toLocaleDateString(),
          }]}
          series={[
            {
              data: chartData.values,
              label: 'CPI Data',
              area: true,
            },
          ]}
          height={400}
          margin={{ top: 20, right: 20, bottom: 50, left: 50 }}
        />
      )}
    </div>
  )
}

export default App
