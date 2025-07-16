#!/usr/bin/env python3
"""
Alternative installation script that installs everything except PyTorch
Useful when PyTorch installation fails due to Python version compatibility
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"  Error: {e.stderr}")
        return False

def install_django_and_others():
    """Install Django and other dependencies (excluding PyTorch)"""
    print("Installing Django and other dependencies...")
    
    # Install packages one by one to avoid PyTorch dependency issues
    packages = [
        "Django==4.2.7",
        "opencv-python>=4.8.0",
        "onnx>=1.14.0", 
        "onnxruntime>=1.15.0",
        "Pillow>=9.5.0",
        "numpy>=1.21.0",
        "matplotlib>=3.6.0",
        "python-dotenv>=1.0.0"
    ]
    
    for package in packages:
        if not run_command(f"pip3 install {package}", f"Installing {package}"):
            print(f"⚠️  Failed to install {package}, continuing...")
    
    # Try to install ultralytics (may fail without PyTorch)
    print("\nTrying to install ultralytics...")
    if not run_command("pip3 install ultralytics>=8.0.0", "Installing ultralytics"):
        print("⚠️  ultralytics installation failed (requires PyTorch)")
        print("   This is expected - you'll need to install PyTorch separately")
    
    return True

def main():
    """Main installation function"""
    print("=" * 60)
    print("YOLO Detection Django App - Alternative Installation")
    print("=" * 60)
    print("This script installs everything except PyTorch")
    print("Use this if PyTorch installation fails due to Python version")
    print()
    
    # Install Django and other dependencies
    if not install_django_and_others():
        print("\n❌ Installation failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ Django and other dependencies installed!")
    print()
    print("⚠️  PyTorch still needs to be installed separately")
    print("   Try one of these options:")
    print()
    print("Option 1: Use a different Python version (recommended)")
    print("   - Install Python 3.11 or 3.12")
    print("   - Create new virtual environment")
    print("   - Run: python install_dependencies.py")
    print()
    print("Option 2: Try PyTorch installation manually")
    print("   pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu")
    print()
    print("Option 3: Use conda")
    print("   conda install pytorch torchvision -c pytorch")
    print()
    print("Option 4: Continue without PyTorch (limited functionality)")
    print("   - The app will work but ONNX conversion may fail")
    print("   - You can still test the Django setup")
    print()
    print("Next steps (if PyTorch is installed):")
    print("1. Run: python setup.py")
    print("2. Run: python manage.py runserver")
    print("3. Open http://localhost:8000 in your browser")
    print("=" * 60)

if __name__ == "__main__":
    main() 