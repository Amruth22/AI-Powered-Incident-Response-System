from typing import Dict, Any
from .base_agent import BaseIncidentAgent
from services.gemini.client import parse_incident_alert
from services.email.client import send_incident_alert
from core.state import update_stage

class IncidentTriggerAgent(BaseIncidentAgent):
    """Agent for parsing incident alerts and initializing the response"""
    
    def __init__(self):
        super().__init__("incident_trigger")
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Parse alert and send initial notification"""
        # Parse alert with Gemini
        parsed = parse_incident_alert(state["raw_alert"])
        
        # Update state with parsed information
        state["service"] = parsed["service"]
        state["severity"] = parsed["severity"] 
        state["description"] = parsed["description"]
        
        # Send initial alert email
        send_incident_alert(state["incident_id"], state["service"], state["description"])
        
        # Update stage and set next step to parallel agents
        state = update_stage(state, "analyzing")
        state["next"] = "parallel_agents"
        
        self.logger.info(f"📋 Parsed: Service={parsed['service']}, Severity={parsed['severity']}")
        return state