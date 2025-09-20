"""
Core configuration and state management for incident response system
"""

from .config import *
from .state import create_incident_state, update_stage, should_escalate

__all__ = ['create_incident_state', 'update_stage', 'should_escalate']