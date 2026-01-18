import React, { useState, useEffect } from 'react'
import axios from 'axios'
import CreateTestForm from './CreateTestForm'
import TestTable from './TestTable'
import './Dashboard.css'

const Dashboard = ({ onLogout }) => {
  const [tests, setTests] = useState([])
  const [loading, setLoading] = useState(true)
  const [showCreateForm, setShowCreateForm] = useState(false)

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

  useEffect(() => {
    fetchTests()
  }, [])

  const fetchTests = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/tests`)
      setTests(response.data)
    } catch (error) {
      console.error('Error fetching tests:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleTestCreated = () => {
    fetchTests()
    setShowCreateForm(false)
  }

  const handleTestUpdated = () => {
    fetchTests()
  }

  // Calculate statistics
  const stats = {
    total: tests.length,
    pending: tests.filter(t => t.status === 'Pending').length,
    inProgress: tests.filter(t => t.status === 'In Progress').length,
    completed: tests.filter(t => t.status === 'Completed').length
  }

  return (
    <div className="dashboard">
      <nav className="navbar">
        <h1>Laboratory Information System</h1>
        <button onClick={onLogout} className="btn-secondary">
          Logout
        </button>
      </nav>

      <div className="dashboard-content">
        <div className="dashboard-stats">
          <div className="stat-card">
            <div className="stat-label">Total Tests</div>
            <div className="stat-value">{stats.total}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Pending</div>
            <div className="stat-value">{stats.pending}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">In Progress</div>
            <div className="stat-value">{stats.inProgress}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Completed</div>
            <div className="stat-value">{stats.completed}</div>
          </div>
        </div>

        <div className="dashboard-actions">
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="btn-primary"
          >
            {showCreateForm ? 'Cancel' : 'Create Lab Test'}
          </button>
        </div>

        {showCreateForm && (
          <CreateTestForm
            onTestCreated={handleTestCreated}
            onCancel={() => setShowCreateForm(false)}
          />
        )}

        {loading ? (
          <div className="loading">Loading tests...</div>
        ) : (
          <TestTable tests={tests} onTestUpdated={handleTestUpdated} />
        )}
      </div>
    </div>
  )
}

export default Dashboard
