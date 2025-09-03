#!/usr/bin/env python3
"""
Test script to verify the Python Code Editor setup
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import flask
        print("✓ Flask imported successfully")
    except ImportError as e:
        print(f"✗ Flask import failed: {e}")
        return False
    
    try:
        import requests
        print("✓ Requests imported successfully")
    except ImportError as e:
        print(f"✗ Requests import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✓ Python-dotenv imported successfully")
    except ImportError as e:
        print(f"✗ Python-dotenv import failed: {e}")
        return False
    
    return True

def test_utils():
    """Test if utility modules can be imported"""
    print("\nTesting utility modules...")
    
    try:
        from utils.llama_client import LlamaClient
        print("✓ LlamaClient imported successfully")
    except ImportError as e:
        print(f"✗ LlamaClient import failed: {e}")
        return False
    
    try:
        from utils.code_executor import CodeExecutor
        print("✓ CodeExecutor imported successfully")
    except ImportError as e:
        print(f"✗ CodeExecutor import failed: {e}")
        return False
    
    try:
        from utils.file_manager import FileManager
        print("✓ FileManager imported successfully")
    except ImportError as e:
        print(f"✗ FileManager import failed: {e}")
        return False
    
    return True

def test_directories():
    """Test if required directories exist"""
    print("\nTesting directory structure...")
    
    required_dirs = ['utils', 'templates', 'static', 'static/css', 'static/js', 'workspace']
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✓ Directory exists: {dir_path}")
        else:
            print(f"✗ Directory missing: {dir_path}")
            return False
    
    return True

def test_files():
    """Test if required files exist"""
    print("\nTesting required files...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        'TODO.md',
        'templates/index.html',
        'static/css/style.css',
        'static/js/app.js',
        'utils/__init__.py',
        'utils/llama_client.py',
        'utils/code_executor.py',
        'utils/file_manager.py'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ File exists: {file_path}")
        else:
            print(f"✗ File missing: {file_path}")
            return False
    
    return True

def test_python_version():
    """Test Python version compatibility"""
    print("\nTesting Python version...")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} is not compatible (requires 3.8+)")
        return False

def main():
    """Run all tests"""
    print("🚀 Python Code Editor - Setup Test")
    print("=" * 50)
    
    tests = [
        test_python_version,
        test_imports,
        test_utils,
        test_directories,
        test_files
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Ensure Ollama is running: ollama serve")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Run the application: python app.py")
        print("4. Open http://localhost:5002 in your browser")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
