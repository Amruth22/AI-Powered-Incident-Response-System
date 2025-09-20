import json
import re
from google import genai
from google.genai import types
from core.config import GEMINI_API_KEY, GEMINI_MODEL

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_response(prompt):
    """Generate response from Gemini"""
    try:
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        response = ""
        for chunk in client.models.generate_content_stream(model=GEMINI_MODEL, contents=contents):
            response += chunk.text
        return response.strip()
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return ""

def parse_incident_alert(raw_alert):
    """Parse incident alert and extract info"""
    prompt = f"""
    Parse this incident alert and return JSON with these fields:
    - service: affected service name
    - severity: HIGH, MEDIUM, or LOW  
    - description: brief description
    
    Alert: {raw_alert}
    
    Return only JSON:
    """
    
    response = generate_response(prompt)
    try:
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except:
        pass
    
    # Fallback
    return {
        "service": "Unknown Service",
        "severity": "MEDIUM",
        "description": raw_alert[:100]
    }

def analyze_logs(service, incident_type):
    """Generate logs and find anomalies"""
    prompt = f"""
    For a {incident_type} in {service}, generate 5 log entries and identify 2-3 anomalies.
    
    Format:
    LOGS:
    [timestamp] ERROR: message
    [timestamp] WARN: message
    
    ANOMALIES:
    • anomaly 1
    • anomaly 2
    """
    
    response = generate_response(prompt)
    
    # Extract anomalies
    anomalies = []
    anomalies_section = re.search(r'ANOMALIES:(.*?)$', response, re.DOTALL)
    if anomalies_section:
        for line in anomalies_section.group(1).strip().split('\n'):
            if line.strip().startswith('•'):
                anomalies.append(line.strip()[1:].strip())
    
    if not anomalies:
        anomalies = [f"High error rate in {service}", f"{incident_type} detected"]
    
    return anomalies

def generate_root_cause(incident_info, similar_incidents):
    """Generate root cause with confidence"""
    similar_text = "\n".join([f"- {inc}" for inc in similar_incidents])
    
    prompt = f"""
    Analyze this incident and provide root cause with confidence score.
    
    Current incident: {incident_info}
    Similar past incidents: {similar_text}
    
    Format:
    ROOT_CAUSE: specific cause
    CONFIDENCE: 0.0 to 1.0
    SOLUTION: steps to fix
    """
    
    response = generate_response(prompt)
    
    # Parse response
    root_cause = "Unknown cause"
    confidence = 0.7
    solution = "Investigate and fix"
    
    root_match = re.search(r'ROOT_CAUSE:\s*(.*?)(?:\n|$)', response)
    conf_match = re.search(r'CONFIDENCE:\s*([\d.]+)', response)
    sol_match = re.search(r'SOLUTION:\s*(.*?)$', response, re.DOTALL)
    
    if root_match:
        root_cause = root_match.group(1).strip()
    if conf_match:
        confidence = float(conf_match.group(1))
    if sol_match:
        solution = sol_match.group(1).strip()
    
    return root_cause, confidence, solution

def simulate_mitigation(solution):
    """Simulate executing mitigation"""
    prompt = f"""
    Simulate executing this solution: {solution}
    
    Return:
    SUCCESS: true/false
    DETAILS: what happened
    """
    
    response = generate_response(prompt)
    
    success = "true" in response.lower()
    details = "Mitigation executed"
    
    details_match = re.search(r'DETAILS:\s*(.*?)$', response, re.DOTALL)
    if details_match:
        details = details_match.group(1).strip()
    
    return success, details