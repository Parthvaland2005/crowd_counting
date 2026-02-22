import os
import sys

# Add the parent directory to sys.path so it can find main4.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main4 import app