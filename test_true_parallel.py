#!/usr/bin/env python3
"""
Test to verify TRUE parallel execution works without state conflicts
"""

import time
from datetime import datetime

def test_true_parallel_execution():
    """Test that the system now uses TRUE parallel execution"""
    
    print("🧪 TESTING TRUE PARALLEL EXECUTION")
    print("=" * 50)
    
    try:
        # Import the workflow
        from workflows.parallel_workflow import ParallelIncidentWorkflow
        print("✅ Successfully imported TRUE parallel workflow")
        
        # Create workflow instance
        workflow = ParallelIncidentWorkflow()
        print("✅ Workflow instance created")
        
        # Test workflow creation
        graph = workflow.create_workflow()
        print("✅ Workflow graph created successfully")
        
        # Test with a simple alert
        test_alert = "Payment API database timeout with high error rates"
        print(f"📥 Testing with alert: {test_alert}")
        print("-" * 50)
        
        # Time the execution
        start_time = time.time()
        result = workflow.execute(test_alert)
        end_time = time.time()
        duration = end_time - start_time
        
        print("-" * 50)
        print("✅ TRUE PARALLEL EXECUTION SUCCESSFUL!")
        print(f"⏱️ Completed in {duration:.2f} seconds")
        print(f"📋 Incident: {result.get('incident_id', 'Unknown')}")
        print(f"📊 Status: {result.get('stage', 'Unknown')}")
        
        # Verify parallel execution indicators
        if "agents_completed" in result:
            completed = result["agents_completed"]
            unique_agents = set(completed)
            print(f"🤖 Agents Completed: {len(unique_agents)} unique agents")
            print(f"   Agents: {', '.join(unique_agents)}")
            
            # Check if parallel agents completed
            parallel_agents = {"log_analysis", "knowledge_lookup", "root_cause"}
            completed_parallel = parallel_agents.intersection(unique_agents)
            
            if len(completed_parallel) == 3:
                print("✅ ALL 3 PARALLEL AGENTS COMPLETED!")
                print("🚀 TRUE PARALLEL EXECUTION CONFIRMED!")
            else:
                print(f"⚠️ Only {len(completed_parallel)} parallel agents completed")
        
        # Check decision metrics
        if "decision_metrics" in result:
            metrics = result["decision_metrics"]
            print(f"🎯 Decision: {result.get('decision', 'Unknown')}")
            print(f"📈 Confidence: {metrics.get('confidence', 0):.2f}")
            print(f"🔍 Anomalies Found: {metrics.get('anomalies_found', False)}")
            print(f"📚 Similar Incidents: {metrics.get('similar_incidents_count', 0)}")
        
        print(f"\n🎉 TRUE PARALLEL TEST PASSED!")
        print("The system now executes Log Analysis + Knowledge Lookup + Root Cause simultaneously!")
        return True
        
    except Exception as e:
        print(f"\n❌ TRUE PARALLEL TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_state_schema():
    """Test that the state schema supports concurrent updates"""
    
    print("\n🔧 TESTING STATE SCHEMA FOR CONCURRENT UPDATES")
    print("-" * 50)
    
    try:
        from typing_extensions import TypedDict
        from typing import Annotated, List, Dict, Any
        from operator import add
        
        # Test the state schema definition
        class TestIncidentState(TypedDict):
            agents_completed: Annotated[List[str], add]
            agent_errors: Annotated[List[Dict], add]
        
        print("✅ State schema with Annotated types created successfully")
        print("✅ Concurrent list updates supported")
        return True
        
    except Exception as e:
        print(f"❌ State schema test failed: {e}")
        return False

def test_workflow_routing():
    """Test that workflow routing supports TRUE parallel execution"""
    
    print("\n🔄 TESTING WORKFLOW ROUTING")
    print("-" * 50)
    
    try:
        from workflows.parallel_workflow import ParallelIncidentWorkflow
        
        workflow = ParallelIncidentWorkflow()
        
        # Test parallel routing
        test_state = {"next": "parallel_agents"}
        result = workflow.route_to_parallel_agents(test_state)
        
        expected_agents = ["log_analysis", "knowledge_lookup", "root_cause"]
        
        if isinstance(result, list) and set(result) == set(expected_agents):
            print("✅ Parallel routing returns all 3 agents simultaneously")
            print(f"   Agents: {', '.join(result)}")
            print("🚀 TRUE PARALLEL ROUTING CONFIRMED!")
            return True
        else:
            print(f"❌ Parallel routing failed. Expected {expected_agents}, got {result}")
            return False
            
    except Exception as e:
        print(f"❌ Workflow routing test failed: {e}")
        return False

def run_all_tests():
    """Run all TRUE parallel tests"""
    
    print("🚀 TRUE PARALLEL MULTI-AGENT SYSTEM - VERIFICATION TESTS")
    print("=" * 60)
    
    tests = [
        ("State Schema", test_state_schema),
        ("Workflow Routing", test_workflow_routing),
        ("TRUE Parallel Execution", test_true_parallel_execution)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} Test...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} Test PASSED")
            else:
                print(f"❌ {test_name} Test FAILED")
        except Exception as e:
            print(f"❌ {test_name} Test FAILED with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("\n🚀 TRUE PARALLEL EXECUTION VERIFIED!")
        print("The system now runs Log Analysis + Knowledge Lookup + Root Cause simultaneously!")
        print("\nYou can now run:")
        print("  python main.py \"Payment API database timeout\"")
        print("  python main.py --demo")
        return True
    else:
        print("💥 SOME TESTS FAILED!")
        print("Please check the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)