from datetime import datetime
import uuid

def create_incident_state(raw_alert):
    """Create new incident state compatible with concurrent updates"""
    incident_id = f"INC-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
    
    return {
        # Core incident info
        "incident_id": incident_id,
        "raw_alert": raw_alert,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stage": "detected",
        "service": "",
        "severity": "",
        "description": "",
        
        # Agent results (will be populated by agents)
        "log_analysis_results": {},
        "knowledge_lookup_results": {},
        "root_cause_results": {},
        
        # Coordination (concurrent lists)
        "agents_completed": [],
        "agent_errors": [],
        
        # Decision making
        "decision": "",
        "decision_metrics": {},
        "escalation_reason": "",
        
        # Control flow
        "next": "",
        "retry_count": 0,
        "workflow_complete": False
    }

def update_stage(state, new_stage):
    """Update incident stage"""
    state["stage"] = new_stage
    return state

def should_escalate(state, confidence_threshold=0.8):
    """Check if incident should be escalated"""
    return (
        state["confidence"] < confidence_threshold or
        state["retry_count"] >= 3 or
        state.get("mitigation_failed", False)
    )