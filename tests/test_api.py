import pytest
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app, db, LabTest


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


def test_login_success(client):
    """Test successful login with valid credentials"""
    response = client.post('/login', 
                          json={'username': 'admin', 'password': 'password123'},
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    assert 'token' in data


def test_login_failure(client):
    """Test login failure with invalid credentials"""
    response = client.post('/login',
                          json={'username': 'admin', 'password': 'wrong'},
                          content_type='application/json')
    assert response.status_code == 401
    data = response.get_json()
    assert data['success'] == False


def test_create_test_success(client):
    """Test creating a lab test with valid data"""
    response = client.post('/tests',
                          json={
                              'patient_name': 'John Doe',
                              'doctor_name': 'Dr. Smith',
                              'test_type': 'Blood',
                              'status': 'Pending',
                              'result': ''
                          },
                          content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert data['patient_name'] == 'John Doe'
    assert data['test_type'] == 'Blood'
    assert data['status'] == 'Pending'


def test_create_test_missing_fields(client):
    """Test creating a lab test with missing required fields"""
    response = client.post('/tests',
                          json={
                              'patient_name': 'John Doe',
                              'doctor_name': 'Dr. Smith'
                          },
                          content_type='application/json')
    assert response.status_code == 400


def test_create_test_invalid_test_type(client):
    """Test creating a lab test with invalid test_type"""
    response = client.post('/tests',
                          json={
                              'patient_name': 'John Doe',
                              'doctor_name': 'Dr. Smith',
                              'test_type': 'InvalidType',
                              'status': 'Pending'
                          },
                          content_type='application/json')
    assert response.status_code == 400


def test_get_tests_empty(client):
    """Test getting all tests when database is empty"""
    response = client.get('/tests')
    assert response.status_code == 200
    data = response.get_json()
    assert data == []


def test_get_tests_with_data(client):
    """Test getting all tests with existing data"""
    # Create a test
    test = LabTest(
        patient_name='Jane Doe',
        doctor_name='Dr. Johnson',
        test_type='Urine',
        status='Completed',
        result='Normal'
    )
    with app.app_context():
        db.session.add(test)
        db.session.commit()

    response = client.get('/tests')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['patient_name'] == 'Jane Doe'


def test_get_tests_filtered_by_status(client):
    """Test getting tests filtered by status"""
    # Create multiple tests with different statuses
    tests = [
        LabTest(patient_name='Patient 1', doctor_name='Dr. A', test_type='Blood', status='Pending'),
        LabTest(patient_name='Patient 2', doctor_name='Dr. B', test_type='Urine', status='Completed'),
        LabTest(patient_name='Patient 3', doctor_name='Dr. C', test_type='X-Ray', status='Pending'),
    ]
    with app.app_context():
        for test in tests:
            db.session.add(test)
        db.session.commit()

    response = client.get('/tests?status=Pending')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert all(test['status'] == 'Pending' for test in data)


def test_update_test_success(client):
    """Test updating a lab test"""
    # Create a test
    test = LabTest(
        patient_name='Original Patient',
        doctor_name='Dr. Original',
        test_type='Blood',
        status='Pending',
        result=''
    )
    with app.app_context():
        db.session.add(test)
        db.session.commit()
        test_id = test.id

    # Update the test
    response = client.put(f'/tests/{test_id}',
                         json={'status': 'Completed', 'result': 'All clear'},
                         content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'Completed'
    assert data['result'] == 'All clear'


def test_update_test_not_found(client):
    """Test updating a non-existent test"""
    response = client.put('/tests/999',
                         json={'status': 'Completed'},
                         content_type='application/json')
    assert response.status_code == 404


def test_update_test_invalid_status(client):
    """Test updating a test with invalid status"""
    test = LabTest(
        patient_name='Test Patient',
        doctor_name='Dr. Test',
        test_type='Blood',
        status='Pending'
    )
    with app.app_context():
        db.session.add(test)
        db.session.commit()
        test_id = test.id

    response = client.put(f'/tests/{test_id}',
                         json={'status': 'InvalidStatus'},
                         content_type='application/json')
    assert response.status_code == 400


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
