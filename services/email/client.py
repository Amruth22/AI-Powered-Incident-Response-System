import smtplib
from email.mime.text import MIMEText
from core.config import EMAIL_FROM, EMAIL_PASSWORD, EMAIL_TO, SMTP_SERVER, SMTP_PORT

def send_email(subject, body):
    """Send email notification"""
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email sent: {subject}")
        return True
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False

def send_incident_alert(incident_id, service, description):
    """Send initial incident alert"""
    subject = f"🚨 INCIDENT ALERT: {incident_id} - {service}"
    body = f"""
INCIDENT DETECTED
================
Incident ID: {incident_id}
Service: {service}
Description: {description}

Status: Investigation started
    """
    return send_email(subject, body)

def send_analysis_update(incident_id, anomalies):
    """Send log analysis update"""
    subject = f"🔍 LOG ANALYSIS: {incident_id}"
    body = f"""
LOG ANALYSIS COMPLETE
====================
Incident ID: {incident_id}

ANOMALIES DETECTED:
{chr(10).join(['• ' + a for a in anomalies])}

Status: Searching knowledge base
    """
    return send_email(subject, body)

def send_root_cause_update(incident_id, root_cause, confidence):
    """Send root cause analysis"""
    subject = f"🎯 ROOT CAUSE: {incident_id} - {int(confidence*100)}% Confidence"
    body = f"""
ROOT CAUSE ANALYSIS
==================
Incident ID: {incident_id}

ROOT CAUSE: {root_cause}
CONFIDENCE: {int(confidence*100)}%

Status: {'Proceeding with mitigation' if confidence > 0.8 else 'Escalating to human'}
    """
    return send_email(subject, body)

def send_mitigation_update(incident_id, success, details):
    """Send mitigation results"""
    status = "SUCCESS" if success else "FAILED"
    subject = f"⚡ MITIGATION: {incident_id} - {status}"
    body = f"""
MITIGATION EXECUTED
==================
Incident ID: {incident_id}

STATUS: {status}
DETAILS: {details}

Final Status: {'Incident resolved' if success else 'Escalating to human'}
    """
    return send_email(subject, body)

def send_escalation_alert(incident_id, reason):
    """Send human escalation alert"""
    subject = f"🔴 ESCALATION: {incident_id} - Manual Intervention Required"
    body = f"""
HUMAN ESCALATION REQUIRED
========================
Incident ID: {incident_id}

ESCALATION REASON: {reason}

⚠️ IMMEDIATE ATTENTION REQUIRED ⚠️
Please investigate and take manual action.
    """
    return send_email(subject, body)