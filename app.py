from flask import Flask, request, jsonify
from functools import wraps
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production

# Mock user database
MOCK_USERS = {
    'admin': 'password123',
    'user1': 'mypassword',
    'testuser': 'test123'
}

def token_required(f):
    """Decorator to require valid JWT token for protected routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'Welcome to the Flask Mock Login API',
        'endpoints': {
            'POST /login': 'Login with username and password',
            'GET /protected': 'Protected route (requires token)',
            'GET /users': 'Get list of mock users (for testing)'
        }
    })

@app.route('/login', methods=['POST'])
def login():
    """Mock login endpoint"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password required!'}), 400
    
    username = data['username']
    password = data['password']
    
    # Check against mock user database
    if username in MOCK_USERS and MOCK_USERS[username] == password:
        # Generate JWT token
        token = jwt.encode({
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'message': 'Login successful!',
            'token': token,
            'username': username
        }), 200
    
    return jsonify({'message': 'Invalid username or password!'}), 401

@app.route('/protected')
@token_required
def protected(current_user):
    """Protected route that requires authentication"""
    return jsonify({
        'message': f'Hello {current_user}! This is a protected route.',
        'user': current_user,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/users', methods=['GET'])
def get_users():
    """Get list of mock users (for testing purposes)"""
    return jsonify({
        'message': 'Mock users for testing',
        'users': list(MOCK_USERS.keys()),
        'note': 'Use these usernames with their corresponding passwords to test login'
    })

@app.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """Mock logout endpoint"""
    return jsonify({
        'message': f'User {current_user} logged out successfully!',
        'note': 'In a real app, you would invalidate the token server-side'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
