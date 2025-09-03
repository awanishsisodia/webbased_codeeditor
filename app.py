#!/usr/bin/env python3
"""
Python Code Editor with LLaMA3 Integration
Main Flask application providing web-based code editing capabilities
"""

import os
import json
import subprocess
import tempfile
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from utils.llama_client import LlamaClient
from utils.code_executor import CodeExecutor
from utils.file_manager import FileManager

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
WORKSPACE_DIR = os.getenv('WORKSPACE_DIR', './workspace')
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3:latest')

# Initialize components
llama_client = LlamaClient(OLLAMA_API_URL, OLLAMA_MODEL)
code_executor = CodeExecutor()
file_manager = FileManager(WORKSPACE_DIR)

# Ensure workspace directory exists
os.makedirs(WORKSPACE_DIR, exist_ok=True)

@app.route('/')
def index():
    """Main editor interface"""
    return render_template('index.html')

@app.route('/api/files', methods=['GET'])
def list_files():
    """List all files in the workspace"""
    try:
        files = file_manager.list_files()
        return jsonify({'success': True, 'files': files})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/files', methods=['POST'])
def create_file():
    """Create or save a file"""
    try:
        data = request.get_json()
        file_path = data.get('path')
        content = data.get('content', '')
        
        if not file_path:
            return jsonify({'success': False, 'error': 'File path is required'}), 400
        
        file_manager.save_file(file_path, content)
        return jsonify({'success': True, 'message': 'File saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/files/<path:file_path>', methods=['GET'])
def get_file(file_path):
    """Get file content"""
    try:
        content = file_manager.read_file(file_path)
        return jsonify({'success': True, 'content': content})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/files/<path:file_path>', methods=['DELETE'])
def delete_file(file_path):
    """Delete a file"""
    try:
        file_manager.delete_file(file_path)
        return jsonify({'success': True, 'message': 'File deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/execute', methods=['POST'])
def execute_code():
    """Execute Python code"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        
        if not code:
            return jsonify({'success': False, 'error': 'Code is required'}), 400
        
        # Execute the code
        result = code_executor.execute(code)
        
        # If there's an error, get LLaMA3 suggestions
        if result.get('error'):
            suggestions = llama_client.get_error_fixes(code, result['error'])
            result['suggestions'] = suggestions
        
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/suggest', methods=['POST'])
def get_suggestions():
    """Get code suggestions from LLaMA3"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        context = data.get('context', '')
        
        if not code:
            return jsonify({'success': False, 'error': 'Code is required'}), 400
        
        suggestions = llama_client.get_suggestions(code, context)
        return jsonify({'success': True, 'suggestions': suggestions})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    """Analyze code for potential issues"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        
        if not code:
            return jsonify({'success': False, 'error': 'Code is required'}), 400
        
        # Get LLaMA3 analysis
        analysis = llama_client.analyze_code(code)
        return jsonify({'success': True, 'analysis': analysis})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print(f"🚀 Starting Python Code Editor...")
    print(f"📁 Workspace: {WORKSPACE_DIR}")
    print(f"🤖 Ollama API: {OLLAMA_API_URL}")
    print(f"🤖 Model: {OLLAMA_MODEL}")
    print(f"🌐 Server will be available at: http://localhost:5002")
    
    app.run(debug=True, host='0.0.0.0', port=5002)
