import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'

function App () {
  return (
    <div>
      <h1>HI</h1>
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
