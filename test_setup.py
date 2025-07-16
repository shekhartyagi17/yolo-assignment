#!/usr/bin/env python
"""
Test script to verify the Django YOLO detection setup
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yolo_detection.settings')
django.setup()

def test_django_setup():
    """Test Django setup"""
    print("Testing Django setup...")
    try:
        from django.conf import settings
        print(f"✓ Django settings loaded successfully")
        print(f"  - DEBUG: {settings.DEBUG}")
        print(f"  - YOLO_MODEL_PATH: {settings.YOLO_MODEL_PATH}")
        print(f"  - ONNX_MODEL_PATH: {settings.ONNX_MODEL_PATH}")
        return True
    except Exception as e:
        print(f"✗ Django setup failed: {e}")
        return False

def test_model_paths():
    """Test if model files exist"""
    print("\nTesting model paths...")
    from django.conf import settings
    
    pytorch_exists = settings.YOLO_MODEL_PATH.exists()
    print(f"  - PyTorch model: {'✓' if pytorch_exists else '✗'} {settings.YOLO_MODEL_PATH}")
    
    onnx_exists = settings.ONNX_MODEL_PATH.exists()
    print(f"  - ONNX model: {'✓' if onnx_exists else '✗'} {settings.ONNX_MODEL_PATH}")
    
    return pytorch_exists

def test_imports():
    """Test if required packages can be imported"""
    print("\nTesting package imports...")
    
    packages = [
        ('torch', 'PyTorch'),
        ('cv2', 'OpenCV'),
        ('onnxruntime', 'ONNX Runtime'),
        ('ultralytics', 'Ultralytics YOLO'),
        ('numpy', 'NumPy'),
        ('PIL', 'Pillow'),
    ]
    
    all_imported = True
    for package, name in packages:
        try:
            __import__(package)
            print(f"  ✓ {name} imported successfully")
        except ImportError as e:
            print(f"  ✗ {name} import failed: {e}")
            all_imported = False
    
    return all_imported

def test_service_loading():
    """Test if the YOLO service can be loaded"""
    print("\nTesting YOLO service...")
    try:
        from detection.services import YOLOInferenceService
        service = YOLOInferenceService()
        print("  ✓ YOLOInferenceService created successfully")
        
        # Test PyTorch model loading
        try:
            model = service.load_pytorch_model()
            print("  ✓ PyTorch model loaded successfully")
        except Exception as e:
            print(f"  ✗ PyTorch model loading failed: {e}")
            return False
        
        return True
    except Exception as e:
        print(f"  ✗ Service loading failed: {e}")
        return False

def test_database_models():
    """Test if database models can be created"""
    print("\nTesting database models...")
    try:
        from detection.models import UploadedImage, DetectionResult
        print("  ✓ Database models imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Database models failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("YOLO Detection Django App - Setup Test")
    print("=" * 50)
    
    tests = [
        test_django_setup,
        test_model_paths,
        test_imports,
        test_service_loading,
        test_database_models,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! The setup is ready.")
        print("\nNext steps:")
        print("1. Run: python manage.py makemigrations")
        print("2. Run: python manage.py migrate")
        print("3. Run: python manage.py runserver")
        print("4. Open http://localhost:8000 in your browser")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 