"""Common deployment utilities shared across platforms."""

import sys
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
import json


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class DeploymentUtilities:
    """Shared utilities for deployment scripts."""

    def __init__(self, verbose: bool = False):
        """
        Initialize deployment utilities.

        Args:
            verbose: Enable verbose output
        """
        self.verbose = verbose
        self.framework_root = Path(__file__).parent.parent.absolute()

    # ===== Output Methods =====

    def print_header(self, message: str) -> None:
        """Print formatted header."""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{message.center(80)}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")

    def print_success(self, message: str) -> None:
        """Print success message."""
        print(f"{Colors.GREEN}✓ {message}{Colors.ENDC}")

    def print_warning(self, message: str) -> None:
        """Print warning message."""
        print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")

    def print_error(self, message: str) -> None:
        """Print error message."""
        print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

    def print_info(self, message: str) -> None:
        """Print info message."""
        print(f"{Colors.CYAN}ℹ {message}{Colors.ENDC}")

    # ===== Command Execution =====

    def run_command(self, command: str, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess:
        """
        Run shell command.

        Args:
            command: Command to run
            check: Raise exception on failure
            capture: Capture output

        Returns:
            CompletedProcess result
        """
        if self.verbose:
            self.print_info(f"Running: {command}")

        result = subprocess.run(
            command,
            shell=True,
            check=check,
            capture_output=capture,
            text=True
        )
        return result

    # ===== File Operations =====

    def copy_template(self, template_name: str, destination: Path, replacements: Dict[str, str] = None) -> None:
        """
        Copy template file and optionally perform replacements.

        Args:
            template_name: Name of template file (e.g., 'pytest.ini.template')
            destination: Destination file path
            replacements: Dictionary of {placeholder: value} for template substitution
        """
        # Find template file
        template_path = None
        for search_dir in ['common', 'ios', 'android']:
            candidate = self.framework_root / 'templates' / search_dir / template_name
            if candidate.exists():
                template_path = candidate
                break

        if not template_path:
            raise FileNotFoundError(f"Template not found: {template_name}")

        # Read template
        with open(template_path, 'r') as f:
            content = f.read()

        # Perform replacements
        if replacements:
            for placeholder, value in replacements.items():
                content = content.replace(f"{{{{{placeholder}}}}}", str(value))

        # Write to destination
        destination.parent.mkdir(parents=True, exist_ok=True)
        with open(destination, 'w') as f:
            f.write(content)

        if self.verbose:
            self.print_info(f"Created: {destination.name}")

    def create_directory_structure(self, base_dir: Path, structure: Dict[str, Any]) -> None:
        """
        Create directory structure from dictionary.

        Args:
            base_dir: Base directory path
            structure: Dictionary defining structure
                      {
                          'dir_name': {
                              'subdir': {},
                              'file.txt': 'content'
                          }
                      }
        """
        for name, content in structure.items():
            path = base_dir / name

            if isinstance(content, dict):
                # It's a directory
                path.mkdir(parents=True, exist_ok=True)
                if content:  # Has subdirectories/files
                    self.create_directory_structure(path, content)
            elif isinstance(content, str):
                # It's a file with content
                path.parent.mkdir(parents=True, exist_ok=True)
                with open(path, 'w') as f:
                    f.write(content)
            elif content is None:
                # Empty directory
                path.mkdir(parents=True, exist_ok=True)

    # ===== Python Environment =====

    def create_virtual_environment(self, project_dir: Path) -> bool:
        """
        Create Python virtual environment.

        Args:
            project_dir: Project directory

        Returns:
            True if successful
        """
        venv_path = project_dir / 'venv'

        if venv_path.exists():
            self.print_warning("Virtual environment already exists")
            return True

        try:
            self.print_info("Creating virtual environment...")
            self.run_command(f'python3 -m venv "{venv_path}"', check=True)
            self.print_success("Virtual environment created")

            return True
        except subprocess.CalledProcessError as e:
            self.print_error(f"Virtual environment creation failed: {e}")
            return False

    def install_dependencies(self, project_dir: Path) -> bool:
        """
        Install Python dependencies.

        Args:
            project_dir: Project directory

        Returns:
            True if successful
        """
        venv_path = project_dir / 'venv'
        requirements_file = project_dir / 'requirements.txt'

        if not venv_path.exists():
            self.print_error("Virtual environment not found")
            return False

        if not requirements_file.exists():
            self.print_error("requirements.txt not found")
            return False

        try:
            self.print_info("Installing dependencies...")
            pip_cmd = f'"{venv_path / "bin/pip"}" install -r "{requirements_file}"'
            self.run_command(pip_cmd, check=True)
            self.print_success("Dependencies installed")

            return True
        except subprocess.CalledProcessError as e:
            self.print_error(f"Dependency installation failed: {e}")
            return False

    # ===== App Name Detection =====

    def detect_app_name(self, app_path: Path) -> str:
        """
        Detect app name from path.

        Args:
            app_path: Path to app project

        Returns:
            Detected app name
        """
        # For iOS projects, look for .xcodeproj
        xcodeprojects = list(app_path.glob('*.xcodeproj'))
        if xcodeprojects:
            return xcodeprojects[0].stem

        # For Android projects, look for app module or settings.gradle
        # TODO: Implement Android app name detection

        # Fallback: use directory name
        return app_path.name

    def create_automation_project_path(self, app_path: Path, output_dir: Optional[Path], app_name: Optional[str]) -> Path:
        """
        Create path for automation project.

        Args:
            app_path: Path to app project
            output_dir: Optional output directory
            app_name: Optional app name override

        Returns:
            Path for automation project
        """
        # Determine app name
        if app_name is None:
            app_name = self.detect_app_name(app_path)

        # Determine output directory
        if output_dir is None:
            output_dir = app_path.parent

        # Create automation project name
        automation_project_name = f"{app_name}-Automation"

        return output_dir / automation_project_name

    # ===== Configuration =====

    def save_json_config(self, file_path: Path, config: Dict[str, Any]) -> None:
        """
        Save JSON configuration file.

        Args:
            file_path: Path to JSON file
            config: Configuration dictionary
        """
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w') as f:
            json.dump(config, f, indent=2)

        if self.verbose:
            self.print_info(f"Saved config: {file_path.name}")

    # ===== Validation =====

    def validate_python(self) -> bool:
        """
        Validate Python installation.

        Returns:
            True if Python 3.8+ found
        """
        try:
            result = self.run_command('python3 --version', check=True, capture=True)
            version_str = result.stdout.strip()
            self.print_success(f"Python found: {version_str}")

            # Check version
            version = version_str.split()[1]
            major, minor = map(int, version.split('.')[:2])

            if major < 3 or (major == 3 and minor < 8):
                self.print_error("Python 3.8+ required")
                return False

            return True
        except subprocess.CalledProcessError:
            self.print_error("Python 3.8+ not found")
            return False

    def validate_appium(self) -> bool:
        """
        Validate Appium installation.

        Returns:
            True if Appium found
        """
        try:
            result = self.run_command('appium --version', check=True, capture=True)
            version = result.stdout.strip()
            self.print_success(f"Appium found: {version}")
            return True
        except subprocess.CalledProcessError:
            self.print_warning("Appium not installed")
            self.print_info("Install: npm install -g appium")
            return False
