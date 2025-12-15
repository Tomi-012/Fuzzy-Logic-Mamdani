from app import app  # Flask app instance

# Vercel will look for a WSGI/ASGI callable named "app" or "application"
# Using both for compatibility
application = app

# Vercel serverless function handler
def handler(request):
    return app(request.environ, lambda status, headers: None)
