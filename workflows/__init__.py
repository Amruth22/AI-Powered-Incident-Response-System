"""
LangGraph workflow definitions for incident response system
"""

from .parallel_workflow import ParallelIncidentWorkflow, process_incident

__all__ = ['ParallelIncidentWorkflow', 'process_incident']