#!/usr/bin/env python3
"""
iOS Automation Project Deployment Script.

This script creates a complete, independent automation project for iOS apps.
It can be run against any iOS Xcode project to generate a ready-to-use
test automation suite.

Usage:
    python deploy_ios.py --app-path ~/Projects/YourApp
    python deploy_ios.py --app-path ~/Projects/YourApp --output-dir ~/Automation
    python deploy_ios.py --app-path ~/Projects/YourApp --app-name "MyApp" --skip-build
"""

import sys
import argparse
from pathlib import Path
from typing import Optional
import subprocess

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from deploy.common import DeploymentUtilities, Colors


class iOSDeployment:
    """Manages iOS automation project deployment."""

    def __init__(self, verbose: bool = False):
        """
        Initialize iOS deployment.

        Args:
            verbose: Enable verbose output
        """
        self.utils = DeploymentUtilities(verbose=verbose)
        self.verbose = verbose
        self.app_path: Optional[Path] = None
        self.bundle_id: Optional[str] = None
        self.app_name: Optional[str] = None
        self.built_app_path: Optional[Path] = None

    # ===== iOS-Specific Validation =====

    def validate_ios_prerequisites(self) -> bool:
        """
        Validate iOS-specific prerequisites.

        Returns:
            True if all prerequisites met
        """
        self.utils.print_header("Validating iOS Prerequisites")

        all_valid = True

        # Check Python
        if not self.utils.validate_python():
            all_valid = False

        # Check Xcode
        try:
            result = self.utils.run_command('xcodebuild -version', check=True, capture=True)
            version = result.stdout.strip().split('\n')[0]
            self.utils.print_success(f"Xcode found: {version}")
        except subprocess.CalledProcessError:
            self.utils.print_error("Xcode not found")
            all_valid = False

        # Check iOS Simulators
        try:
            result = self.utils.run_command('xcrun simctl list devices available', check=True, capture=True)
            if 'iPhone' in result.stdout:
                self.utils.print_success("iOS Simulators found")
            else:
                self.utils.print_warning("No iOS Simulators found")
        except subprocess.CalledProcessError:
            self.utils.print_error("xcrun command failed")
            all_valid = False

        # Check Appium
        if not self.utils.validate_appium():
            self.utils.print_warning("Appium not installed - will provide installation instructions")

        # Check XCUITest driver
        try:
            result = self.utils.run_command('appium driver list', check=True, capture=True)
            if 'xcuitest' in result.stdout.lower():
                self.utils.print_success("XCUITest driver found")
            else:
                self.utils.print_warning("XCUITest driver not installed")
                self.utils.print_info("Install: appium driver install xcuitest")
        except subprocess.CalledProcessError:
            self.utils.print_warning("Could not check Appium drivers")

        return all_valid

    # ===== iOS App Building =====

    def find_xcodeproj(self, project_path: Path) -> Optional[Path]:
        """
        Find .xcodeproj file in project directory.

        Args:
            project_path: Project directory

        Returns:
            Path to .xcodeproj or None
        """
        xcodeprojects = list(project_path.glob('*.xcodeproj'))

        if not xcodeprojects:
            self.utils.print_error("No .xcodeproj file found")
            return None

        if len(xcodeprojects) > 1:
            self.utils.print_warning(f"Multiple .xcodeproj files found, using: {xcodeprojects[0].name}")

        return xcodeprojects[0]

    def build_ios_app(self, project_path: Path) -> Optional[Path]:
        """
        Build iOS app for simulator.

        Args:
            project_path: Path to Xcode project directory

        Returns:
            Path to built .app bundle or None
        """
        self.utils.print_header("Building iOS Application")

        xcodeproj = self.find_xcodeproj(project_path)
        if not xcodeproj:
            return None

        self.utils.print_info(f"Found project: {xcodeproj.name}")

        # Get scheme name (usually same as project name)
        scheme_name = xcodeproj.stem

        # Build for simulator
        build_dir = project_path / 'build'
        build_command = f"""
        xcodebuild \
            -project "{xcodeproj}" \
            -scheme "{scheme_name}" \
            -sdk iphonesimulator \
            -configuration Debug \
            -derivedDataPath "{build_dir}" \
            build
        """

        self.utils.print_info(f"Building {scheme_name} for simulator...")
        self.utils.print_info("This may take a few minutes...")

        try:
            self.utils.run_command(build_command, check=True)
            self.utils.print_success("Build completed successfully")
        except subprocess.CalledProcessError as e:
            self.utils.print_error(f"Build failed: {e}")
            return None

        # Find .app bundle
        app_bundles = list(build_dir.glob('**/Build/Products/Debug-iphonesimulator/*.app'))

        if not app_bundles:
            self.utils.print_error("Could not find built .app bundle")
            return None

        app_path = app_bundles[0]
        self.utils.print_success(f"App bundle found: {app_path.name}")

        return app_path

    def extract_bundle_id(self, app_path: Path) -> Optional[str]:
        """
        Extract bundle ID from Info.plist.

        Args:
            app_path: Path to .app bundle

        Returns:
            Bundle ID or None
        """
        info_plist = app_path / 'Info.plist'

        if not info_plist.exists():
            self.utils.print_warning("Info.plist not found")
            return None

        try:
            result = self.utils.run_command(
                f'/usr/libexec/PlistBuddy -c "Print :CFBundleIdentifier" "{info_plist}"',
                check=True,
                capture=True
            )
            bundle_id = result.stdout.strip()
            self.utils.print_success(f"Bundle ID: {bundle_id}")
            return bundle_id
        except subprocess.CalledProcessError:
            self.utils.print_error("Failed to extract bundle ID")
            return None

    def get_simulator_info(self) -> dict:
        """
        Get default iOS simulator information.

        Returns:
            Dictionary with device name, version, and UDID
        """
        try:
            result = self.utils.run_command(
                'xcrun simctl list devices available -j',
                check=True,
                capture=True
            )

            import json
            devices = json.loads(result.stdout)

            # Find first available iPhone
            for runtime, device_list in devices['devices'].items():
                if 'iOS' in runtime:
                    for device in device_list:
                        if 'iPhone' in device['name']:
                            # Extract iOS version from runtime
                            ios_version = runtime.split('.')[-1].replace('-', '.')
                            return {
                                'device_name': device['name'],
                                'ios_version': ios_version,
                                'udid': device['udid']
                            }

            # Fallback
            return {
                'device_name': 'iPhone 15',
                'ios_version': '17.0',
                'udid': 'auto'
            }

        except:
            # Fallback
            return {
                'device_name': 'iPhone 15',
                'ios_version': '17.0',
                'udid': 'auto'
            }

    # ===== Project Creation =====

    def create_project_structure(self, automation_project_path: Path) -> None:
        """
        Create automation project directory structure.

        Args:
            automation_project_path: Path for automation project
        """
        self.utils.print_header("Creating Project Structure")

        structure = {
            'config': {
                'ios': None,
                'android': {'README.md': 'Android support coming soon.\n'},
                '__init__.py': ''
            },
            'tests': {
                'ios': {'__init__.py': ''},
                'android': {'__init__.py': '', 'README.md': 'Android tests will go here.\n'},
                'cross_platform': {'__init__.py': '', 'README.md': 'Cross-platform tests will go here.\n'},
                '__init__.py': ''
            },
            'pages': {
                'ios': {'__init__.py': ''},
                'android': {'__init__.py': '', 'README.md': 'Android page objects will go here.\n'},
                '__init__.py': ''
            },
            'utils': {'__init__.py': ''},
            'data': None,
            'reports': {
                'ios': None,
                'android': None
            },
            'screenshots': {
                'ios': None,
                'android': None
            },
            'logs': None
        }

        self.utils.create_directory_structure(automation_project_path, structure)
        self.utils.print_success("Project structure created")

    def copy_templates(self, automation_project_path: Path) -> None:
        """
        Copy and configure template files.

        Args:
            automation_project_path: Path to automation project
        """
        self.utils.print_header("Copying Templates")

        # Get simulator info
        sim_info = self.get_simulator_info()

        # Prepare replacements
        replacements = {
            'app_name': self.app_name,
            'app_path': str(self.built_app_path) if self.built_app_path else '',
            'bundle_id': self.bundle_id or '',
            'ios_version': sim_info['ios_version'],
            'device_name': sim_info['device_name']
        }

        # Common templates
        self.utils.copy_template(
            'requirements.txt.template',
            automation_project_path / 'requirements.txt',
            replacements
        )

        self.utils.copy_template(
            'pytest.ini.template',
            automation_project_path / 'pytest.ini',
            replacements
        )

        self.utils.copy_template(
            'gitignore.template',
            automation_project_path / '.gitignore',
            replacements
        )

        self.utils.copy_template(
            'common.json.template',
            automation_project_path / 'config' / 'common.json',
            replacements
        )

        # iOS templates
        self.utils.copy_template(
            'capabilities.json.template',
            automation_project_path / 'config' / 'ios' / 'capabilities.json',
            replacements
        )

        self.utils.copy_template(
            'conftest.py.template',
            automation_project_path / 'tests' / 'ios' / 'conftest.py',
            replacements
        )

        self.utils.copy_template(
            'base_page.py.template',
            automation_project_path / 'pages' / 'base_page.py',
            replacements
        )

        self.utils.copy_template(
            'home_page.py.template',
            automation_project_path / 'pages' / 'ios' / 'home_page.py',
            replacements
        )

        self.utils.copy_template(
            'test_smoke.py.template',
            automation_project_path / 'tests' / 'ios' / 'test_smoke.py',
            replacements
        )

        self.utils.print_success("Templates copied and configured")

    def create_project_readme(self, automation_project_path: Path) -> None:
        """
        Create project-specific README.

        Args:
            automation_project_path: Path to automation project
        """
        readme_content = f"""# {self.app_name}-Automation

iOS (and Android) automation testing for {self.app_name}.

## Quick Start

```bash
# Activate virtual environment
source venv/bin/activate

# Start Appium (in separate terminal)
appium

# Run iOS smoke tests
pytest tests/ios/ -m smoke -v

# Run all iOS tests
pytest tests/ios/ -v
```

## Project Structure

- `config/` - Configuration files (iOS/Android/common)
- `tests/` - Test suites organized by platform
- `pages/` - Page Object Model classes
- `utils/` - Utility functions and helpers
- `data/` - Test data files
- `reports/` - Test execution reports
- `screenshots/` - Failure screenshots
- `logs/` - Execution logs

## Running Tests

### iOS Tests

```bash
# Smoke tests
pytest tests/ios/ -m smoke -v

# All tests
pytest tests/ios/ -v

# Specific test
pytest tests/ios/test_smoke.py::TestiOSSmoke::test_app_launches -v

# Generate HTML report
pytest tests/ios/ --html=reports/ios/report.html
```

### Android Tests (Coming Soon)

```bash
# Once Android is implemented
pytest tests/android/ -m smoke -v
```

## Configuration

Edit `config/common.json` for general settings.
Edit `config/ios/capabilities.json` for iOS-specific configuration.

## Adding Tests

1. Create page objects in `pages/ios/` (or `pages/android/`)
2. Create tests in `tests/ios/` (or `tests/android/`)
3. Use `@pytest.mark.ios` or `@pytest.mark.android` markers
4. Use `@pytest.mark.smoke` for critical path tests

## Reports

- HTML reports: `reports/ios/` and `reports/android/`
- Screenshots: `screenshots/ios/` and `screenshots/android/`
- Logs: `logs/pytest.log`

## Troubleshooting

### Appium not starting
```bash
# Kill existing Appium
pkill -f appium

# Start fresh
appium
```

### App not launching
- Check app path in `config/ios/capabilities.json`
- Verify bundle ID is correct
- Rebuild app if needed

### Element not found
- Use Appium Inspector to verify locators
- Check if element is visible on screen
- Increase wait timeout

---

Generated by appium-multiplatform-framework
"""

        with open(automation_project_path / 'README.md', 'w') as f:
            f.write(readme_content)

        self.utils.print_success("Project README created")

    # ===== Main Deployment =====

    def deploy(
        self,
        app_path: str,
        output_dir: Optional[str] = None,
        app_name: Optional[str] = None,
        skip_build: bool = False,
        skip_venv: bool = False
    ) -> bool:
        """
        Main deployment workflow.

        Args:
            app_path: Path to iOS project
            output_dir: Optional output directory
            app_name: Optional app name override
            skip_build: Skip building the app
            skip_venv: Skip creating virtual environment

        Returns:
            True if deployment successful
        """
        # Convert paths
        app_path_obj = Path(app_path).expanduser().absolute()
        output_dir_obj = Path(output_dir).expanduser().absolute() if output_dir else None

        if not app_path_obj.exists():
            self.utils.print_error(f"App path does not exist: {app_path_obj}")
            return False

        # Step 1: Validate prerequisites
        if not self.validate_ios_prerequisites():
            self.utils.print_error("Prerequisites not met")
            return False

        # Step 2: Detect/set app name
        if app_name:
            self.app_name = app_name
        else:
            self.app_name = self.utils.detect_app_name(app_path_obj)

        self.utils.print_info(f"App name: {self.app_name}")

        # Step 3: Build app (if needed)
        if skip_build:
            self.utils.print_info("Skipping build - looking for existing .app...")
            app_bundles = list(app_path_obj.glob('**/Build/Products/Debug-iphonesimulator/*.app'))
            if app_bundles:
                self.built_app_path = app_bundles[0]
                self.utils.print_success(f"Found existing app: {self.built_app_path}")
            else:
                self.utils.print_warning("No existing .app found")
        else:
            self.built_app_path = self.build_ios_app(app_path_obj)

        # Step 4: Extract bundle ID
        if self.built_app_path:
            self.bundle_id = self.extract_bundle_id(self.built_app_path)

        # Step 5: Create automation project path
        automation_project_path = self.utils.create_automation_project_path(
            app_path_obj,
            output_dir_obj,
            self.app_name
        )

        if automation_project_path.exists():
            self.utils.print_warning(f"Project already exists: {automation_project_path}")
            response = input("Overwrite? (y/N): ")
            if response.lower() != 'y':
                self.utils.print_info("Deployment cancelled")
                return False

        self.utils.print_info(f"Creating automation project at: {automation_project_path}")

        # Step 6: Create project structure
        self.create_project_structure(automation_project_path)

        # Step 7: Copy templates
        self.copy_templates(automation_project_path)

        # Step 8: Create README
        self.create_project_readme(automation_project_path)

        # Step 9: Setup virtual environment
        if not skip_venv:
            if self.utils.create_virtual_environment(automation_project_path):
                self.utils.install_dependencies(automation_project_path)

        # Step 10: Print success and next steps
        self.print_next_steps(automation_project_path)

        return True

    def print_next_steps(self, automation_project_path: Path) -> None:
        """Print next steps for user."""
        self.utils.print_header("🎉 Deployment Complete!")

        print(f"{Colors.GREEN}Automation project created at:{Colors.ENDC}")
        print(f"  {Colors.BOLD}{automation_project_path}{Colors.ENDC}\n")

        print(f"{Colors.BOLD}Next Steps:{Colors.ENDC}\n")

        print(f"1. Navigate to project:")
        print(f"   cd {automation_project_path}\n")

        print(f"2. Activate virtual environment:")
        print(f"   source venv/bin/activate\n")

        print(f"3. Install/Start Appium (if not running):")
        print(f"   npm install -g appium")
        print(f"   appium driver install xcuitest")
        print(f"   appium  # In separate terminal\n")

        print(f"4. Update page object locators:")
        print(f"   - Edit pages/ios/home_page.py")
        print(f"   - Use Appium Inspector to find accessibility IDs\n")

        print(f"5. Run smoke tests:")
        print(f"   pytest tests/ios/ -m smoke -v\n")

        print(f"6. Run all iOS tests:")
        print(f"   pytest tests/ios/ -v\n")

        print(f"{Colors.BOLD}Useful Commands:{Colors.ENDC}")
        print(f"   pytest tests/ios/ --html=reports/ios/report.html")
        print(f"   pytest tests/ios/ -m smoke --tb=short")
        print(f"   pytest tests/ios/test_smoke.py::test_app_launches -v\n")

        print(f"{Colors.CYAN}📖 See README.md in project for full documentation{Colors.ENDC}\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Deploy iOS automation project',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python deploy_ios.py --app-path ~/Projects/AppJubilee
  python deploy_ios.py --app-path ~/Projects/MyApp --output-dir ~/Automation
  python deploy_ios.py --app-path ~/Projects/MyApp --app-name "CoolApp"
  python deploy_ios.py --app-path ~/Projects/MyApp --skip-build --skip-venv
        """
    )

    parser.add_argument(
        '--app-path',
        required=True,
        help='Path to iOS Xcode project directory'
    )
    parser.add_argument(
        '--output-dir',
        help='Directory where automation project will be created (default: same as app parent)'
    )
    parser.add_argument(
        '--app-name',
        help='Override auto-detected app name'
    )
    parser.add_argument(
        '--skip-build',
        action='store_true',
        help='Skip building the app (use existing .app)'
    )
    parser.add_argument(
        '--skip-venv',
        action='store_true',
        help='Skip creating virtual environment'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    deployer = iOSDeployment(verbose=args.verbose)
    success = deployer.deploy(
        app_path=args.app_path,
        output_dir=args.output_dir,
        app_name=args.app_name,
        skip_build=args.skip_build,
        skip_venv=args.skip_venv
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
