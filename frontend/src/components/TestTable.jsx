import React, { useState } from 'react'
import axios from 'axios'
import './TestTable.css'

const TestTable = ({ tests, onTestUpdated }) => {
  const [editingId, setEditingId] = useState(null)
  const [editData, setEditData] = useState({})
  const [error, setError] = useState('')

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

  const handleEdit = (test) => {
    setEditingId(test.id)
    setEditData({
      status: test.status,
      result: test.result || ''
    })
    setError('')
  }

  const handleCancel = () => {
    setEditingId(null)
    setEditData({})
    setError('')
  }

  const handleSave = async (testId) => {
    setError('')
    try {
      await axios.put(`${API_BASE_URL}/tests/${testId}`, editData)
      setEditingId(null)
      setEditData({})
      onTestUpdated()
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update test')
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setEditData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  if (tests.length === 0) {
    return (
      <div className="no-tests">
        <p>No lab tests found. Create your first test above.</p>
      </div>
    )
  }

  return (
    <div className="test-table-container">
      <h2>Lab Tests</h2>
      {error && <div className="error-message">{error}</div>}
      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Patient Name</th>
              <th>Doctor Name</th>
              <th>Test Type</th>
              <th>Status</th>
              <th>Result</th>
              <th>Created At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {tests.map(test => (
              <tr key={test.id}>
                <td>{test.id}</td>
                <td>{test.patient_name}</td>
                <td>{test.doctor_name}</td>
                <td>{test.test_type}</td>
                <td>
                  {editingId === test.id ? (
                    <select
                      name="status"
                      value={editData.status}
                      onChange={handleChange}
                    >
                      <option value="Pending">Pending</option>
                      <option value="In Progress">In Progress</option>
                      <option value="Completed">Completed</option>
                    </select>
                  ) : (
                    test.status
                  )}
                </td>
                <td>
                  {editingId === test.id ? (
                    <textarea
                      name="result"
                      value={editData.result}
                      onChange={handleChange}
                      rows="2"
                      style={{ width: '100%', minWidth: '200px' }}
                    />
                  ) : (
                    test.result || <em>No result</em>
                  )}
                </td>
                <td>
                  {test.created_at
                    ? new Date(test.created_at).toLocaleString()
                    : 'N/A'}
                </td>
                <td className="actions-cell">
                  {editingId === test.id ? (
                    <>
                      <button
                        onClick={() => handleSave(test.id)}
                        className="btn-primary"
                      >
                        Save
                      </button>
                      <button
                        onClick={handleCancel}
                        className="btn-secondary"
                      >
                        Cancel
                      </button>
                    </>
                  ) : (
                    <button
                      onClick={() => handleEdit(test)}
                      className="btn-secondary"
                    >
                      Edit
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default TestTable
