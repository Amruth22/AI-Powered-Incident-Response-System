"""
Email notification service integration
"""

from .client import (
    send_incident_alert, send_analysis_update, send_root_cause_update,
    send_mitigation_update, send_escalation_alert
)

__all__ = [
    'send_incident_alert', 'send_analysis_update', 'send_root_cause_update',
    'send_mitigation_update', 'send_escalation_alert'
]