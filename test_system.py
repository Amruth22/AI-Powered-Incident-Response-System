#!/usr/bin/env python3
"""
System test to verify the professional incident response system works
"""

def test_imports():
    """Test that all modules can be imported correctly"""
    print("🧪 Testing imports...")
    
    try:
        # Core imports
        from core.config import CONFIDENCE_THRESHOLD, MAX_RETRIES
        from core.state import create_incident_state, update_stage
        print("✅ Core modules imported successfully")
        
        # Agent imports
        from agents import (
            IncidentTriggerAgent, LogAnalysisAgent, KnowledgeLookupAgent,
            RootCauseAgent, MitigationAgent, EscalationAgent, 
            CommunicatorAgent, AgentCoordinator
        )
        print("✅ Agent modules imported successfully")
        
        # Service imports
        from services.gemini.client import parse_incident_alert
        from services.email.client import send_incident_alert
        from services.knowledge.client import load_past_resolutions
        print("✅ Service modules imported successfully")
        
        # Workflow imports
        from workflows import process_incident
        print("✅ Workflow modules imported successfully")
        
        # Utils imports
        from utils.logging_utils import setup_logging
        print("✅ Utils modules imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_configuration():
    """Test configuration values"""
    print("\n🔧 Testing configuration...")
    
    try:
        from core.config import CONFIDENCE_THRESHOLD, MAX_RETRIES, GEMINI_API_KEY
        
        assert 0 < CONFIDENCE_THRESHOLD <= 1, "Invalid confidence threshold"
        assert MAX_RETRIES > 0, "Invalid max retries"
        assert GEMINI_API_KEY, "Gemini API key not configured"
        
        print("✅ Configuration values are valid")
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_state_management():
    """Test state creation and management"""
    print("\n📊 Testing state management...")
    
    try:
        from core.state import create_incident_state, update_stage
        
        # Create test state
        state = create_incident_state("Test incident alert")
        
        assert "incident_id" in state, "Missing incident ID"
        assert state["incident_id"].startswith("INC-"), "Invalid incident ID format"
        assert state["stage"] == "detected", "Invalid initial stage"
        
        # Test stage update
        updated_state = update_stage(state, "analyzing")
        assert updated_state["stage"] == "analyzing", "Stage update failed"
        
        print("✅ State management working correctly")
        return True
        
    except Exception as e:
        print(f"❌ State management error: {e}")
        return False

def test_agent_creation():
    """Test agent instantiation"""
    print("\n🤖 Testing agent creation...")
    
    try:
        from agents import (
            IncidentTriggerAgent, LogAnalysisAgent, KnowledgeLookupAgent,
            RootCauseAgent, AgentCoordinator
        )
        
        # Create agents
        trigger = IncidentTriggerAgent()
        log_analysis = LogAnalysisAgent()
        knowledge = KnowledgeLookupAgent()
        root_cause = RootCauseAgent()
        coordinator = AgentCoordinator()
        
        # Verify agent properties
        assert trigger.agent_name == "incident_trigger", "Invalid agent name"
        assert hasattr(trigger, 'execute'), "Missing execute method"
        assert hasattr(trigger, 'process'), "Missing process method"
        
        print("✅ Agents created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Agent creation error: {e}")
        return False

def test_knowledge_base():
    """Test knowledge base loading"""
    print("\n📚 Testing knowledge base...")
    
    try:
        from services.knowledge.client import load_past_resolutions
        
        incidents = load_past_resolutions()
        
        assert isinstance(incidents, list), "Incidents should be a list"
        assert len(incidents) > 0, "No incidents loaded"
        
        # Check first incident structure
        if incidents:
            incident = incidents[0]
            required_fields = ['service', 'root_cause', 'solution', 'keywords']
            for field in required_fields:
                assert field in incident, f"Missing field: {field}"
        
        print(f"✅ Knowledge base loaded: {len(incidents)} incidents")
        return True
        
    except Exception as e:
        print(f"❌ Knowledge base error: {e}")
        return False

def test_workflow_creation():
    """Test workflow instantiation"""
    print("\n🔄 Testing workflow creation...")
    
    try:
        from workflows.parallel_workflow import ParallelIncidentWorkflow
        
        # Create workflow
        workflow = ParallelIncidentWorkflow()
        
        # Create workflow graph
        graph = workflow.create_workflow()
        
        assert graph is not None, "Workflow graph not created"
        assert workflow.workflow is not None, "Workflow not compiled"
        
        print("✅ Workflow created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Workflow creation error: {e}")
        return False

def run_all_tests():
    """Run all system tests"""
    print("🚀 PROFESSIONAL INCIDENT RESPONSE SYSTEM - SYSTEM TESTS")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_configuration,
        test_state_management,
        test_agent_creation,
        test_knowledge_base,
        test_workflow_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! System is ready to use.")
        print("\nYou can now run:")
        print("  python main.py --demo")
        print("  python main.py \"Payment API database timeout\"")
        return True
    else:
        print("💥 SOME TESTS FAILED! Please check the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)