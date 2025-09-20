from typing import Dict, Any
from datetime import datetime
from .base_agent import BaseIncidentAgent

class AgentCoordinator(BaseIncidentAgent):
    """Coordinator agent that waits for all parallel agents to complete"""
    
    def __init__(self):
        super().__init__("agent_coordinator")
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate results from all parallel agents"""
        incident_id = state["incident_id"]
        
        # Check which agents have completed
        completed_agents = state.get("agents_completed", [])
        expected_agents = ["log_analysis", "knowledge_lookup", "root_cause"]
        
        self.logger.info(f"🔄 Coordinating results for {incident_id}")
        self.logger.info(f"   Completed agents: {completed_agents}")
        self.logger.info(f"   Expected agents: {expected_agents}")
        
        # Verify all expected agents have completed
        missing_agents = [agent for agent in expected_agents if agent not in completed_agents]
        
        if missing_agents:
            self.logger.warning(f"⏳ Still waiting for: {missing_agents}")
            # This shouldn't happen in the workflow, but handle gracefully
            state["coordination_status"] = "waiting"
            state["missing_agents"] = missing_agents
        else:
            self.logger.info("✅ All parallel agents completed successfully")
            state["coordination_status"] = "complete"
            state["next"] = "decision_maker"
        
        # Aggregate any errors from parallel agents
        agent_errors = state.get("agent_errors", [])
        if agent_errors:
            self.logger.warning(f"⚠️ {len(agent_errors)} agent errors occurred")
            for error in agent_errors:
                self.logger.warning(f"   {error['agent']}: {error['error']}")
        
        state["coordination_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return state