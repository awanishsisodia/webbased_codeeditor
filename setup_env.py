#!/usr/bin/env python3
"""
Setup script to create .env file with Ollama configuration
"""

import os

def create_env_file():
    """Create .env file with Ollama configuration"""
    
    env_content = """# Python Code Editor Environment Configuration
# Ollama API Configuration
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=llama3:latest

# Workspace Configuration
WORKSPACE_DIR=./workspace

# Flask Configuration (optional)
FLASK_ENV=development
FLASK_DEBUG=1
"""
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists. Skipping creation.")
        return
    
    # Create .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("📝 Configuration:")
        print("   - Ollama API: http://localhost:11434")
        print("   - Model: llama3:latest")
        print("   - Workspace: ./workspace")
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")

def main():
    """Main setup function"""
    print("🚀 Python Code Editor - Environment Setup")
    print("=" * 40)
    
    create_env_file()
    
    print("\n🎯 Next steps:")
    print("1. Ensure Ollama is running: ollama serve")
    print("2. Run the application: python3 app.py")
    print("3. Open http://localhost:5002 in your browser")
    
    print("\n💡 To test Ollama connection:")
    print("   python3 test_ollama.py")

if __name__ == "__main__":
    main()
