#!/usr/bin/env python3
"""
Installation script for YOLO Detection Django App
Handles PyTorch installation from official source
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

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    
    # Check if Python version is too new for PyTorch
    if version.major == 3 and version.minor >= 13:
        print("⚠️  Warning: Python 3.13+ detected")
        print("   PyTorch may not have pre-built wheels for this version")
        print("   Consider using Python 3.11 or 3.12 for better compatibility")
        print("   Or try installing from source (slower but more compatible)")
    
    print("✅ Python version is compatible")
    return True

def install_pytorch():
    """Install PyTorch from official source"""
    print("\nInstalling PyTorch from official source...")
    
    # Try different installation methods for Python 3.13+
    version = sys.version_info
    if version.major == 3 and version.minor >= 13:
        print("Using alternative installation methods for Python 3.13+")
        pytorch_commands = [
            "pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu --no-cache-dir",
            "pip3 install torch torchvision --no-cache-dir",
            "pip3 install torch torchvision --pre --index-url https://download.pytorch.org/whl/nightly/cpu",
        ]
    else:
        pytorch_commands = [
            "pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu",
            "pip3 install torch torchvision",  # Fallback
        ]
    
    for i, command in enumerate(pytorch_commands, 1):
        print(f"Trying method {i}/{len(pytorch_commands)}...")
        if run_command(command, f"Installing PyTorch (method {i})"):
            return True
    
    return False

def install_alternative_pytorch():
    """Try alternative PyTorch installation methods"""
    print("\nTrying alternative PyTorch installation methods...")
    
    alternative_commands = [
        "pip3 install torch torchvision --find-links https://download.pytorch.org/whl/torch_stable.html",
        "pip3 install torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu",
        "pip3 install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cpu",
    ]
    
    for i, command in enumerate(alternative_commands, 1):
        print(f"Trying alternative method {i}/{len(alternative_commands)}...")
        if run_command(command, f"Alternative PyTorch installation (method {i})"):
            return True
    
    return False

def install_other_requirements():
    """Install other requirements"""
    return run_command("pip3 install -r requirements.txt", "Installing other requirements")

def suggest_alternatives():
    """Suggest alternative solutions"""
    print("\n" + "=" * 60)
    print("🔧 Alternative Solutions for Python 3.13+")
    print("=" * 60)
    print("Since PyTorch doesn't have pre-built wheels for Python 3.13 yet,")
    print("here are some alternatives:")
    print()
    print("Option 1: Use a different Python version")
    print("  - Install Python 3.11 or 3.12")
    print("  - Create a new virtual environment")
    print("  - Re-run this installation script")
    print()
    print("Option 2: Use conda (if available)")
    print("  conda install pytorch torchvision -c pytorch")
    print()
    print("Option 3: Build from source (advanced)")
    print("  git clone https://github.com/pytorch/pytorch")
    print("  cd pytorch && python setup.py install")
    print()
    print("Option 4: Use a Docker container with Python 3.11")
    print("  docker run -it python:3.11-slim bash")
    print()
    print("Option 5: Try the nightly build")
    print("  pip3 install --pre torch torchvision --index-url https://download.pytorch.org/whl/nightly/cpu")

def main():
    """Main installation function"""
    print("=" * 60)
    print("YOLO Detection Django App - Dependency Installation")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install PyTorch
    if not install_pytorch():
        print("\n❌ Standard PyTorch installation failed")
        
        # Try alternative methods
        if not install_alternative_pytorch():
            print("\n❌ All PyTorch installation methods failed")
            suggest_alternatives()
            sys.exit(1)
    
    # Install other requirements
    if not install_other_requirements():
        print("\n❌ Other dependencies installation failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ All dependencies installed successfully!")
    print("\nNext steps:")
    print("1. Run: python setup.py")
    print("2. Run: python manage.py runserver")
    print("3. Open http://localhost:8000 in your browser")
    print("=" * 60)

if __name__ == "__main__":
    main() 