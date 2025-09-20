#!/usr/bin/env python3
"""
Parallel Multi-Agent Incident Response Workflow - FIXED VERSION
Properly handles concurrent state updates in LangGraph
"""

from typing import Dict, Any, List, Annotated
import logging
from datetime import datetime
from langgraph.graph import StateGraph, END
from operator import add
from typing_extensions import TypedDict

from agents import (
    IncidentTriggerAgent, LogAnalysisAgent, KnowledgeLookupAgent,
    RootCauseAgent, MitigationAgent, EscalationAgent, CommunicatorAgent,
    AgentCoordinator
)
from core.state import create_incident_state, update_stage
from core.config import CONFIDENCE_THRESHOLD, MAX_RETRIES

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("parallel_workflow")

class ParallelIncidentWorkflow:
    """Fixed Parallel Multi-Agent Incident Response Workflow using LangGraph"""
    
    def __init__(self):
        self.workflow = None
        self.logger = logger
    
    def create_workflow(self):
        """Create the TRUE parallel multi-agent incident workflow"""
        self.logger.info("🚀 Building TRUE Parallel Multi-Agent Incident Workflow...")
        
        # Define state schema for TRUE parallel execution
        class IncidentState(TypedDict):
            # Core incident info
            incident_id: str
            raw_alert: str
            timestamp: str
            stage: str
            service: str
            severity: str
            description: str
            
            # Agent results (concurrent updates allowed)
            log_analysis_results: Dict[str, Any]
            knowledge_lookup_results: Dict[str, Any]
            root_cause_results: Dict[str, Any]
            
            # Coordination (use Annotated for concurrent list updates)
            agents_completed: Annotated[List[str], add]
            agent_errors: Annotated[List[Dict], add]
            
            # Decision making
            decision: str
            decision_metrics: Dict[str, Any]
            escalation_reason: str
            
            # Control flow
            next: str
            retry_count: int
            workflow_complete: bool
        
        # Create workflow graph with proper state schema
        workflow = StateGraph(IncidentState)
        
        # Initialize agents
        incident_trigger = IncidentTriggerAgent()
        log_analysis = LogAnalysisAgent()
        knowledge_lookup = KnowledgeLookupAgent()
        root_cause = RootCauseAgent()
        mitigation = MitigationAgent()
        escalation = EscalationAgent()
        communicator = CommunicatorAgent()
        coordinator = AgentCoordinator()
        
        # Add nodes with wrapper functions to handle concurrent updates
        workflow.add_node("incident_trigger", self._wrap_agent(incident_trigger))
        workflow.add_node("log_analysis", self._wrap_agent(log_analysis))
        workflow.add_node("knowledge_lookup", self._wrap_agent(knowledge_lookup))
        workflow.add_node("root_cause", self._wrap_agent(root_cause))
        workflow.add_node("agent_coordinator", self._wrap_agent(coordinator))
        workflow.add_node("decision_maker", self.decision_maker_node)
        workflow.add_node("mitigation", self._wrap_agent(mitigation))
        workflow.add_node("escalation", self._wrap_agent(escalation))
        workflow.add_node("communicator", self._wrap_agent(communicator))
        workflow.add_node("error_handler", self.error_handler_node)
        
        # Set entry point
        workflow.set_entry_point("incident_trigger")
        
        # Define routing logic - TRUE PARALLEL EXECUTION
        workflow.add_conditional_edges("incident_trigger", self.route_to_parallel_agents)
        
        # All parallel agents route to coordinator
        workflow.add_edge("log_analysis", "agent_coordinator")
        workflow.add_edge("knowledge_lookup", "agent_coordinator")
        workflow.add_edge("root_cause", "agent_coordinator")
        
        # Coordinator waits for all agents then routes to decision maker
        workflow.add_conditional_edges("agent_coordinator", self.route_after_coordination)
        workflow.add_conditional_edges("decision_maker", self.route_after_decision)
        
        # Final nodes
        workflow.add_edge("mitigation", "communicator")
        workflow.add_edge("escalation", "communicator")
        workflow.add_edge("communicator", END)
        workflow.add_edge("error_handler", END)
        
        self.logger.info("✅ TRUE Parallel Multi-Agent Incident Workflow Created")
        self.logger.info("🔄 Flow: Trigger → [Log Analysis + Knowledge + Root Cause] → Coordinator → Decision → Action → Communicator")
        
        self.workflow = workflow.compile()
        return self.workflow
    
    def _wrap_agent(self, agent):
        """Wrap agent execution for TRUE parallel execution"""
        def wrapped_execute(state):
            try:
                result = agent.execute(state)
                # Return only the agent's specific updates for concurrent merging
                return result
            except Exception as e:
                self.logger.error(f"❌ Agent {agent.agent_name} error: {e}")
                return {
                    "agents_completed": [agent._get_agent_id()],
                    "agent_errors": [{
                        "agent": agent.agent_name,
                        "error": str(e),
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }]
                }
        return wrapped_execute
    
    def route_to_parallel_agents(self, state: Dict[str, Any]):
        """Route to TRUE parallel agents after incident trigger"""
        next_step = state.get("next", "end")
        
        if next_step == "parallel_agents":
            # 🚀 LAUNCH ALL AGENTS IN TRUE PARALLEL
            self.logger.info("🚀 Launching TRUE PARALLEL agents: Log Analysis + Knowledge Lookup + Root Cause")
            return ["log_analysis", "knowledge_lookup", "root_cause"]
        elif next_step == "error_handler":
            return "error_handler"
        else:
            return END
    
    def route_after_coordination(self, state: Dict[str, Any]):
        """Route after coordination"""
        if state.get("error"):
            return "error_handler"
        else:
            return "decision_maker"
    
    def route_after_decision(self, state: Dict[str, Any]):
        """Route after decision making"""
        next_step = state.get("next", "end")
        
        if next_step == "mitigation":
            return "mitigation"
        elif next_step == "escalation":
            return "escalation"
        elif next_step == "error_handler":
            return "error_handler"
        else:
            return END
    
    def decision_maker_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Decision maker node - analyzes all results and makes routing decision"""
        self.logger.info(f"🎯 DECISION MAKER: {state['incident_id']}")
        
        try:
            # Extract results from agents
            log_results = state.get("log_analysis_results", {})
            knowledge_results = state.get("knowledge_lookup_results", {})
            root_cause_results = state.get("root_cause_results", {})
            
            # Get confidence and anomalies
            confidence = root_cause_results.get("confidence", 0.0)
            anomalies_found = len(log_results.get("anomalies", [])) > 0
            similar_incidents = len(knowledge_results.get("similar_incidents", [])) > 0
            retry_count = state.get("retry_count", 0)
            
            # Decision logic based on multiple factors
            decision = "auto_mitigation"
            escalation_reason = ""
            
            # Check for escalation conditions
            if retry_count >= MAX_RETRIES:
                decision = "escalation"
                escalation_reason = f"Max retries ({MAX_RETRIES}) reached without finding anomalies"
            elif not anomalies_found:
                decision = "escalation"
                escalation_reason = "No anomalies detected in log analysis"
            elif confidence < CONFIDENCE_THRESHOLD:
                decision = "escalation"
                escalation_reason = f"Low confidence ({confidence:.2f}) in root cause analysis"
            elif not similar_incidents:
                decision = "escalation"
                escalation_reason = "No similar historical incidents found for guidance"
            
            # Log decision
            if decision == "auto_mitigation":
                self.logger.info(f"✅ HIGH CONFIDENCE ({confidence:.2f}) - Proceeding with auto-mitigation")
                next_step = "mitigation"
            else:
                self.logger.info(f"🔴 ESCALATING - {escalation_reason}")
                next_step = "escalation"
            
            # Update state with decision
            return {
                **state,
                "decision": decision,
                "decision_metrics": {
                    "confidence": confidence,
                    "anomalies_found": anomalies_found,
                    "similar_incidents_count": len(knowledge_results.get("similar_incidents", [])),
                    "retry_count": retry_count,
                    "escalation_reason": escalation_reason
                },
                "escalation_reason": escalation_reason,
                "stage": "decision_complete",
                "next": next_step
            }
            
        except Exception as e:
            self.logger.error(f"❌ Decision maker error: {e}")
            return {
                **state,
                "error": str(e),
                "next": "error_handler",
                "stage": "decision_error"
            }
    
    def error_handler_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Error handler node implementation"""
        from services.email.client import send_escalation_alert
        
        error_message = state.get("error", "Unknown error")
        self.logger.error(f"❌ ERROR HANDLER: {error_message}")
        
        try:
            # Send error notification
            incident_id = state.get("incident_id", "unknown")
            send_escalation_alert(incident_id, f"System Error: {error_message}")
            
            return {
                **state,
                "stage": "error_handled",
                "workflow_complete": True,
                "error_handled": True
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error handler failed: {e}")
            return {
                **state,
                "stage": "error_handling_failed",
                "workflow_complete": True
            }
    
    def execute(self, raw_alert: str) -> Dict[str, Any]:
        """Execute the parallel workflow for an incident"""
        self.logger.info("🚀 STARTING TRUE PARALLEL MULTI-AGENT INCIDENT RESPONSE")
        self.logger.info(f"📥 Alert: {raw_alert}")
        self.logger.info("=" * 60)
        
        if not self.workflow:
            self.create_workflow()
        
        # Create initial state
        state = create_incident_state(raw_alert)
        
        # Execute workflow
        self.logger.info("⚡ Executing TRUE PARALLEL MULTI-AGENT workflow...")
        final_state = self.workflow.invoke(state)
        
        # Display results
        self.logger.info("=" * 60)
        self.logger.info("🏁 TRUE PARALLEL WORKFLOW COMPLETED")
        self.logger.info(f"📋 Incident: {final_state['incident_id']}")
        self.logger.info(f"📊 Status: {final_state['stage'].upper()}")
        
        # Display agent completion status
        if "agents_completed" in final_state:
            completed_agents = final_state["agents_completed"]
            self.logger.info(f"🤖 Agents Completed: {', '.join(set(completed_agents))}")
        
        # Display decision metrics
        if "decision_metrics" in final_state:
            metrics = final_state["decision_metrics"]
            self.logger.info(f"🎯 Decision: {final_state.get('decision', 'unknown').upper()}")
            self.logger.info(f"📈 Confidence: {metrics.get('confidence', 0):.2f}")
            self.logger.info(f"🔍 Anomalies Found: {metrics.get('anomalies_found', False)}")
            self.logger.info(f"📚 Similar Incidents: {metrics.get('similar_incidents_count', 0)}")
            
            if metrics.get("escalation_reason"):
                self.logger.info(f"🔴 Escalation Reason: {metrics['escalation_reason']}")
        
        return final_state

def process_incident(raw_alert: str):
    """Process an incident through the parallel workflow"""
    workflow = ParallelIncidentWorkflow()
    return workflow.execute(raw_alert)