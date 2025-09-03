"""
LLaMA3 API client for code suggestions and analysis
"""

import requests
import json
from typing import List, Dict, Optional

class LlamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, api_url: str, model: str = "llama3"):
        self.api_url = api_url.rstrip('/')
        self.model = model
        self.headers = {
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, endpoint: str, data: Dict) -> Dict:
        """Make a request to the Ollama API"""
        try:
            url = f"{self.api_url}{endpoint}"
            response = requests.post(url, headers=self.headers, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ollama API request failed: {e}")
            return {"error": str(e)}
        except json.JSONDecodeError as e:
            print(f"Failed to parse Ollama response: {e}")
            return {"error": "Invalid response format"}
    
    def get_suggestions(self, code: str, context: str = "") -> List[str]:
        """Get code suggestions from LLaMA3"""
        prompt = f"""
        You are a Python programming assistant. Based on the following code and context, provide helpful suggestions for code completion or improvement.
        
        Context: {context}
        Code:
        {code}
        
        Provide 3-5 specific, actionable suggestions for improving or completing this code. Focus on Python best practices, readability, and functionality.
        """
        
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "top_p": 0.9,
                "num_predict": 500
            }
        }
        
        response = self._make_request("/api/generate", data)
        
        if "error" in response:
            return [f"Error getting suggestions: {response['error']}"]
        
        # Parse suggestions from response
        suggestions = []
        if "response" in response:
            text = response["response"]
            # Split into individual suggestions
            suggestions = [s.strip() for s in text.split('\n') if s.strip()]
        
        return suggestions[:5] if suggestions else ["No suggestions available"]
    
    def get_error_fixes(self, code: str, error: str) -> List[str]:
        """Get fix suggestions for Python errors"""
        prompt = f"""
        You are a Python debugging expert. The following code has an error. Please provide specific fixes.
        
        Code:
        {code}
        
        Error:
        {error}
        
        Provide 3-5 specific, actionable fixes for this error. Include corrected code snippets and explanations.
        """
        
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "top_p": 0.9,
                "num_predict": 600
            }
        }
        
        response = self._make_request("/api/generate", data)
        
        if "error" in response:
            return [f"Error getting fixes: {response['error']}"]
        
        # Parse fixes from response
        fixes = []
        if "response" in response:
            text = response["response"]
            # Split into individual fixes
            fixes = [f.strip() for f in text.split('\n') if f.strip()]
        
        return fixes[:5] if fixes else ["No fixes available"]
    
    def analyze_code(self, code: str) -> Dict:
        """Analyze code for potential issues and improvements"""
        prompt = f"""
        You are a Python code reviewer. Analyze the following code for:
        1. Potential bugs or errors
        2. Code quality issues
        3. Performance improvements
        4. Best practices violations
        5. Security concerns
        
        Code:
        {code}
        
        Provide a comprehensive analysis with specific recommendations.
        """
        
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9,
                "num_predict": 800
            }
        }
        
        response = self._make_request("/api/generate", data)
        
        if "error" in response:
            return {"error": f"Analysis failed: {response['error']}"}
        
        # Parse analysis from response
        analysis = {}
        if "response" in response:
            text = response["response"]
            analysis = {
                "analysis": text.strip(),
                "summary": "Code analysis completed"
            }
        else:
            analysis = {"error": "No analysis available"}
        
        return analysis
    
    def test_connection(self) -> bool:
        """Test if Ollama API is accessible"""
        try:
            data = {
                "model": self.model,
                "prompt": "Hello",
                "stream": False,
                "options": {
                    "num_predict": 10
                }
            }
            response = self._make_request("/api/generate", data)
            return "error" not in response
        except Exception:
            return False
