#!/usr/bin/env python3
"""
Multi-Platform Deployment Orchestrator.

This script orchestrates deployment for both iOS and Android platforms,
creating a unified automation project that supports both.

Usage:
    python deploy_both.py \
        --ios-path ~/Projects/MyApp-iOS \
        --android-path ~/Projects/MyApp-Android
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from deploy.common import DeploymentUtilities
from deploy.deploy_ios import iOSDeployment
from deploy.deploy_android import AndroidDeployment


class MultiPlatformDeployment:
    """Orchestrates multi-platform deployment."""

    def __init__(self, verbose: bool = False):
        """
        Initialize multi-platform deployment.

        Args:
            verbose: Enable verbose output
        """
        self.utils = DeploymentUtilities(verbose=verbose)
        self.verbose = verbose

    def deploy(
        self,
        ios_path: str = None,
        android_path: str = None,
        output_dir: str = None,
        app_name: str = None,
        skip_build: bool = False,
        skip_venv: bool = False
    ) -> bool:
        """
        Deploy automation for both platforms.

        Args:
            ios_path: Path to iOS project
            android_path: Path to Android project
            output_dir: Output directory for automation project
            app_name: App name (must be same for both)
            skip_build: Skip building apps
            skip_venv: Skip virtual environment setup

        Returns:
            True if deployment successful
        """
        self.utils.print_header("Multi-Platform Deployment")

        if not ios_path and not android_path:
            self.utils.print_error("At least one platform path must be provided")
            return False

        success = True

        # Deploy iOS first (if provided)
        if ios_path:
            self.utils.print_info("Deploying iOS automation...")
            ios_deployer = iOSDeployment(verbose=self.verbose)

            ios_success = ios_deployer.deploy(
                app_path=ios_path,
                output_dir=output_dir,
                app_name=app_name,
                skip_build=skip_build,
                skip_venv=skip_venv
            )

            if not ios_success:
                self.utils.print_warning("iOS deployment failed")
                success = False

        # Deploy Android (if provided and implemented)
        if android_path:
            self.utils.print_info("Deploying Android automation...")
            android_deployer = AndroidDeployment(verbose=self.verbose)

            android_success = android_deployer.deploy(
                app_path=android_path,
                output_dir=output_dir,
                app_name=app_name,
                skip_build=skip_build,
                skip_venv=skip_venv
            )

            if not android_success:
                self.utils.print_warning("Android deployment not yet available")
                # Don't fail overall if only Android is missing (not implemented yet)

        return success


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Deploy automation for both iOS and Android',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Both platforms
  python deploy_both.py \
      --ios-path ~/Projects/MyApp-iOS \
      --android-path ~/Projects/MyApp-Android

  # iOS only (same as deploy_ios.py)
  python deploy_both.py --ios-path ~/Projects/MyApp

  # Custom output directory
  python deploy_both.py \
      --ios-path ~/Projects/MyApp-iOS \
      --output-dir ~/Automation
        """
    )

    parser.add_argument(
        '--ios-path',
        help='Path to iOS Xcode project'
    )
    parser.add_argument(
        '--android-path',
        help='Path to Android project'
    )
    parser.add_argument(
        '--output-dir',
        help='Directory where automation project will be created'
    )
    parser.add_argument(
        '--app-name',
        help='App name (must be same for both platforms)'
    )
    parser.add_argument(
        '--skip-build',
        action='store_true',
        help='Skip building apps'
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

    if not args.ios_path and not args.android_path:
        parser.error("At least one of --ios-path or --android-path is required")

    deployer = MultiPlatformDeployment(verbose=args.verbose)
    success = deployer.deploy(
        ios_path=args.ios_path,
        android_path=args.android_path,
        output_dir=args.output_dir,
        app_name=args.app_name,
        skip_build=args.skip_build,
        skip_venv=args.skip_venv
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
