"""
Testing utilities for ESI Conversation Flow Agent
"""

import json
import sys
from esi_conversation_flow import ESIConversationFlowBuilder

def test_conversation_flow_structure():
    """Test that the conversation flow structure is valid"""
    
    print("🧪 Testing conversation flow structure...")
    
    builder = ESIConversationFlowBuilder()
    flow = builder.build_conversation_flow()
    
    # Basic structure tests
    assert "nodes" in flow, "Flow missing 'nodes'"
    assert "tools" in flow, "Flow missing 'tools'"
    assert "global_prompt" in flow, "Flow missing 'global_prompt'"
    assert "start_node_id" in flow, "Flow missing 'start_node_id'"
    
    # Nodes tests
    nodes = flow["nodes"]
    assert len(nodes) > 0, "No nodes found"
    
    # Find start node
    start_node = next((n for n in nodes if n["id"] == flow["start_node_id"]), None)
    assert start_node is not None, "Start node not found"
    
    # Tools tests
    tools = flow["tools"]
    assert len(tools) > 0, "No tools found"
    
    # Check required tools exist
    tool_names = [tool["name"] for tool in tools]
    expected_tools = [
        "check_availability_privada",
        "check_availability_online", 
        "book_calendar_privada",
        "book_calendar_online",
        "create_hubspot_task"
    ]
    
    for expected_tool in expected_tools:
        assert expected_tool in tool_names, f"Missing tool: {expected_tool}"
    
    print(f"   ✅ Found {len(nodes)} nodes")
    print(f"   ✅ Found {len(tools)} tools")
    print(f"   ✅ Start node: {flow['start_node_id']}")
    print("✅ Conversation flow structure tests passed!")

def test_tool_parameters():
    """Test that tool parameters are properly structured"""
    
    print("\n🧪 Testing tool parameters...")
    
    builder = ESIConversationFlowBuilder()
    builder.create_tools()
    
    for tool in builder.tools:
        assert tool.url is not None, f"Tool {tool.name} missing URL"
        assert tool.method in ["GET", "POST", "PUT", "DELETE"], f"Tool {tool.name} has invalid method"
        assert hasattr(tool, 'parameters'), f"Tool {tool.name} missing parameters"
        
        # Test n8n webhook URL
        assert "n8n.zonder.ai" in tool.url, f"Tool {tool.name} not using n8n webhook"
    
    print(f"   ✅ Tested {len(builder.tools)} tools")
    print("✅ Tool parameter tests passed!")

def test_global_prompt():
    """Test that the global prompt contains ESI-specific content"""
    
    print("\n🧪 Testing global prompt...")
    
    builder = ESIConversationFlowBuilder()
    prompt = builder.global_prompt
    
    # Check for key ESI elements
    assert "Bea" in prompt, "Global prompt missing Bea identity"
    assert "ESI" in prompt, "Global prompt missing ESI reference"
    assert "español" in prompt.lower(), "Global prompt missing Spanish language reference"
    assert "diseño" in prompt.lower(), "Global prompt missing design reference"
    
    # Check for course types
    courses = ["Diseño Gráfico", "UX/UI", "Interiores", "Ilustración", "Motion Graphics"]
    for course in courses:
        assert course in prompt, f"Global prompt missing course: {course}"
    
    # Check for specialist emails
    specialists = ["caridadfrutos@", "vanessacalvo@", "martagutierrez@"]
    for specialist in specialists:
        assert specialist in prompt, f"Global prompt missing specialist: {specialist}"
    
    print(f"   ✅ Prompt length: {len(prompt)} characters")
    print("✅ Global prompt tests passed!")

def validate_json_output():
    """Validate that the output can be serialized to JSON"""
    
    print("\n🧪 Testing JSON serialization...")
    
    builder = ESIConversationFlowBuilder()
    flow = builder.build_conversation_flow()
    
    try:
        # Test JSON serialization
        json_output = json.dumps(flow, ensure_ascii=False, indent=2)
        
        # Test JSON parsing
        parsed_back = json.loads(json_output)
        
        # Basic validation that parsing worked
        assert parsed_back["conversation_flow_id"] == flow["conversation_flow_id"]
        assert len(parsed_back["nodes"]) == len(flow["nodes"])
        assert len(parsed_back["tools"]) == len(flow["tools"])
        
        print(f"   ✅ JSON size: {len(json_output)} bytes")
        print("✅ JSON serialization test passed!")
        
    except Exception as e:
        print(f"❌ JSON serialization failed: {e}")
        raise

def test_configuration():
    """Test that configuration is properly loaded"""
    
    print("\n🧪 Testing configuration...")
    
    try:
        from config import Config
        
        # Test that config class exists and has required attributes
        required_attrs = [
            'RETELL_API_KEY', 'AGENT_NAME', 'N8N_WEBHOOK_URL',
            'CUSTOM_VOICE_ID', 'LANGUAGE', 'ONLINE_SPECIALISTS'
        ]
        
        for attr in required_attrs:
            assert hasattr(Config, attr), f"Config missing attribute: {attr}"
        
        # Test language is Spanish
        assert Config.LANGUAGE == "es-ES", "Language should be es-ES"
        
        # Test specialists are configured
        assert len(Config.ONLINE_SPECIALISTS) > 0, "No online specialists configured"
        assert len(Config.PRIVATE_SPECIALISTS) > 0, "No private specialists configured"
        
        print(f"   ✅ Language: {Config.LANGUAGE}")
        print(f"   ✅ Online specialists: {len(Config.ONLINE_SPECIALISTS)}")
        print(f"   ✅ Private specialists: {len(Config.PRIVATE_SPECIALISTS)}")
        print("✅ Configuration tests passed!")
        
    except ImportError as e:
        print(f"❌ Configuration import failed: {e}")
        print("Make sure you have run setup.py first")
        raise

def run_all_tests():
    """Run all tests and report results"""
    
    print("🧪 ESI Conversation Flow Agent - Test Suite")
    print("=" * 50)
    
    tests = [
        test_configuration,
        test_conversation_flow_structure,
        test_tool_parameters,
        test_global_prompt,
        validate_json_output
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ Test failed: {test.__name__}")
            print(f"   Error: {e}")
            
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your conversation flow is ready to deploy.")
        print("\nNext steps:")
        print("1. Make sure your RETELL_API_KEY is set in .env")
        print("2. Run: python run.py")
        return True
    else:
        print(f"\n❌ {total - passed} tests failed. Please fix the issues above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
