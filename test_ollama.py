#!/usr/bin/env python3
"""
Test script to verify Ollama connection and API functionality
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_ollama_connection():
    """Test basic Ollama connection"""
    print("🧪 Testing Ollama Connection...")
    
    ollama_url = os.getenv('OLLAMA_API_URL', 'http://localhost:11434')
    model = os.getenv('OLLAMA_MODEL', 'llama3')
    
    print(f"📡 Ollama URL: {ollama_url}")
    print(f"🤖 Model: {model}")
    
    try:
        # Test basic connection
        response = requests.get(f"{ollama_url}/api/tags", timeout=10)
        if response.status_code == 200:
            print("✓ Ollama service is accessible")
            
            # Check available models
            models = response.json()
            if 'models' in models:
                available_models = [m['name'] for m in models['models']]
                print(f"📋 Available models: {', '.join(available_models)}")
                
                if model in available_models:
                    print(f"✅ Model '{model}' is available")
                else:
                    print(f"⚠️  Model '{model}' not found. Available: {', '.join(available_models)}")
                    print(f"💡 You can pull it with: ollama pull {model}")
            else:
                print("⚠️  Could not retrieve model list")
        else:
            print(f"❌ Ollama service returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Ollama service")
        print("💡 Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False
    
    return True

def test_ollama_generation():
    """Test Ollama text generation"""
    print("\n🧪 Testing Ollama Generation...")
    
    ollama_url = os.getenv('OLLAMA_API_URL', 'http://localhost:11434')
    model = os.getenv('OLLAMA_MODEL', 'llama3')
    
    try:
        # Test simple generation
        data = {
            "model": model,
            "prompt": "Say 'Hello from Ollama!' in one sentence.",
            "stream": False,
            "options": {
                "num_predict": 50
            }
        }
        
        response = requests.post(f"{ollama_url}/api/generate", 
                               json=data, 
                               headers={'Content-Type': 'application/json'},
                               timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'response' in result:
                print("✅ Text generation successful")
                print(f"📝 Response: {result['response'].strip()}")
                return True
            else:
                print("❌ Unexpected response format")
                print(f"Response: {result}")
                return False
        else:
            print(f"❌ Generation failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Generation test failed: {e}")
        return False

def test_python_code_suggestion():
    """Test Python code suggestion functionality"""
    print("\n🧪 Testing Python Code Suggestion...")
    
    ollama_url = os.getenv('OLLAMA_API_URL', 'http://localhost:11434')
    model = os.getenv('OLLAMA_MODEL', 'llama3')
    
    try:
        # Test Python code suggestion
        prompt = """You are a Python programming assistant. Provide a brief suggestion for improving this code:

def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

Provide one specific improvement suggestion:"""
        
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 100
            }
        }
        
        response = requests.post(f"{ollama_url}/api/generate", 
                               json=data, 
                               headers={'Content-Type': 'application/json'},
                               timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'response' in result:
                print("✅ Python code suggestion successful")
                print(f"💡 Suggestion: {result['response'].strip()}")
                return True
            else:
                print("❌ Unexpected response format")
                return False
        else:
            print(f"❌ Code suggestion failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Code suggestion test failed: {e}")
        return False

def main():
    """Run all Ollama tests"""
    print("🚀 Ollama Connection Test")
    print("=" * 40)
    
    tests = [
        test_ollama_connection,
        test_ollama_generation,
        test_python_code_suggestion
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Ollama tests passed! Your setup is ready.")
        print("\nYou can now run the Python Code Editor:")
        print("  python app.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
