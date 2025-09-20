from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging
from datetime import datetime

class BaseIncidentAgent(ABC):
    """Abstract base class for all incident response agents"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.logger = logging.getLogger(f"agent.{agent_name}")
    
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Main execution method with standardized error handling and logging"""
        incident_id = state.get("incident_id", "unknown")
        self.logger.info(f"🤖 {self.agent_name.upper()} AGENT: {incident_id}")
        
        try:
            # Execute agent-specific processing
            result = self.process(state)
            
            # Add agent to completed list for TRUE parallel execution
            agent_id = self._get_agent_id()
            result["agents_completed"] = [agent_id]  # LangGraph will merge with existing list
                
            self.logger.info(f"✅ {self.agent_name.capitalize()} analysis complete")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ {self.agent_name.capitalize()} agent error: {e}")
            # Return error state for TRUE parallel execution
            agent_id = self._get_agent_id()
            error_info = {
                "agent": self.agent_name,
                "error": str(e),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return {
                f"{self._get_result_key()}": {},
                "agents_completed": [agent_id],  # LangGraph merges with Annotated[List, add]
                "agent_errors": [error_info]     # LangGraph merges with Annotated[List, add]
            }
    
    @abstractmethod
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Agent-specific processing logic to be implemented by subclasses"""
        pass
    
    def _get_agent_id(self) -> str:
        """Get the agent identifier for completion tracking"""
        return self.agent_name.lower().replace("_agent", "").replace(" ", "_")
    
    def _get_result_key(self) -> str:
        """Get the state key for storing this agent's results"""
        agent_id = self._get_agent_id()
        return f"{agent_id}_results"