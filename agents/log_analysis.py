from typing import Dict, Any
from datetime import datetime
from .base_agent import BaseIncidentAgent
from services.gemini.client import analyze_logs
from services.email.client import send_analysis_update

class LogAnalysisAgent(BaseIncidentAgent):
    """Agent for log analysis and anomaly detection"""
    
    def __init__(self):
        super().__init__("log_analysis")
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze logs and detect anomalies with retry logic"""
        service = state.get("service", "Unknown Service")
        description = state.get("description", "Unknown incident")
        retry_count = state.get("retry_count", 0)
        
        self.logger.info(f"🔍 Analyzing logs for {service} (Attempt {retry_count + 1})")
        
        # Generate logs and find anomalies
        anomalies = analyze_logs(service, description)
        
        results = {
            "service": service,
            "anomalies": anomalies,
            "retry_count": retry_count,
            "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if anomalies and len(anomalies) > 0:
            self.logger.info(f"✅ Found {len(anomalies)} anomalies: {', '.join(anomalies[:2])}...")
            send_analysis_update(state["incident_id"], anomalies)
            results["anomalies_found"] = True
        else:
            self.logger.warning(f"⚠️ No anomalies found (attempt {retry_count + 1})")
            results["anomalies_found"] = False
            # Increment retry count for decision making
            state["retry_count"] = retry_count + 1
        
        return {
            **state,
            "log_analysis_results": results
        }