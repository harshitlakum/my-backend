import os, sys
# add project root so "from app.main import app" works
ROOT = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
