"""
Simple runner script for ESI Conversation Flow Agent
"""

import os
import sys
from esi_conversation_flow import ESIAgentManager
from config import Config

def main():
    print("🏗️  ESI Conversation Flow Agent")
    print("================================")
    
    # Check configuration
    if not Config.RETELL_API_KEY or Config.RETELL_API_KEY == "your_retell_api_key_here":
        print("❌ Please set RETELL_API_KEY in your .env file")
        print("Copy .env.example to .env and add your API key")
        print("\nGet your API key from: https://dashboard.retellai.com/api-keys")
        sys.exit(1)
    
    print(f"Agent Name: {Config.AGENT_NAME}")
    print(f"Language: {Config.LANGUAGE}")
    print(f"Voice ID: {Config.CUSTOM_VOICE_ID}")
    print(f"n8n Webhook: {Config.N8N_WEBHOOK_URL}")
    print()
    
    # Create agent manager
    print("🚀 Deploying your agent...")
    agent_manager = ESIAgentManager(Config.RETELL_API_KEY)
    
    try:
        # Create the agent
        agent = agent_manager.create_agent(Config.AGENT_NAME)
        
        # Save conversation flow for reference
        flow_file = agent_manager.save_conversation_flow()
        
        print(f"\n🎉 SUCCESS!")
        print(f"Agent ID: {agent.agent_id}")
        print(f"Agent Name: {agent.agent_name}")
        print(f"📁 Flow saved to: {flow_file}")
        
        print("\n🔗 Useful links:")
        print("- Retell Dashboard: https://dashboard.retellai.com")
        print("- Agent Management: https://dashboard.retellai.com/agents")
        print("- Call History: https://dashboard.retellai.com/calls")
        
        print("\n📋 Next steps:")
        print("1. Go to Retell dashboard to test your agent")
        print("2. Configure your phone number to use this agent")
        print("3. Start taking calls!")
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check your RETELL_API_KEY is correct")
        print("2. Ensure you have internet connection")
        print("3. Verify your account has API access")
        sys.exit(1)

if __name__ == "__main__":
    main()
