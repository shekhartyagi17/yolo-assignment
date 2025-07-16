# Quick Start Guide - YOLO Object Detection Web App

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies
**Option A: Use the installation script (Recommended)**
```bash
python install_dependencies.py
```

**Option B: Manual installation**
```bash
# Install PyTorch first (from official source)
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Then install other requirements
pip3 install -r requirements.txt
```

### 2. Setup the Application
```bash
python setup.py
```

### 3. Start the Server
```bash
python manage.py runserver
```

### 4. Open Your Browser
Go to: http://localhost:8000

### 5. Upload an Image
- Drag and drop an image or click to browse
- The app will run both PyTorch and ONNX inference
- View results side-by-side with bounding boxes

## 📁 Project Structure

```
Assignment/
├── detection/                 # Main Django app
│   ├── models.py             # Database models
│   ├── views.py              # View handlers  
│   ├── services.py           # YOLO inference services
│   ├── forms.py              # Form definitions
│   ├── urls.py               # URL routing
│   └── admin.py              # Admin interface
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   └── detection/            # App templates
├── yolo_detection/           # Django project settings
├── media/                    # Uploaded files & results
├── static/                   # Static files
├── requirements.txt           # Python dependencies (excluding PyTorch)
├── install_dependencies.py   # Installation script
├── setup.py                  # Setup script
├── test_setup.py             # Test script
├── README.md                 # Full documentation
└── yolo11n.pt               # Your YOLO model
```

## 🔧 Key Components

### Models (`detection/models.py`)
- `UploadedImage`: Stores uploaded images
- `DetectionResult`: Stores detection results

### Services (`detection/services.py`)
- `YOLOInferenceService`: Handles PyTorch & ONNX inference
- Automatic model conversion
- Bounding box visualization

### Views (`detection/views.py`)
- Main upload page
- Results display
- API endpoints

## 🎯 Features

✅ **Dual Model Inference**: PyTorch + ONNX  
✅ **Automatic Conversion**: PyTorch → ONNX  
✅ **Side-by-Side Results**: Compare both models  
✅ **Modern UI**: Drag & drop upload  
✅ **Real-time Processing**: See results immediately  
✅ **Bounding Box Visualization**: Clear detection display  

## 🛠 API Endpoints

- `GET /` - Upload page
- `POST /` - Upload & detect
- `GET /result/<id>/` - View results
- `POST /api/detect/` - API endpoint
- `POST /api/convert-model/` - Convert model

## 🔍 Testing

Run the test script to verify setup:
```bash
python test_setup.py
```

## 📊 Example Usage

1. **Upload Image**: Use the web interface
2. **Processing**: App runs both models
3. **Results**: View side-by-side comparison
4. **Details**: See detection counts and confidence scores

## 🚨 Troubleshooting

### Common Issues:

1. **PyTorch installation fails**:
   ```bash
   # Try the official PyTorch source
   pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu
   ```

2. **Model not found**: Ensure `yolo11n.pt` is in project root

3. **Import errors**: Run `python install_dependencies.py`

4. **Database errors**: Run `python manage.py migrate`

5. **ONNX conversion fails**: Check ultralytics version

### Performance Tips:
- Use GPU if available (install CUDA version of PyTorch)
- Reduce image size for faster processing
- Consider model quantization

## 📝 Configuration

Update model paths in `yolo_detection/settings.py`:
```python
YOLO_MODEL_PATH = BASE_DIR / 'yolo11n.pt'
ONNX_MODEL_PATH = BASE_DIR / 'yolo11n.onnx'
```

## 🎨 Customization

- **Styling**: Modify `templates/base.html`
- **Detection Parameters**: Edit `services.py`
- **Model Paths**: Update `settings.py`
- **File Upload**: Configure in `forms.py`

## 📚 Next Steps

1. **Explore the code**: Check `detection/services.py` for inference logic
2. **Customize**: Modify templates and styling
3. **Extend**: Add new models or features
4. **Deploy**: Consider production deployment options

## 🆘 Support

- Check the full `README.md` for detailed documentation
- Review Django and YOLO documentation
- Test with different images and models

---

**Ready to detect objects! 🎯** 