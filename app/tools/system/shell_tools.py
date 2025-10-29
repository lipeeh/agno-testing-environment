"""Shell Tools for AgentOS."""

import os
import json
import logging
import subprocess
import shlex
import platform
from typing import Dict, Any, List, Optional
from agno.tools import tool

logger = logging.getLogger(__name__)

class ShellTools:
    """Secure shell command execution tools."""
    
    def __init__(self):
        # Get allowed commands from environment or use defaults
        default_commands = "curl,git,ls,cat,head,tail,grep,pwd,whoami,date,echo,find,wc,sort,uniq"
        allowed_commands_str = os.getenv("ALLOWED_COMMANDS", default_commands)
        self.allowed_commands = set(cmd.strip() for cmd in allowed_commands_str.split(','))
        
        self.timeout = 30  # seconds
        self.max_output_size = 10000  # characters
        self.working_directory = "/tmp/agno_shell"
        
        # Ensure working directory exists
        os.makedirs(self.working_directory, exist_ok=True)
    
    def _is_command_allowed(self, command: str) -> bool:
        """Check if command is in whitelist."""
        # Extract the base command (first word)
        base_command = command.strip().split()[0] if command.strip() else ""
        return base_command in self.allowed_commands
    
    def _sanitize_command(self, command: str) -> str:
        """Basic command sanitization."""
        # Remove dangerous characters and patterns
        dangerous_patterns = [
            '&&', '||', ';', '|', '>', '>>', '<', '`', '$(',
            'rm -rf', 'chmod', 'chown', 'sudo', 'su', 'passwd'
        ]
        
        sanitized = command.strip()
        for pattern in dangerous_patterns:
            if pattern in sanitized.lower():
                raise ValueError(f"Dangerous pattern detected: {pattern}")
        
        return sanitized
    
    @tool
    def execute_command(self, command: str, timeout: Optional[int] = None) -> Dict[str, Any]:
        """
        Execute a shell command in a sandboxed environment.
        
        Args:
            command: The shell command to execute
            timeout: Command timeout in seconds (default: 30)
            
        Returns:
            Dictionary with command output, error, and execution info
        """
        try:
            if not command or not command.strip():
                return {
                    "success": False,
                    "error": "Empty command provided"
                }
            
            # Check if command is allowed
            if not self._is_command_allowed(command):
                base_command = command.strip().split()[0]
                return {
                    "success": False,
                    "error": f"Command '{base_command}' not allowed. Allowed commands: {', '.join(sorted(self.allowed_commands))}"
                }
            
            # Sanitize command
            try:
                sanitized_command = self._sanitize_command(command)
            except ValueError as e:
                return {
                    "success": False,
                    "error": str(e)
                }
            
            # Set timeout
            exec_timeout = timeout or self.timeout
            
            logger.info(f"Executing command: {sanitized_command} (timeout: {exec_timeout}s)")
            
            # Execute command
            process = subprocess.run(
                sanitized_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=exec_timeout,
                cwd=self.working_directory,
                env={
                    "PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin"),
                    "HOME": self.working_directory,
                    "USER": "agno",
                    "SHELL": "/bin/bash"
                }
            )
            
            # Limit output size
            stdout = process.stdout[:self.max_output_size] if process.stdout else ""
            stderr = process.stderr[:self.max_output_size] if process.stderr else ""
            
            # Prepare result
            result = {
                "success": process.returncode == 0,
                "command": sanitized_command,
                "return_code": process.returncode,
                "stdout": stdout,
                "stderr": stderr,
                "execution_time": exec_timeout,
                "output_truncated": len(process.stdout or "") > self.max_output_size or len(process.stderr or "") > self.max_output_size
            }
            
            if process.returncode != 0:
                result["error"] = f"Command failed with return code {process.returncode}"
            
            logger.info(f"Command executed successfully: {sanitized_command} (return code: {process.returncode})")
            return result
            
        except subprocess.TimeoutExpired:
            logger.error(f"Command timeout: {command}")
            return {
                "success": False,
                "error": f"Command timed out after {exec_timeout} seconds",
                "command": command,
                "timeout": exec_timeout
            }
        except FileNotFoundError as e:
            logger.error(f"Command not found: {command} - {str(e)}")
            return {
                "success": False,
                "error": f"Command not found: {str(e)}",
                "command": command
            }
        except PermissionError as e:
            logger.error(f"Permission denied: {command} - {str(e)}")
            return {
                "success": False,
                "error": f"Permission denied: {str(e)}",
                "command": command
            }
        except Exception as e:
            logger.error(f"Unexpected error executing command {command}: {str(e)}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "command": command
            }
    
    @tool
    def list_allowed_commands(self) -> Dict[str, Any]:
        """
        List all allowed shell commands.
        
        Returns:
            Dictionary with list of allowed commands and configuration
        """
        return {
            "success": True,
            "allowed_commands": sorted(list(self.allowed_commands)),
            "total_commands": len(self.allowed_commands),
            "timeout": self.timeout,
            "max_output_size": self.max_output_size,
            "working_directory": self.working_directory
        }
    
    @tool
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get basic system information using safe commands.
        
        Returns:
            Dictionary with system information
        """
        try:
            system_info = {
                "success": True,
                "platform": platform.system(),
                "platform_release": platform.release(),
                "platform_version": platform.version(),
                "architecture": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version(),
                "working_directory": self.working_directory
            }
            
            # Try to get additional info with safe commands
            safe_commands = {
                "current_user": "whoami",
                "current_directory": "pwd",
                "current_date": "date",
                "disk_usage": "df -h ."
            }
            
            for info_name, cmd in safe_commands.items():
                if self._is_command_allowed(cmd):
                    try:
                        result = subprocess.run(
                            cmd,
                            shell=True,
                            capture_output=True,
                            text=True,
                            timeout=5,
                            cwd=self.working_directory
                        )
                        if result.returncode == 0:
                            system_info[info_name] = result.stdout.strip()
                    except Exception as e:
                        system_info[info_name] = f"Error: {str(e)}"
                else:
                    system_info[info_name] = "Command not allowed"
            
            logger.info("System info retrieved successfully")
            return system_info
            
        except Exception as e:
            logger.error(f"Error getting system info: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to get system info: {str(e)}"
            }
    
    @tool
    def check_command_safety(self, command: str) -> Dict[str, Any]:
        """
        Check if a command is safe to execute without running it.
        
        Args:
            command: The command to check
            
        Returns:
            Dictionary with safety analysis
        """
        try:
            analysis = {
                "command": command,
                "is_allowed": False,
                "base_command": "",
                "safety_issues": [],
                "recommendations": []
            }
            
            if not command or not command.strip():
                analysis["safety_issues"].append("Empty command")
                return {"success": True, "analysis": analysis}
            
            # Extract base command
            base_command = command.strip().split()[0]
            analysis["base_command"] = base_command
            
            # Check if allowed
            analysis["is_allowed"] = self._is_command_allowed(command)
            
            if not analysis["is_allowed"]:
                analysis["safety_issues"].append(f"Command '{base_command}' not in whitelist")
                analysis["recommendations"].append(f"Use one of the allowed commands: {', '.join(sorted(self.allowed_commands))}")
            
            # Check for dangerous patterns
            dangerous_patterns = [
                ('&&', 'Command chaining detected'),
                ('||', 'Command chaining detected'),
                (';', 'Command separator detected'),
                ('|', 'Pipe detected'),
                ('>', 'Output redirection detected'),
                ('>>', 'Output redirection detected'),
                ('<', 'Input redirection detected'),
                ('`', 'Command substitution detected'),
                ('$(', 'Command substitution detected'),
                ('rm -rf', 'Dangerous deletion command'),
                ('chmod', 'Permission modification command'),
                ('sudo', 'Privilege escalation command')
            ]
            
            for pattern, issue in dangerous_patterns:
                if pattern in command.lower():
                    analysis["safety_issues"].append(issue)
                    analysis["recommendations"].append(f"Avoid using '{pattern}' in commands")
            
            # Overall safety assessment
            analysis["is_safe"] = len(analysis["safety_issues"]) == 0
            
            return {
                "success": True,
                "analysis": analysis
            }
            
        except Exception as e:
            logger.error(f"Error checking command safety: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to check command safety: {str(e)}"
            }
