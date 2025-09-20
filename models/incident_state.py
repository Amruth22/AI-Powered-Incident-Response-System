from typing import Dict, Any, List, Optional
from datetime import datetime

class IncidentState:
    """Data model for incident state"""
    
    def __init__(self, incident_id: str, raw_alert: str):
        self.incident_id = incident_id
        self.raw_alert = raw_alert
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.stage = "detected"
        self.service = ""
        self.severity = ""
        self.description = ""
        
        # Agent results
        self.log_analysis_results = {}
        self.knowledge_lookup_results = {}
        self.root_cause_results = {}
        
        # Coordination
        self.agents_completed = []
        self.agent_errors = []
        
        # Decision making
        self.decision = ""
        self.decision_metrics = {}
        self.escalation_reason = ""
        
        # Control flow
        self.next = ""
        self.retry_count = 0
        self.workflow_complete = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for LangGraph state"""
        return {
            "incident_id": self.incident_id,
            "raw_alert": self.raw_alert,
            "timestamp": self.timestamp,
            "stage": self.stage,
            "service": self.service,
            "severity": self.severity,
            "description": self.description,
            "log_analysis_results": self.log_analysis_results,
            "knowledge_lookup_results": self.knowledge_lookup_results,
            "root_cause_results": self.root_cause_results,
            "agents_completed": self.agents_completed,
            "agent_errors": self.agent_errors,
            "decision": self.decision,
            "decision_metrics": self.decision_metrics,
            "escalation_reason": self.escalation_reason,
            "next": self.next,
            "retry_count": self.retry_count,
            "workflow_complete": self.workflow_complete
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IncidentState':
        """Create from dictionary"""
        instance = cls(data["incident_id"], data["raw_alert"])
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        return instance