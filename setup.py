#!/usr/bin/env python3
"""
Setup script for AI-Powered Incident Response System
Helps with installation and configuration
"""

import os
import sys
import shutil
from pathlib import Path

def create_env_file():
    """Create .env file from .env.example if it doesn't exist"""
    
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return True
    
    if not os.path.exists('.env.example'):
        print("❌ .env.example file not found")
        return False
    
    try:
        shutil.copy('.env.example', '.env')
        print("✅ Created .env file from .env.example")
        print("💡 Please edit .env file with your actual credentials")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def create_logs_directory():
    """Create logs directory if it doesn't exist"""
    
    logs_dir = Path('logs')
    if logs_dir.exists():
        print("✅ logs/ directory already exists")
        return True
    
    try:
        logs_dir.mkdir(exist_ok=True)
        print("✅ Created logs/ directory")
        return True
    except Exception as e:
        print(f"❌ Error creating logs directory: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    
    required_packages = [
        'google-generativeai',
        'langgraph',
        'langchain-core',
        'python-dotenv',
        'typing_extensions'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages are installed")
        return True

def validate_configuration():
    """Validate the configuration"""
    
    try:
        from core.config import validate_config
        validate_config()
        print("✅ Configuration is valid")
        return True
    except ValueError as e:
        print(f"⚠️ Configuration validation failed: {e}")
        print("💡 Please update your .env file with valid credentials")
        return False
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def run_system_test():
    """Run system tests"""
    
    try:
        print("\n🧪 Running system tests...")
        import subprocess
        result = subprocess.run([sys.executable, 'test_system.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ System tests passed")
            return True
        else:
            print("❌ System tests failed")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def print_setup_instructions():
    """Print setup instructions"""
    
    print("\n" + "="*60)
    print("🚀 AI-POWERED INCIDENT RESPONSE SYSTEM SETUP")
    print("="*60)
    print("\n📋 Setup Checklist:")
    print("1. ✅ Install dependencies: pip install -r requirements.txt")
    print("2. ✅ Create .env file from .env.example")
    print("3. ✅ Create logs directory")
    print("4. ⚠️ Edit .env file with your credentials:")
    print("   - EMAIL_FROM, EMAIL_PASSWORD, EMAIL_TO")
    print("   - GEMINI_API_KEY")
    print("5. ✅ Validate configuration")
    print("6. ✅ Run system tests")
    print("\n🔗 Get API Keys:")
    print("- Gemini API: https://makersuite.google.com/app/apikey")
    print("- Gmail App Password: https://myaccount.google.com/apppasswords")
    print("\n🚀 After setup, run:")
    print("  python main.py --demo")

def main():
    """Main setup function"""
    
    print("🚀 Setting up AI-Powered Incident Response System...")
    print("-" * 50)
    
    steps = [
        ("Creating .env file", create_env_file),
        ("Creating logs directory", create_logs_directory),
        ("Checking dependencies", check_dependencies),
        ("Validating configuration", validate_configuration),
        ("Running system tests", run_system_test)
    ]
    
    completed = 0
    total = len(steps)
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        try:
            if step_func():
                completed += 1
            else:
                print(f"⚠️ {step_name} needs attention")
        except Exception as e:
            print(f"❌ {step_name} failed: {e}")
    
    print("\n" + "="*50)
    print(f"📊 Setup Progress: {completed}/{total} steps completed")
    
    if completed == total:
        print("🎉 Setup completed successfully!")
        print("\n🚀 You can now run:")
        print("  python main.py --demo")
    else:
        print("⚠️ Setup needs attention. Please check the steps above.")
        print_setup_instructions()

if __name__ == "__main__":
    main()