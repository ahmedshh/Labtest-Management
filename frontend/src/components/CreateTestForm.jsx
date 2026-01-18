import React, { useState } from 'react'
import axios from 'axios'
import './CreateTestForm.css'

const CreateTestForm = ({ onTestCreated, onCancel }) => {
  const [formData, setFormData] = useState({
    patient_name: '',
    doctor_name: '',
    test_type: 'Blood',
    status: 'Pending',
    result: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await axios.post(`${API_BASE_URL}/tests`, formData)
      setFormData({
        patient_name: '',
        doctor_name: '',
        test_type: 'Blood',
        status: 'Pending',
        result: ''
      })
      onTestCreated()
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create test')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="form-container">
      <h2>Create Lab Test</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="patient_name">Patient Name:</label>
          <input
            type="text"
            id="patient_name"
            name="patient_name"
            value={formData.patient_name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="doctor_name">Doctor Name:</label>
          <input
            type="text"
            id="doctor_name"
            name="doctor_name"
            value={formData.doctor_name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="test_type">Test Type:</label>
          <select
            id="test_type"
            name="test_type"
            value={formData.test_type}
            onChange={handleChange}
            required
          >
            <option value="Blood">Blood</option>
            <option value="Urine">Urine</option>
            <option value="X-Ray">X-Ray</option>
            <option value="MRI">MRI</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="status">Status:</label>
          <select
            id="status"
            name="status"
            value={formData.status}
            onChange={handleChange}
            required
          >
            <option value="Pending">Pending</option>
            <option value="In Progress">In Progress</option>
            <option value="Completed">Completed</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="result">Result (optional):</label>
          <textarea
            id="result"
            name="result"
            value={formData.result}
            onChange={handleChange}
            rows="4"
          />
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="form-actions">
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Creating...' : 'Create Test'}
          </button>
          <button type="button" onClick={onCancel} className="btn-secondary">
            Cancel
          </button>
        </div>
      </form>
    </div>
  )
}

export default CreateTestForm
