from typing import Dict, Any
from datetime import datetime
from .base_agent import BaseIncidentAgent
from services.gemini.client import generate_root_cause
from services.email.client import send_root_cause_update
from core.config import CONFIDENCE_THRESHOLD

class RootCauseAgent(BaseIncidentAgent):
    """Agent for AI-powered root cause analysis"""
    
    def __init__(self):
        super().__init__("root_cause")
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate root cause hypothesis with confidence scoring"""
        service = state.get("service", "Unknown Service")
        description = state.get("description", "Unknown incident")
        
        # Get results from other agents (may be partial in parallel execution)
        log_results = state.get("log_analysis_results", {})
        knowledge_results = state.get("knowledge_lookup_results", {})
        
        anomalies = log_results.get("anomalies", [description])
        similar_incidents = knowledge_results.get("similar_incidents", [])
        
        # Prepare incident info for Gemini
        incident_info = f"Service: {service}, Description: {description}, Anomalies: {', '.join(anomalies)}"
        similar_text = [f"{inc.get('root_cause', 'Unknown')} -> {inc.get('solution', 'Unknown')}" 
                       for inc in similar_incidents]
        
        self.logger.info(f"🎯 Analyzing root cause for {service}...")
        
        # Generate root cause with AI
        root_cause, confidence, solution = generate_root_cause(incident_info, similar_text)
        
        results = {
            "service": service,
            "incident_info": incident_info,
            "root_cause": root_cause,
            "confidence": confidence,
            "solution": solution,
            "similar_incidents_used": len(similar_incidents),
            "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Send root cause update
        send_root_cause_update(state["incident_id"], root_cause, confidence)
        
        confidence_pct = int(confidence * 100)
        if confidence >= CONFIDENCE_THRESHOLD:
            self.logger.info(f"✅ HIGH CONFIDENCE ({confidence_pct}%) - {root_cause}")
        else:
            self.logger.warning(f"⚠️ LOW CONFIDENCE ({confidence_pct}%) - {root_cause}")
        
        # Return only agent-specific results for TRUE parallel execution
        return {
            "root_cause_results": results
        }