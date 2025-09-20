from typing import Dict, Any
from datetime import datetime
from .base_agent import BaseIncidentAgent
from services.gemini.client import simulate_mitigation
from services.email.client import send_mitigation_update
from core.state import update_stage

class MitigationAgent(BaseIncidentAgent):
    """Agent for executing automated mitigation"""
    
    def __init__(self):
        super().__init__("mitigation")
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute mitigation based on root cause analysis"""
        root_cause_results = state.get("root_cause_results", {})
        solution = root_cause_results.get("solution", "Generic restart and investigation")
        
        self.logger.info(f"⚡ Executing mitigation: {solution[:50]}...")
        
        # Update stage
        state = update_stage(state, "mitigating")
        
        # Simulate mitigation execution
        success, details = simulate_mitigation(solution)
        
        # Send mitigation update
        send_mitigation_update(state["incident_id"], success, details)
        
        if success:
            state = update_stage(state, "resolved")
            self.logger.info(f"✅ Mitigation successful: {details}")
        else:
            state["mitigation_failed"] = True
            state["escalation_reason"] = f"Mitigation failed: {details}"
            self.logger.error(f"❌ Mitigation failed: {details}")
        
        state["mitigation_results"] = {
            "solution": solution,
            "success": success,
            "details": details,
            "execution_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return state