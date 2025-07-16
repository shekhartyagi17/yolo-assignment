# YOLO Object Detection Web Application

A Django-based web application for running object detection using YOLO models with both PyTorch and ONNX inference engines.

## Features

- **Dual Model Inference**: Run object detection using both PyTorch and ONNX models
- **Automatic Model Conversion**: Convert PyTorch models to ONNX format automatically
- **Side-by-Side Comparison**: View results from both models simultaneously
- **Modern Web Interface**: Beautiful, responsive UI with drag-and-drop upload
- **Real-time Processing**: See detection results with bounding boxes and confidence scores

## Project Structure

```
yolo_detection/
├── detection/                 # Main Django app
│   ├── models.py             # Database models
│   ├── views.py              # View handlers
│   ├── services.py           # YOLO inference services
│   ├── forms.py              # Form definitions
│   └── urls.py               # URL routing
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   └── detection/            # App-specific templates
├── static/                   # Static files (CSS, JS)
├── media/                    # Uploaded files and results
├── yolo_detection/           # Django project settings
└── manage.py                 # Django management script
```

## Requirements

- Python 3.8+
- Django 4.2+
- PyTorch
- ONNX Runtime
- OpenCV
- Ultralytics (YOLO)

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create necessary directories**:
   ```bash
   mkdir -p media/uploads media/results/pytorch media/results/onnx
   ```

5. **Place your YOLO model**:
   - Copy your `.pt` model file to the project root
   - Update `YOLO_MODEL_PATH` in `yolo_detection/settings.py` if needed

## Usage

1. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

2. **Open your browser** and go to `http://localhost:8000`

3. **Upload an image** using the web interface

4. **View results** - the application will:
   - Run PyTorch inference
   - Convert the model to ONNX (if not already done)
   - Run ONNX inference
   - Display both results side by side

## API Endpoints

- `GET /` - Main upload page
- `POST /` - Upload image and run detection
- `GET /result/<image_id>/` - View detection results
- `POST /api/detect/` - API endpoint for detection
- `POST /api/convert-model/` - Convert PyTorch model to ONNX

## Configuration

### Model Paths
Update these in `yolo_detection/settings.py`:
```python
YOLO_MODEL_PATH = BASE_DIR / 'yolo11n.pt'
ONNX_MODEL_PATH = BASE_DIR / 'yolo11n.onnx'
```

### File Upload Settings
- Maximum file size: 10MB
- Supported formats: JPEG, PNG, GIF
- Files are stored in `media/uploads/`

## Components Breakdown

### Models (`detection/models.py`)
- `UploadedImage`: Stores uploaded images
- `DetectionResult`: Stores detection results and metadata

### Services (`detection/services.py`)
- `YOLOInferenceService`: Handles PyTorch and ONNX inference
- Model loading and caching
- Automatic ONNX conversion
- Bounding box visualization

### Views (`detection/views.py`)
- `index()`: Main upload page
- `detection_result()`: Display results
- `api_detect()`: API endpoint
- `convert_model()`: Model conversion endpoint

### Templates
- `base.html`: Base template with Bootstrap styling
- `index.html`: Upload interface with drag-and-drop
- `result.html`: Side-by-side results display
- `error.html`: Error handling

## Customization

### Adding New Models
1. Update `YOLOInferenceService` in `services.py`
2. Add model loading logic
3. Update templates to display new results

### Changing Detection Parameters
Modify confidence thresholds and other parameters in `services.py`:
```python
confidence_threshold = 0.25  # Adjust as needed
```

### Styling
- CSS is included in `base.html`
- Uses Bootstrap 5 for responsive design
- Custom styles for upload area and results

## Troubleshooting

### Common Issues

1. **Model not found**:
   - Ensure your `.pt` file is in the project root
   - Check the path in `settings.py`

2. **ONNX conversion fails**:
   - Ensure you have the latest ultralytics version
   - Check model compatibility

3. **No detections found**:
   - Try adjusting confidence thresholds
   - Check if the image contains detectable objects

4. **Memory issues**:
   - Reduce image size before upload
   - Use smaller model variants

### Performance Tips

- Use GPU acceleration if available
- Consider model quantization for faster inference
- Implement result caching for repeated images
- Use background tasks for long-running detections

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations detection
python manage.py migrate
```

### Static Files
```bash
python manage.py collectstatic
```

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
- Check the troubleshooting section
- Review the Django and YOLO documentation
- Open an issue on the project repository 