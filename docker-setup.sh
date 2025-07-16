#!/bin/bash

echo "🐳 YOLO Detection Django App - Docker Setup"
echo "============================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed"
    echo "Please install Docker Compose first: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Check if YOLO model file exists
if [ ! -f "yolo11n.pt" ]; then
    echo "⚠️  Warning: yolo11n.pt not found in current directory"
    echo "   Please ensure your YOLO model file is in the project root"
    echo "   The application will still work but model conversion may fail"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p media/uploads media/results/pytorch media/results/onnx

# Build and run the Docker container
echo "🔨 Building Docker image..."
docker-compose build

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully"
    
    echo "🚀 Starting the application..."
    echo "   The app will be available at: http://localhost:8000"
    echo "   Press Ctrl+C to stop the application"
    echo ""
    
    # Run the container
    docker-compose up
else
    echo "❌ Docker build failed"
    echo "Please check the error messages above"
    exit 1
fi 