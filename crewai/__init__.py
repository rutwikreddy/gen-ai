"""
__init__.py - CrewAI Incident Management Package
"""

from crew import create_crew
from config import ORG_CONTEXT, MODEL

__version__ = "1.0.0"
__all__ = ["create_crew", "ORG_CONTEXT", "MODEL"]
