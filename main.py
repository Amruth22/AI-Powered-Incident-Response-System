#!/usr/bin/env python3
"""
AI-Powered Incident Response System
Professional parallel multi-agent system with LangGraph orchestration
"""

import sys
import argparse
from datetime import datetime

from workflows import process_incident
from utils.logging_utils import setup_logging

def main():
    """Main application entry point"""
    
    parser = argparse.ArgumentParser(
        description="AI-Powered Incident Response System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py "Payment API database timeout"
  python main.py --demo
  python main.py --help
        """
    )
    
    # Demo option
    parser.add_argument(
        "--demo", "-d", 
        action="store_true",
        help="Run interactive demo with sample scenarios"
    )
    
    # Alert text (positional argument)
    parser.add_argument(
        "alert", 
        nargs="*", 
        help="Incident alert text to process"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging("INFO", "logs/incident_response.log")
    
    # Handle different modes
    if args.demo:
        run_demo()
    elif args.alert:
        alert_text = " ".join(args.alert)
        run_incident_response(alert_text)
    else:
        # Interactive mode
        run_interactive_mode()

def run_incident_response(alert_text: str):
    """Run the parallel multi-agent workflow"""
    print("🚀 TRUE PARALLEL MULTI-AGENT INCIDENT RESPONSE")
    print("=" * 50)
    start_time = datetime.now()
    
    try:
        result = process_incident(alert_text)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n⏱️ Workflow completed in {duration:.2f} seconds")
        print_workflow_summary(result)
        
    except Exception as e:
        print(f"❌ Workflow error: {e}")
        import traceback
        traceback.print_exc()

def run_demo():
    """Run interactive demo with sample scenarios"""
    print("🎬 INTERACTIVE DEMO - TRUE Parallel AI-Powered Incident Response")
    print("=" * 55)
    
    scenarios = [
        {
            "name": "Database Timeout",
            "alert": "Payment API experiencing database connection timeouts and high error rates",
            "description": "High confidence scenario - should auto-resolve"
        },
        {
            "name": "Memory Leak",
            "alert": "Auth Service showing memory leak patterns and degraded performance",
            "description": "Medium confidence scenario - may require escalation"
        },
        {
            "name": "Network Issues",
            "alert": "Load balancer reporting uneven traffic distribution and connection failures",
            "description": "Complex scenario - likely escalation"
        },
        {
            "name": "Unknown Service",
            "alert": "Critical system failure in unknown microservice with no clear symptoms",
            "description": "Low confidence scenario - definite escalation"
        }
    ]
    
    print("Available Demo Scenarios:")
    for i, scenario in enumerate(scenarios, 1):
        print(f"  {i}. {scenario['name']} - {scenario['description']}")
    
    print("  5. Custom Alert - Enter your own incident")
    print("  0. Exit")
    
    while True:
        try:
            choice = input("\nSelect scenario (0-5): ").strip()
            
            if choice == "0":
                print("👋 Demo completed!")
                break
            elif choice in ["1", "2", "3", "4"]:
                scenario = scenarios[int(choice) - 1]
                print(f"\n🎯 Running scenario: {scenario['name']}")
                print(f"Alert: {scenario['alert']}")
                print("-" * 50)
                run_incident_response(scenario['alert'])
                    
            elif choice == "5":
                custom_alert = input("Enter custom incident alert: ").strip()
                if custom_alert:
                    run_incident_response(custom_alert)
                else:
                    print("❌ No alert provided")
                    
            else:
                print("❌ Invalid choice. Please select 0-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted!")
            break
        except Exception as e:
            print(f"❌ Demo error: {e}")

def run_interactive_mode():
    """Interactive mode for single incident processing"""
    print("🚨 TRUE Parallel AI-Powered Incident Response System")
    print("=" * 45)
    print("Options:")
    print("  1. Process Incident Alert")
    print("  2. Interactive Demo")
    print("  0. Exit")
    
    choice = input("\nSelect option (0-2): ").strip()
    
    if choice == "0":
        print("👋 Goodbye!")
        return
    elif choice == "1":
        alert = input("Enter incident alert: ").strip()
        if alert:
            run_incident_response(alert)
        else:
            print("❌ No alert provided")
    elif choice == "2":
        run_demo()
    else:
        print("❌ Invalid choice")

def print_workflow_summary(result: dict):
    """Print a summary of workflow results"""
    print(f"\n📋 WORKFLOW SUMMARY")
    print("-" * 40)
    print(f"Incident ID: {result.get('incident_id', 'Unknown')}")
    print(f"Final Status: {result.get('stage', 'Unknown').upper()}")
    
    # Show decision metrics if available
    if "decision_metrics" in result:
        metrics = result["decision_metrics"]
        print(f"Confidence: {metrics.get('confidence', 0):.2f}")
        print(f"Decision: {result.get('decision', 'Unknown').upper()}")
        
        if metrics.get("escalation_reason"):
            print(f"Escalation Reason: {metrics['escalation_reason']}")
    
    # Show agent completion
    if "agents_completed" in result:
        agents = result["agents_completed"]
        print(f"Agents Completed: {len(set(agents))}")
    
    print(f"Workflow Complete: {result.get('workflow_complete', False)}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Application interrupted!")
    except Exception as e:
        print(f"❌ Application error: {e}")
        sys.exit(1)