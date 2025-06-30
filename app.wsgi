import os
import sys

# Add the project path
sys.path.insert(0, os.path.dirname(__file__))

# ✅ Load environment variables before anything else
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Now import the app
from app import create_app
application = create_app()
