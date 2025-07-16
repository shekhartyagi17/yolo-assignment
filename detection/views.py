from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import os
import json
from .models import UploadedImage, DetectionResult
from .services import YOLOInferenceService
from .forms import ImageUploadForm


def index(request):
    """Main page with upload form"""
    print(f"Index view called - Method: {request.method}")
    
    if request.method == 'POST':
        print("POST request received")
        print(f"FILES: {request.FILES}")
        print(f"POST: {request.POST}")
        
        form = ImageUploadForm(request.POST, request.FILES)
        print(f"Form is valid: {form.is_valid()}")
        if form.is_valid():
            uploaded_image = form.save()
            print(f"Image saved with ID: {uploaded_image.id}")
            return redirect('detection:detection_result', image_id=uploaded_image.id)
        else:
            print(f"Form errors: {form.errors}")
            print(f"Form non-field errors: {form.non_field_errors()}")
    else:
        print("GET request received")
        form = ImageUploadForm()
    
    return render(request, 'detection/index.html', {'form': form})


def detection_result(request, image_id):
    """Display detection results"""
    try:
        uploaded_image = UploadedImage.objects.get(id=image_id)
        detection_result = DetectionResult.objects.filter(uploaded_image=uploaded_image).first()
        
        if not detection_result:
            # Run detection if not already done
            detection_result = run_detection(uploaded_image)
        
        context = {
            'uploaded_image': uploaded_image,
            'detection_result': detection_result,
        }
        return render(request, 'detection/result.html', context)
    
    except UploadedImage.DoesNotExist:
        return render(request, 'detection/error.html', {'error': 'Image not found'})


@csrf_exempt
@require_http_methods(["POST"])
def api_detect(request):
    """API endpoint for running detection"""
    try:
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image provided'}, status=400)
        
        # Save uploaded image
        uploaded_image = UploadedImage.objects.create(
            image=request.FILES['image']
        )
        
        # Run detection
        detection_result = run_detection(uploaded_image)
        
        # Return results
        response_data = {
            'success': True,
            'image_id': uploaded_image.id,
            'pytorch_detections': detection_result.pytorch_detections,
            'onnx_detections': detection_result.onnx_detections,
            'pytorch_result_url': detection_result.pytorch_result_image.url if detection_result.pytorch_result_image else None,
            'onnx_result_url': detection_result.onnx_result_image.url if detection_result.onnx_result_image else None,
        }
        
        return JsonResponse(response_data)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def run_detection(uploaded_image):
    """Run detection on uploaded image"""
    service = YOLOInferenceService()
    
    # Get image path
    image_path = uploaded_image.image.path
    
    # Create results directory
    results_dir = os.path.join(settings.MEDIA_ROOT, 'results')
    pytorch_dir = os.path.join(results_dir, 'pytorch')
    onnx_dir = os.path.join(results_dir, 'onnx')
    
    os.makedirs(pytorch_dir, exist_ok=True)
    os.makedirs(onnx_dir, exist_ok=True)
    
    # Generate output filenames
    base_filename = os.path.splitext(uploaded_image.get_filename())[0]
    pytorch_output = os.path.join(pytorch_dir, f"{base_filename}_pytorch_result.jpg")
    onnx_output = os.path.join(onnx_dir, f"{base_filename}_onnx_result.jpg")
    
    # Run PyTorch inference
    pytorch_detections, pytorch_results = service.run_pytorch_inference(image_path)
    
    # Draw PyTorch results
    if pytorch_detections:
        service.draw_detections(image_path, pytorch_detections, pytorch_output)
        pytorch_result_image = f"results/pytorch/{base_filename}_pytorch_result.jpg"
    else:
        pytorch_result_image = None
    
    # Run ONNX inference
    try:
        onnx_detections = service.run_onnx_inference(image_path)
        
        # Draw ONNX results
        if onnx_detections:
            service.draw_detections(image_path, onnx_detections, onnx_output)
            onnx_result_image = f"results/onnx/{base_filename}_onnx_result.jpg"
        else:
            onnx_result_image = None
    except Exception as e:
        print(f"ONNX inference failed: {e}")
        onnx_detections = []
        onnx_result_image = None
    
    # Save results to database
    detection_result = DetectionResult.objects.create(
        uploaded_image=uploaded_image,
        pytorch_result_image=pytorch_result_image,
        onnx_result_image=onnx_result_image,
        pytorch_detections=pytorch_detections,
        onnx_detections=onnx_detections
    )
    
    return detection_result


def convert_model(request):
    """Convert PyTorch model to ONNX"""
    try:
        service = YOLOInferenceService()
        onnx_path = service.convert_to_onnx()
        return JsonResponse({
            'success': True,
            'message': f'Model converted successfully to {onnx_path}'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500) 