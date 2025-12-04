import os
from app import create_app, socketio

# Obtener entorno de la variable de entorno (por defecto: 'development')
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=7000, debug=True)
