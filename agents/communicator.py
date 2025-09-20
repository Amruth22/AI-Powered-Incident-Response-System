from typing import Dict, Any
from datetime import datetime
from .base_agent import BaseIncidentAgent

class CommunicatorAgent(BaseIncidentAgent):
    """Agent for final communication and workflow completion"""
    
    def __init__(self):
        super().__init__("communicator")
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final communication and complete workflow"""
        incident_id = state["incident_id"]
        stage = state.get("stage", "unknown")
        
        self.logger.info(f"📧 Final communication for {incident_id}")
        
        if stage == "resolved":
            root_cause_results = state.get("root_cause_results", {})
            root_cause = root_cause_results.get("root_cause", "Unknown")
            self.logger.info(f"✅ INCIDENT RESOLVED: {incident_id}")
            self.logger.info(f"   Service: {state.get('service', 'Unknown')}")
            self.logger.info(f"   Root Cause: {root_cause}")
        else:
            escalation_reason = state.get("escalation_reason", "Unknown reason")
            self.logger.info(f"🔴 INCIDENT ESCALATED: {incident_id}")
            self.logger.info(f"   Reason: {escalation_reason}")
        
        state["workflow_complete"] = True
        state["completion_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return state