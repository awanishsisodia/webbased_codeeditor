"""
Safe Python code execution utility
"""

import subprocess
import tempfile
import os
import sys
import traceback
from typing import Dict, Any
from io import StringIO
import contextlib

class CodeExecutor:
    """Safe Python code execution with sandboxing"""
    
    def __init__(self):
        self.timeout = 10  # seconds
        self.max_output_size = 10000  # characters
        
    def execute(self, code: str) -> Dict[str, Any]:
        """Execute Python code safely and return results"""
        if not code.strip():
            return {"output": "", "error": "No code provided"}
        
        # Create temporary file for execution
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name
        
        try:
            # Execute the code
            result = self._run_code(temp_file_path)
            return result
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except OSError:
                pass
    
    def _run_code(self, file_path: str) -> Dict[str, Any]:
        """Run Python code from file"""
        try:
            # Capture stdout and stderr
            output_buffer = StringIO()
            error_buffer = StringIO()
            
            with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(error_buffer):
                # Execute the code
                result = subprocess.run(
                    [sys.executable, file_path],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    cwd=os.getcwd()
                )
            
            # Get output and errors
            stdout = output_buffer.getvalue()
            stderr = error_buffer.getvalue()
            
            # Combine captured output with subprocess output
            combined_output = stdout + result.stdout
            combined_error = stderr + result.stderr
            
            # Truncate output if too long
            if len(combined_output) > self.max_output_size:
                combined_output = combined_output[:self.max_output_size] + "\n... (output truncated)"
            
            if len(combined_error) > self.max_output_size:
                combined_error = combined_error[:self.max_output_size] + "\n... (error truncated)"
            
            # Check for execution errors
            if result.returncode != 0:
                return {
                    "output": combined_output,
                    "error": combined_error or "Code execution failed",
                    "return_code": result.returncode
                }
            
            return {
                "output": combined_output,
                "error": None,
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "output": "",
                "error": f"Code execution timed out after {self.timeout} seconds"
            }
        except subprocess.SubprocessError as e:
            return {
                "output": "",
                "error": f"Subprocess error: {str(e)}"
            }
        except Exception as e:
            return {
                "output": "",
                "error": f"Execution error: {str(e)}"
            }
    
    def execute_interactive(self, code: str) -> Dict[str, Any]:
        """Execute code in interactive mode (for REPL-like behavior)"""
        try:
            # Create a new Python process
            process = subprocess.Popen(
                [sys.executable, '-i', '-c', code],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=self.timeout
            )
            
            stdout, stderr = process.communicate(timeout=self.timeout)
            
            if process.returncode != 0:
                return {
                    "output": stdout,
                    "error": stderr or "Interactive execution failed",
                    "return_code": process.returncode
                }
            
            return {
                "output": stdout,
                "error": None,
                "return_code": process.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "output": "",
                "error": f"Interactive execution timed out after {self.timeout} seconds"
            }
        except Exception as e:
            return {
                "output": "",
                "error": f"Interactive execution error: {str(e)}"
            }
    
    def validate_code(self, code: str) -> Dict[str, Any]:
        """Validate Python code syntax without execution"""
        try:
            compile(code, '<string>', 'exec')
            return {"valid": True, "error": None}
        except SyntaxError as e:
            return {
                "valid": False,
                "error": f"Syntax error: {e.msg} at line {e.lineno}",
                "line": e.lineno,
                "offset": e.offset
            }
        except Exception as e:
            return {
                "valid": False,
                "error": f"Validation error: {str(e)}"
            }
    
    def get_code_info(self, code: str) -> Dict[str, Any]:
        """Get information about the code without execution"""
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        return {
            "total_lines": len(lines),
            "non_empty_lines": len(non_empty_lines),
            "characters": len(code),
            "has_functions": "def " in code,
            "has_classes": "class " in code,
            "has_imports": any(keyword in code for keyword in ["import ", "from "]),
            "has_loops": any(keyword in code for keyword in ["for ", "while "]),
            "has_conditionals": any(keyword in code for keyword in ["if ", "elif ", "else:"]),
        }
