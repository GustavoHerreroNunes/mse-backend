import sys
import os

# Ensure the project root is on sys.path so that
# `reportlab_pages.*` imports resolve correctly when
# running pytest from any working directory.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
