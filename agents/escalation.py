from typing import Dict, Any
from datetime import datetime
from .base_agent import BaseIncidentAgent
from services.email.client import send_escalation_alert
from core.state import update_stage

class EscalationAgent(BaseIncidentAgent):
    """Agent for human escalation"""
    
    def __init__(self):
        super().__init__("escalation")
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Escalate incident to human operators"""
        escalation_reason = state.get("escalation_reason", "Unknown escalation reason")
        
        self.logger.info(f"🔴 Escalating incident: {escalation_reason}")
        
        # Update stage
        state = update_stage(state, "escalated")
        
        # Send escalation alert
        send_escalation_alert(state["incident_id"], escalation_reason)
        
        state["escalation_results"] = {
            "reason": escalation_reason,
            "escalated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "requires_human_intervention": True
        }
        
        return state