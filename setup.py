#!/usr/bin/env python
"""
Setup script for the YOLO Detection Django application
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"  Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"✗ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✓ Python {version.major}.{version.minor} is compatible")
    return True

def install_requirements():
    """Install required packages"""
    if not os.path.exists('requirements.txt'):
        print("✗ requirements.txt not found")
        return False
    
    return run_command("pip install -r requirements.txt", "Installing requirements")

def setup_django():
    """Setup Django database and migrations"""
    commands = [
        ("python manage.py makemigrations detection", "Creating database migrations"),
        ("python manage.py migrate", "Applying database migrations"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True

def create_directories():
    """Create necessary directories"""
    directories = [
        'media/uploads',
        'media/results/pytorch',
        'media/results/onnx',
        'static/css',
        'static/js',
    ]
    
    print("Creating directories...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {directory}")
    return True

def check_model_file():
    """Check if YOLO model file exists"""
    print("Checking model files...")
    
    model_files = ['yolo11n.pt']
    for model_file in model_files:
        if os.path.exists(model_file):
            print(f"✓ Found {model_file}")
        else:
            print(f"⚠ Warning: {model_file} not found")
            print(f"  Please place your YOLO model file in the project root")
    
    return True

def main():
    """Main setup function"""
    print("=" * 60)
    print("YOLO Detection Django App - Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("\n✗ Setup failed at requirements installation")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("\n✗ Setup failed at directory creation")
        sys.exit(1)
    
    # Check model files
    check_model_file()
    
    # Setup Django
    if not setup_django():
        print("\n✗ Setup failed at Django setup")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✓ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Ensure your YOLO model file is in the project root")
    print("2. Run: python manage.py runserver")
    print("3. Open http://localhost:8000 in your browser")
    print("4. Upload an image to test the detection")
    print("\nOptional:")
    print("- Run: python test_setup.py to verify the setup")
    print("- Create a superuser: python manage.py createsuperuser")
    print("=" * 60)

if __name__ == "__main__":
    main() 