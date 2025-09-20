from typing import Dict, Any
from datetime import datetime
from .base_agent import BaseIncidentAgent
from services.knowledge.client import load_past_resolutions, find_similar_incidents

# Load past incidents once for all agents
PAST_INCIDENTS = load_past_resolutions()

class KnowledgeLookupAgent(BaseIncidentAgent):
    """Agent for searching similar historical incidents"""
    
    def __init__(self):
        super().__init__("knowledge_lookup")
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Search for similar incidents in knowledge base"""
        service = state.get("service", "Unknown Service")
        
        # Get anomalies from log analysis (may be empty if running in parallel)
        log_results = state.get("log_analysis_results", {})
        anomalies = log_results.get("anomalies", [])
        
        # If no anomalies yet (parallel execution), use description keywords
        if not anomalies:
            description = state.get("description", "")
            anomalies = description.lower().split()[:3]  # Use first 3 words as keywords
        
        self.logger.info(f"📚 Searching knowledge base for {service} with keywords: {anomalies[:2]}...")
        
        # Search for similar incidents
        similar = find_similar_incidents(anomalies, service, PAST_INCIDENTS)
        
        results = {
            "service": service,
            "search_keywords": anomalies,
            "similar_incidents": similar,
            "similar_count": len(similar),
            "search_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.logger.info(f"✅ Found {len(similar)} similar historical incidents")
        
        # Return only agent-specific results for TRUE parallel execution
        return {
            "knowledge_lookup_results": results
        }