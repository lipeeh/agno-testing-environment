"""File Tools for AgentOS."""

import os
import json
import logging
import hashlib
import mimetypes
from pathlib import Path
from typing import Dict, Any, Optional
from agno.tools import tool

logger = logging.getLogger(__name__)

class FileTools:
    """Secure file operation tools."""
    
    def __init__(self):
        self.max_file_size = self._parse_size(os.getenv("MAX_FILE_SIZE", "50MB"))
        self.base_path = Path("/tmp/agno_files")
        self.allowed_extensions = {
            '.txt', '.json', '.csv', '.md', '.py', '.js', '.html', '.css',
            '.xml', '.yml', '.yaml', '.log', '.conf', '.cfg', '.ini'
        }
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def _parse_size(self, size_str: str) -> int:
        size_str = size_str.upper().strip()
        if size_str.endswith('KB'):
            return int(size_str[:-2]) * 1024
        if size_str.endswith('MB'):
            return int(size_str[:-2]) * 1024 * 1024
        if size_str.endswith('GB'):
            return int(size_str[:-2]) * 1024 * 1024 * 1024
        return int(size_str)
    
    def _sanitize_path(self, filename: str) -> Path:
        clean = str(filename).replace('..', '').replace('/', '_').replace('\\', '_')
        return self.base_path / clean
    
    def _check_size(self, b: bytes) -> Optional[str]:
        if len(b) > self.max_file_size:
            return f"Content size {len(b)} exceeds max {self.max_file_size}"
        return None
    
    @tool
    def create_file(self, filename: str, content: str, encoding: str = "utf-8") -> Dict[str, Any]:
        if Path(filename).suffix.lower() not in self.allowed_extensions:
            return {"success": False, "error": "Extension not allowed"}
        path = self._sanitize_path(filename)
        b = content.encode(encoding)
        err = self._check_size(b)
        if err:
            return {"success": False, "error": err}
        with open(path, 'w', encoding=encoding) as f:
            f.write(content)
        return {"success": True, "path": str(path), "size": len(b)}
    
    @tool
    def read_file(self, filename: str, encoding: str = "utf-8", max_lines: Optional[int] = None) -> Dict[str, Any]:
        path = self._sanitize_path(filename)
        if not path.exists():
            return {"success": False, "error": "Not found"}
        if path.stat().st_size > self.max_file_size:
            return {"success": False, "error": "File too large"}
        if max_lines:
            lines = []
            with open(path, 'r', encoding=encoding) as f:
                for i, line in enumerate(f):
                    if i >= max_lines:
                        break
                    lines.append(line.rstrip('\n\r'))
            content = '\n'.join(lines)
        else:
            content = path.read_text(encoding=encoding)
        return {"success": True, "content": content, "size": path.stat().st_size}
    
    @tool
    def list_files(self, pattern: str = "*") -> Dict[str, Any]:
        items = []
        for p in self.base_path.glob(pattern):
            if p.is_file():
                items.append({"name": p.name, "size": p.stat().st_size})
        items.sort(key=lambda x: x["name"])
        return {"success": True, "files": items, "count": len(items)}
    
    @tool
    def delete_file(self, filename: str) -> Dict[str, Any]:
        path = self._sanitize_path(filename)
        if not path.exists():
            return {"success": False, "error": "Not found"}
        size = path.stat().st_size
        path.unlink()
        return {"success": True, "size_freed": size}
    
    @tool
    def get_file_info(self, filename: str) -> Dict[str, Any]:
        path = self._sanitize_path(filename)
        if not path.exists():
            return {"success": False, "error": "Not found"}
        stat = path.stat()
        return {
            "success": True,
            "info": {
                "name": filename,
                "size": stat.st_size,
                "modified": stat.st_mtime,
                "mime": mimetypes.guess_type(filename)[0]
            }
        }
