"""
Setup script for ESI Conversation Flow Agent
Run this first to get everything configured quickly
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"You have Python {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version} is compatible")

def install_dependencies():
    """Install required packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def create_env_file():
    """Create .env file from template"""
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if env_path.exists():
        print("✅ .env file already exists")
        return
    
    if env_example_path.exists():
        # Copy to .env
        with open(env_example_path, "r") as f:
            content = f.read()
        
        with open(env_path, "w") as f:
            f.write(content)
        
        print("📝 Created .env file")
        print("🔧 Please edit .env and add your actual RETELL_API_KEY")

def verify_setup():
    """Verify that everything is set up correctly"""
    print("\n🧪 Verifying setup...")
    
    try:
        from config import Config
        from esi_conversation_flow import ESIAgentManager
        print("✅ All modules import successfully")
        
        if Config.RETELL_API_KEY and Config.RETELL_API_KEY != "your_retell_api_key_here":
            print("✅ Configuration looks good")
        else:
            print("⚠️  Please update your RETELL_API_KEY in .env file")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup verification failed: {e}")
        return False

def main():
    print("🚀 ESI Conversation Flow Agent Setup")
    print("====================================\n")
    
    check_python_version()
    install_dependencies()
    create_env_file()
    
    if verify_setup():
        print("\n🎉 Setup complete!")
        print("\nNext steps:")
        print("1. Edit .env and add your RETELL_API_KEY")
        print("2. Run: python test_agent.py")
        print("3. Run: python run.py")
    else:
        print("\n❌ Setup incomplete. Please check the errors above.")

if __name__ == "__main__":
    main()
