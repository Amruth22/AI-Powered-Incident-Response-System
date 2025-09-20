def load_past_resolutions():
    """Load incidents from past_resolutions.txt"""
    incidents = []
    try:
        with open('data/past_resolutions.txt', 'r') as f:
            content = f.read()
        
        # Split by INCIDENT blocks
        blocks = content.split('INCIDENT: ')[1:]  # Skip first empty split
        
        for block in blocks:
            lines = block.strip().split('\n')
            incident = {}
            
            for line in lines:
                if line.startswith('SERVICE:'):
                    incident['service'] = line.replace('SERVICE:', '').strip()
                elif line.startswith('ANOMALY:'):
                    incident['anomaly'] = line.replace('ANOMALY:', '').strip()
                elif line.startswith('ROOT_CAUSE:'):
                    incident['root_cause'] = line.replace('ROOT_CAUSE:', '').strip()
                elif line.startswith('SOLUTION:'):
                    incident['solution'] = line.replace('SOLUTION:', '').strip()
                elif line.startswith('KEYWORDS:'):
                    incident['keywords'] = line.replace('KEYWORDS:', '').strip().split(', ')
            
            if incident:
                incidents.append(incident)
        
        print(f"✅ Loaded {len(incidents)} past incidents")
        return incidents
        
    except Exception as e:
        print(f"❌ Failed to load past resolutions: {e}")
        return []

def find_similar_incidents(anomalies, service, past_incidents):
    """Find similar incidents based on anomalies and service"""
    similar = []
    
    for incident in past_incidents:
        score = 0
        
        # Check service match
        if service.lower() in incident.get('service', '').lower():
            score += 0.5
        
        # Check anomaly keywords
        incident_keywords = incident.get('keywords', [])
        for anomaly in anomalies:
            anomaly_words = anomaly.lower().split()
            for word in anomaly_words:
                for keyword in incident_keywords:
                    if word in keyword.lower():
                        score += 0.2
        
        if score > 0.3:  # Minimum similarity threshold
            similar.append({
                'incident': incident,
                'score': score
            })
    
    # Sort by score and return top 3
    similar.sort(key=lambda x: x['score'], reverse=True)
    return [s['incident'] for s in similar[:3]]