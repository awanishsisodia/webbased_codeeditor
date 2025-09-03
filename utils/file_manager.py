"""
File system management utility for the code editor
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

class FileManager:
    """Manages file system operations for the code editor"""
    
    def __init__(self, workspace_dir: str):
        self.workspace_dir = Path(workspace_dir).resolve()
        self.ensure_workspace_exists()
    
    def ensure_workspace_exists(self):
        """Ensure workspace directory exists"""
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
    
    def list_files(self, path: str = "") -> List[Dict[str, Any]]:
        """List files and directories in the specified path"""
        try:
            target_path = self.workspace_dir / path if path else self.workspace_dir
            if not target_path.exists():
                return []
            
            items = []
            for item in target_path.iterdir():
                if item.name.startswith('.'):  # Skip hidden files
                    continue
                
                item_info = {
                    "name": item.name,
                    "path": str(item.relative_to(self.workspace_dir)),
                    "type": "directory" if item.is_dir() else "file",
                    "size": self._get_file_size(item),
                    "modified": self._get_modified_time(item),
                    "extension": item.suffix if item.is_file() else ""
                }
                
                if item.is_file():
                    item_info["readable"] = self._is_readable_file(item)
                    item_info["writable"] = self._is_writable_file(item)
                
                items.append(item_info)
            
            # Sort: directories first, then files alphabetically
            items.sort(key=lambda x: (x["type"] == "file", x["name"].lower()))
            return items
            
        except Exception as e:
            print(f"Error listing files: {e}")
            return []
    
    def read_file(self, file_path: str) -> str:
        """Read content of a file"""
        try:
            target_path = self.workspace_dir / file_path
            if not target_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            if not target_path.is_file():
                raise ValueError(f"Path is not a file: {file_path}")
            
            # Only allow reading Python files and text files
            if not self._is_safe_file(target_path):
                raise ValueError(f"File type not allowed: {file_path}")
            
            with open(target_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        except Exception as e:
            raise Exception(f"Failed to read file {file_path}: {str(e)}")
    
    def save_file(self, file_path: str, content: str) -> None:
        """Save content to a file"""
        try:
            target_path = self.workspace_dir / file_path
            
            # Ensure parent directory exists
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Only allow saving Python files and text files
            if not self._is_safe_file(target_path):
                raise ValueError(f"File type not allowed: {file_path}")
            
            # Write content to file
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            raise Exception(f"Failed to save file {file_path}: {str(e)}")
    
    def delete_file(self, file_path: str) -> None:
        """Delete a file or directory"""
        try:
            target_path = self.workspace_dir / file_path
            
            if not target_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Prevent deletion of workspace root
            if target_path == self.workspace_dir:
                raise ValueError("Cannot delete workspace root")
            
            if target_path.is_file():
                target_path.unlink()
            elif target_path.is_dir():
                self._delete_directory(target_path)
                
        except Exception as e:
            raise Exception(f"Failed to delete {file_path}: {str(e)}")
    
    def create_directory(self, dir_path: str) -> None:
        """Create a new directory"""
        try:
            target_path = self.workspace_dir / dir_path
            target_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise Exception(f"Failed to create directory {dir_path}: {str(e)}")
    
    def rename_file(self, old_path: str, new_path: str) -> None:
        """Rename a file or directory"""
        try:
            old_target = self.workspace_dir / old_path
            new_target = self.workspace_dir / new_path
            
            if not old_target.exists():
                raise FileNotFoundError(f"File not found: {old_path}")
            
            if new_target.exists():
                raise ValueError(f"Target already exists: {new_path}")
            
            old_target.rename(new_target)
            
        except Exception as e:
            raise Exception(f"Failed to rename {old_path} to {new_path}: {str(e)}")
    
    def copy_file(self, source_path: str, dest_path: str) -> None:
        """Copy a file"""
        try:
            source_target = self.workspace_dir / source_path
            dest_target = self.workspace_dir / dest_path
            
            if not source_target.exists():
                raise FileNotFoundError(f"Source file not found: {source_path}")
            
            if not source_target.is_file():
                raise ValueError(f"Source is not a file: {source_path}")
            
            # Ensure destination directory exists
            dest_target.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            import shutil
            shutil.copy2(source_target, dest_target)
            
        except Exception as e:
            raise Exception(f"Failed to copy {source_path} to {dest_path}: {str(e)}")
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get detailed information about a file"""
        try:
            target_path = self.workspace_dir / file_path
            
            if not target_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            stat = target_path.stat()
            
            info = {
                "name": target_path.name,
                "path": str(target_path.relative_to(self.workspace_dir)),
                "type": "directory" if target_path.is_dir() else "file",
                "size": self._get_file_size(target_path),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
                "permissions": oct(stat.st_mode)[-3:],
                "readable": os.access(target_path, os.R_OK),
                "writable": os.access(target_path, os.W_OK),
                "executable": os.access(target_path, os.X_OK)
            }
            
            if target_path.is_file():
                info["extension"] = target_path.suffix
                info["mime_type"] = self._get_mime_type(target_path)
            
            return info
            
        except Exception as e:
            raise Exception(f"Failed to get file info for {file_path}: {str(e)}")
    
    def _get_file_size(self, path: Path) -> str:
        """Get human-readable file size"""
        try:
            if path.is_file():
                size = path.stat().st_size
                for unit in ['B', 'KB', 'MB', 'GB']:
                    if size < 1024.0:
                        return f"{size:.1f} {unit}"
                    size /= 1024.0
                return f"{size:.1f} TB"
            elif path.is_dir():
                return "Directory"
            else:
                return "Unknown"
        except:
            return "Unknown"
    
    def _get_modified_time(self, path: Path) -> str:
        """Get human-readable modified time"""
        try:
            mtime = path.stat().st_mtime
            return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        except:
            return "Unknown"
    
    def _is_readable_file(self, path: Path) -> bool:
        """Check if file is readable"""
        return os.access(path, os.R_OK)
    
    def _is_writable_file(self, path: Path) -> bool:
        """Check if file is writable"""
        return os.access(path, os.W_OK)
    
    def _is_safe_file(self, path: Path) -> bool:
        """Check if file type is safe for editing"""
        safe_extensions = {'.py', '.txt', '.md', '.json', '.yaml', '.yml', '.ini', '.cfg', '.log'}
        return path.suffix.lower() in safe_extensions
    
    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type of file"""
        import mimetypes
        mime_type, _ = mimetypes.guess_type(str(path))
        return mime_type or 'application/octet-stream'
    
    def _delete_directory(self, path: Path) -> None:
        """Recursively delete a directory"""
        import shutil
        shutil.rmtree(path)
    
    def search_files(self, query: str, file_types: List[str] = None) -> List[Dict[str, Any]]:
        """Search for files by name or content"""
        try:
            results = []
            
            for root, dirs, files in os.walk(self.workspace_dir):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    if file.startswith('.'):
                        continue
                    
                    file_path = Path(root) / file
                    
                    # Filter by file type if specified
                    if file_types and file_path.suffix.lower() not in file_types:
                        continue
                    
                    # Search in filename
                    if query.lower() in file.lower():
                        results.append({
                            "name": file,
                            "path": str(file_path.relative_to(self.workspace_dir)),
                            "type": "file",
                            "match_type": "filename"
                        })
                        continue
                    
                    # Search in file content (for text files only)
                    if self._is_safe_file(file_path):
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if query.lower() in content.lower():
                                    results.append({
                                        "name": file,
                                        "path": str(file_path.relative_to(self.workspace_dir)),
                                        "type": "file",
                                        "match_type": "content"
                                    })
                        except:
                            continue
            
            return results
            
        except Exception as e:
            print(f"Error searching files: {e}")
            return []
