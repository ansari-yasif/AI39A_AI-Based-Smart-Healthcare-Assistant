"""
run.py — Application Entry Point
=================================
This is the main entry point to start the VitaPulse Flask server.
Run with: python run.py
"""

from app import create_app

# Create the Flask application using the factory pattern
app = create_app()

if __name__ == '__main__':
    # Debug mode enabled for development — disable in production
    app.run(debug=True, host='0.0.0.0', port=5000)