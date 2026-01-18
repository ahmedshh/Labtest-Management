from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Determine if running in production (Docker) or development
IS_PRODUCTION = os.path.exists('/app/static')

app = Flask(__name__, static_folder='/app/static' if IS_PRODUCTION else None)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///lab_tests.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS for React frontend (only in development)
if not IS_PRODUCTION:
    CORS(app)

db = SQLAlchemy(app)


# Database Model
class LabTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    doctor_name = db.Column(db.String(100), nullable=False)
    test_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    result = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_name': self.patient_name,
            'doctor_name': self.doctor_name,
            'test_type': self.test_type,
            'status': self.status,
            'result': self.result,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# Initialize database
with app.app_context():
    db.create_all()


# Dummy authentication - simple check for demo purposes
VALID_CREDENTIALS = {
    'username': 'admin',
    'password': 'password123'
}


@app.route('/login', methods=['POST'])
def login():
    """
    Dummy authentication endpoint for demo purposes.
    Accepts username and password, returns success if credentials match.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == VALID_CREDENTIALS['username'] and password == VALID_CREDENTIALS['password']:
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': 'dummy_token_for_demo'
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid credentials'
        }), 401


@app.route('/tests', methods=['POST'])
def create_test():
    """
    Create a new lab test.
    Required fields: patient_name, doctor_name, test_type, status
    Optional: result
    """
    data = request.get_json()

    # Validation
    required_fields = ['patient_name', 'doctor_name', 'test_type', 'status']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    # Validate test_type
    valid_test_types = ['Blood', 'Urine', 'X-Ray', 'MRI']
    if data.get('test_type') not in valid_test_types:
        return jsonify({'error': f'test_type must be one of: {", ".join(valid_test_types)}'}), 400

    # Validate status
    valid_statuses = ['Pending', 'In Progress', 'Completed']
    if data.get('status') not in valid_statuses:
        return jsonify({'error': f'status must be one of: {", ".join(valid_statuses)}'}), 400

    # Create new lab test
    lab_test = LabTest(
        patient_name=data['patient_name'],
        doctor_name=data['doctor_name'],
        test_type=data['test_type'],
        status=data['status'],
        result=data.get('result', '')
    )

    db.session.add(lab_test)
    db.session.commit()

    return jsonify(lab_test.to_dict()), 201


@app.route('/tests', methods=['GET'])
def get_tests():
    """
    Get all lab tests.
    Optionally filter by status using query parameter: ?status=Pending
    """
    status_filter = request.args.get('status')
    
    if status_filter:
        tests = LabTest.query.filter_by(status=status_filter).all()
    else:
        tests = LabTest.query.all()

    return jsonify([test.to_dict() for test in tests]), 200


@app.route('/tests/<int:test_id>', methods=['PUT'])
def update_test(test_id):
    """
    Update an existing lab test.
    Can update: status, result, patient_name, doctor_name, test_type
    """
    test = LabTest.query.get_or_404(test_id)
    data = request.get_json()

    # Validate test_type if provided
    if 'test_type' in data and data['test_type'] not in ['Blood', 'Urine', 'X-Ray', 'MRI']:
        return jsonify({'error': 'Invalid test_type'}), 400

    # Validate status if provided
    if 'status' in data and data['status'] not in ['Pending', 'In Progress', 'Completed']:
        return jsonify({'error': 'Invalid status'}), 400

    # Update fields
    if 'patient_name' in data:
        test.patient_name = data['patient_name']
    if 'doctor_name' in data:
        test.doctor_name = data['doctor_name']
    if 'test_type' in data:
        test.test_type = data['test_type']
    if 'status' in data:
        test.status = data['status']
    if 'result' in data:
        test.result = data['result']

    db.session.commit()

    return jsonify(test.to_dict()), 200


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for CI/CD and monitoring"""
    return jsonify({'status': 'healthy'}), 200


# Serve React app in production (Docker)
if IS_PRODUCTION:
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react_app(path):
        """Serve React app static files"""
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
