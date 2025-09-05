#!/usr/bin/env python3
# Copyright (c) 2024 Eric Hoy
# Licensed under the MIT License

import argparse
import os
import shutil
import subprocess
import sys
import textwrap

# --- Configuration ---
DEFAULT_PYTHON_VERSION = "3.11"
DEFAULT_PACKAGES = ["tabulate", "boto3"]
VALID_PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"]
DOCKER_IMAGE_TEMPLATE = "public.ecr.aws/lambda/python:{}"
BUILD_DIR = "build"

# --- Colors for output ---
class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_color(msg, color):
    """Prints a message in a given color."""
    print(f"{color}{msg}{Colors.ENDC}")

def run_command(command, capture_output=False, text=False, check=True):
    """Runs a command and handles errors."""
    print_color(f"\n▶️  Executing: {' '.join(command)}", Colors.OKCYAN)
    try:
        result = subprocess.run(
            command,
            capture_output=capture_output,
            text=text,
            check=check
        )
        if result.stderr:
            print_color(f"   Warning/Info from command:\n{textwrap.indent(result.stderr, '   ')}", Colors.WARNING)
        return result
    except FileNotFoundError:
        print_color(f"❌ Error: Command '{command[0]}' not found. Is it installed and in your PATH?", Colors.FAIL)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print_color(f"❌ Command failed with exit code {e.returncode}:", Colors.FAIL)
        error_output = e.stderr or e.stdout
        if error_output:
             print(textwrap.indent(error_output, '   '))
        sys.exit(1)

def check_docker():
    """Checks if Docker is installed and running."""
    print_color("Verifying Docker installation...", Colors.HEADER)
    run_command(["docker", "--version"])
    try:
        run_command(["docker", "info"], capture_output=True, text=True, check=True)
        print_color("✅ Docker is installed and the daemon is running.", Colors.OKGREEN)
    except subprocess.CalledProcessError:
        print_color("❌ Error: Docker daemon is not running.", Colors.FAIL)
        print("Please start the Docker daemon and try again.")
        sys.exit(1)


def main():
    """Main function to build the Lambda layer."""
    parser = argparse.ArgumentParser(
        description="Build an AWS Lambda layer .zip file using Docker.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-p", "--python-version",
        choices=VALID_PYTHON_VERSIONS,
        default=DEFAULT_PYTHON_VERSION,
        help=f"Python version for the Lambda layer. Defaults to {DEFAULT_PYTHON_VERSION}."
    )
    parser.add_argument(
        "-r", "--packages",
        nargs='+',
        default=DEFAULT_PACKAGES,
        help=f"Space-separated list of Python packages to install. Defaults to: {' '.join(DEFAULT_PACKAGES)}."
    )
    parser.add_argument(
        "-o", "--output-zip",
        default=None,
        help="Name of the output zip file. Defaults to 'lambda_layer_pyX.Y.zip'."
    )

    args = parser.parse_args()

    python_version = args.python_version
    packages_to_install = args.packages
    output_zip_file = args.output_zip or f"lambda_layer_py{python_version}.zip"
    docker_image = DOCKER_IMAGE_TEMPLATE.format(python_version)
    
    # Layer structure: packages need to be in python/
    install_path = os.path.join(BUILD_DIR, "python")


    print_color("--- Lambda Layer Builder ---", Colors.BOLD)
    print(f"   Python Version: {python_version}")
    print(f"   Packages: {', '.join(packages_to_install)}")
    print(f"   Output File: {output_zip_file}")
    print(f"   Docker Image: {docker_image}")
    print("----------------------------")

    check_docker()
    
    # Clean up previous build if it exists
    if os.path.exists(BUILD_DIR):
        print_color(f"Removing existing build directory: {BUILD_DIR}", Colors.WARNING)
        shutil.rmtree(BUILD_DIR)

    # Create build directory
    print_color(f"Creating build directory: {install_path}", Colors.OKBLUE)
    os.makedirs(install_path)

    try:
        # Pull the docker image
        print_color(f"Pulling Docker image: {docker_image}", Colors.HEADER)
        run_command(["docker", "pull", docker_image])
        
        # Install packages using docker
        print_color(f"Installing packages: {', '.join(packages_to_install)}", Colors.HEADER)
        
        # Arguments for the pip install command
        pip_install_args = [
            "install",
            *packages_to_install,
            "--target", "/var/task/python"
        ]
        
        # We override the default entrypoint of the Lambda image to run 'pip' directly.
        # This is necessary because the default entrypoint expects a function handler, not a shell command.
        docker_run_command = [
            "docker", "run", "--rm",
            "-v", f"{os.path.abspath(BUILD_DIR)}:/var/task",
            "--entrypoint", "pip",
            docker_image,
            *pip_install_args
        ]
        
        run_command(docker_run_command)
        
        # Create the zip file
        print_color(f"Creating zip file: {output_zip_file}", Colors.HEADER)
        
        # Check if output file already exists
        if os.path.exists(output_zip_file):
            print_color(f"Removing existing zip file: {output_zip_file}", Colors.WARNING)
            os.remove(output_zip_file)
            
        shutil.make_archive(
            output_zip_file.replace('.zip', ''), # shutil adds .zip extension
            'zip',           # format
            root_dir=BUILD_DIR  # directory to zip
        )

        print_color(f"\n✅ Success! Lambda layer created at: {os.path.abspath(output_zip_file)}", Colors.OKGREEN)

    finally:
        # Clean up build directory
        if os.path.exists(BUILD_DIR):
            print_color(f"Cleaning up build directory: {BUILD_DIR}", Colors.OKBLUE)
            shutil.rmtree(BUILD_DIR)

if __name__ == "__main__":
    main()
