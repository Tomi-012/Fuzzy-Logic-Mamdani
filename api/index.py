from app import app  # Flask app instance

# Vercel will look for a WSGI/ASGI callable named "app"
application = app
