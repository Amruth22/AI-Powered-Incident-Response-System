#!/usr/bin/env python3
"""
System test to verify the TRUE parallel incident response system works
with environment configuration support
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
    """Test configuration values and environment loading"""
    print("\n🔧 Testing configuration...")
    
    try:
        from core.config import CONFIDENCE_THRESHOLD, MAX_RETRIES, validate_config
        from dotenv import load_dotenv
        
        # Test basic configuration values
        assert 0 < CONFIDENCE_THRESHOLD <= 1, "Invalid confidence threshold"
        assert MAX_RETRIES > 0, "Invalid max retries"
        
        # Test environment loading
        load_dotenv()
        print("✅ Environment variables loaded")
        
        # Test configuration validation (may fail if .env not set up)
        try:
            validate_config()
            print("✅ Configuration validation passed")
        except ValueError as e:
            print(f"⚠️ Configuration validation failed: {e}")
            print("💡 This is expected if .env file is not configured with real credentials")
        
        print("✅ Configuration structure is valid")
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_environment_file():
    """Test that environment files exist"""
    print("\n📄 Testing environment files...")
    
    try:
        import os
        
        # Check for .env.example
        if os.path.exists(".env.example"):
            print("✅ .env.example file exists")
        else:
            print("❌ .env.example file missing")
            return False
        
        # Check for .env (optional)
        if os.path.exists(".env"):
            print("✅ .env file exists")
        else:
            print("⚠️ .env file not found (copy from .env.example)")
        
        return True
        
    except Exception as e:
        print(f"❌ Environment file test error: {e}")
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
        
        print("✅ TRUE Parallel workflow created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Workflow creation error: {e}")
        return False

def run_all_tests():
    """Run all system tests"""
    print("🚀 TRUE PARALLEL INCIDENT RESPONSE SYSTEM - SYSTEM TESTS")
    print("=" * 60)
    
    tests = [
        ("Environment Files", test_environment_file),
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("State Management", test_state_management),
        ("Agent Creation", test_agent_creation),
        ("Knowledge Base", test_knowledge_base),
        ("Workflow Creation", test_workflow_creation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! System is ready to use.")
        print("\n🚀 Setup Instructions:")
        print("1. Copy .env.example to .env")
        print("2. Update .env with your actual credentials")
        print("3. Run: python main.py --demo")
        return True
    else:
        print("💥 SOME TESTS FAILED! Please check the errors above.")
        print("\n💡 Common Issues:")
        print("- Missing .env file (copy from .env.example)")
        print("- Invalid credentials in .env file")
        print("- Missing dependencies (run: pip install -r requirements.txt)")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)