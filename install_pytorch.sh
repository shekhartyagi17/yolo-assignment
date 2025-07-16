#!/bin/bash

echo "Installing PyTorch and dependencies for YOLO Detection App"
echo "=========================================================="

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: You're not in a virtual environment"
    echo "   It's recommended to create and activate a virtual environment first"
    echo "   python -m venv venv"
    echo "   source venv/bin/activate  # On macOS/Linux"
    echo ""
fi

echo "Step 1: Installing PyTorch from official source..."
echo "This may take a few minutes..."

# Install PyTorch for macOS (CPU version)
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu

if [ $? -eq 0 ]; then
    echo "✅ PyTorch installed successfully!"
else
    echo "❌ PyTorch installation failed"
    echo "Trying alternative installation method..."
    pip3 install torch torchvision
fi

echo ""
echo "Step 2: Installing other requirements..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All dependencies installed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Run: python setup.py"
    echo "2. Run: python manage.py runserver"
    echo "3. Open http://localhost:8000 in your browser"
else
    echo "❌ Some dependencies failed to install"
    echo "Please check the error messages above"
fi 