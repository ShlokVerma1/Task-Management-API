# app/routes/__init__.py

from .auth import auth_bp 
from .tasks import task_bp 

# Now in app/__init__.py you can do:
# from app.routes import auth_bp, task_bp

