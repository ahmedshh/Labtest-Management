# Laboratory Information System (LIS)

A full-stack Laboratory Information System demo built with React (Vite), Flask, SQLite, Docker, and CI/CD using GitHub Actions.

## 🏗️ Architecture Overview

```
┌─────────────┐
│   React     │  Frontend (Vite)
│  Frontend   │  - Login Page
│             │  - Dashboard with Stats
└──────┬──────┘  - Create Test Form
       │         - Test Management Table
       │ HTTP
       ▼
┌─────────────┐
│   Flask     │  Backend (REST API)
│   Backend   │  - POST /login
└──────┬──────┘  - POST /tests
       │         - GET /tests
       │         - PUT /tests/<id>
       │
       ▼
┌─────────────┐
│   SQLite    │  Database
│  Database   │  - lab_tests table
└─────────────┘
```

## 📁 Project Structure

```
lis/
├── backend/                 # Flask REST API
│   ├── app.py              # Main Flask application
│   └── requirements.txt    # Python dependencies
├── frontend/               # React application (Vite)
│   ├── src/
│   │   ├── components/    # React components
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── CreateTestForm.jsx
│   │   │   └── TestTable.jsx
│   │   ├── App.jsx        # Main app component
│   │   └── main.jsx       # Entry point
│   ├── package.json       # Node dependencies
│   └── vite.config.js     # Vite configuration
├── tests/                  # Backend tests
│   ├── test_api.py        # PyTest test cases
│   └── requirements.txt   # Test dependencies
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions CI/CD pipeline
├── Dockerfile             # Multi-stage Docker build
├── .dockerignore          # Docker ignore patterns
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (optional, for containerized deployment)

### Local Development Setup

#### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Flask server
python app.py
```

The backend will start on `http://localhost:5000`

#### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will start on `http://localhost:3000`

#### 3. Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Login credentials:
  - Username: `admin`
  - Password: `password123`

### Docker Deployment

Build and run using Docker:

```bash
# Build Docker image
docker build -t lis:latest .

# Run container
docker run -d -p 5000:5000 --name lis-app lis:latest
```

Access the application at `http://localhost:5000`

## 📋 API Endpoints

### Authentication

- **POST** `/login`
  - Request body: `{ "username": "admin", "password": "password123" }`
  - Returns: `{ "success": true, "token": "dummy_token" }`

### Lab Tests

- **POST** `/tests` - Create a new lab test
  - Required fields: `patient_name`, `doctor_name`, `test_type`, `status`
  - Optional: `result`
  - Example:
    ```json
    {
      "patient_name": "John Doe",
      "doctor_name": "Dr. Smith",
      "test_type": "Blood",
      "status": "Pending",
      "result": ""
    }
    ```

- **GET** `/tests` - Get all lab tests
  - Optional query: `?status=Pending` (filter by status)

- **PUT** `/tests/<id>` - Update a lab test
  - Can update: `status`, `result`, `patient_name`, `doctor_name`, `test_type`

- **GET** `/health` - Health check endpoint

## 🧪 Testing

### Backend Tests

```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=backend --cov-report=html
```

### Frontend Tests

```bash
cd frontend
npm run build  # Basic build test
```

## 🔄 CI/CD Pipeline (GitHub Actions)

The CI/CD pipeline is defined in `.github/workflows/ci.yml` and consists of three main jobs:

### Pipeline Stages

1. **Backend Test & Lint** (`backend-test`)
   - ✅ Checkout code
   - ✅ Setup Python 3.11
   - ✅ Install backend dependencies
   - ✅ Run PyTest with coverage
   - ✅ Lint Python code with flake8

2. **Frontend Build** (`frontend-build`)
   - ✅ Checkout code
   - ✅ Setup Node.js 18
   - ✅ Install frontend dependencies
   - ✅ Build React application (`npm run build`)
   - ✅ Verify build output

3. **Docker Build** (`docker-build`)
   - ✅ Checkout code
   - ✅ Setup Docker Buildx
   - ✅ Build multi-stage Docker image
   - ✅ Test Docker image (health check)

### Pipeline Triggers

The pipeline runs on:
- Push to `main`, `master`, or `develop` branches
- Pull requests to `main`, `master`, or `develop` branches

### Viewing Pipeline Status

1. Go to your GitHub repository
2. Click on "Actions" tab
3. View workflow runs and their status

## 🐳 Docker Multi-Stage Build

The Dockerfile uses a multi-stage build process:

**Stage 1: Frontend Builder**
- Uses `node:18-alpine` base image
- Installs npm dependencies
- Builds React production bundle

**Stage 2: Production Server**
- Uses `python:3.11-slim` base image
- Installs Python dependencies
- Copies backend code
- Copies built frontend from Stage 1
- Serves both Flask API and React static files

This approach results in a smaller final image (~200MB vs ~500MB) by excluding Node.js and build tools from production.

## 🗄️ Database Schema

### lab_tests Table

| Column      | Type        | Description                    |
|-------------|-------------|--------------------------------|
| id          | INTEGER     | Primary key                    |
| patient_name| VARCHAR(100)| Patient name                   |
| doctor_name | VARCHAR(100)| Doctor name                    |
| test_type   | VARCHAR(50) | Test type (Blood/Urine/X-Ray/MRI) |
| status      | VARCHAR(50) | Status (Pending/In Progress/Completed) |
| result      | TEXT        | Test result                    |
| created_at  | DATETIME    | Creation timestamp             |

## 🛠️ Technologies Used

- **Frontend**: React 18, Vite, React Router, Axios
- **Backend**: Flask, Flask-SQLAlchemy, Flask-CORS
- **Database**: SQLite
- **Testing**: PyTest
- **CI/CD**: GitHub Actions
- **Containerization**: Docker (multi-stage build)
- **Linting**: flake8 (Python)

## 📝 Development Notes

- The authentication is a simple dummy implementation for demo purposes
- SQLite database is created automatically on first run
- CORS is enabled for React frontend development
- Frontend API calls can be configured via `VITE_API_URL` environment variable

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure tests pass
5. Submit a pull request

## 📄 License

This is a demo project for educational purposes.
