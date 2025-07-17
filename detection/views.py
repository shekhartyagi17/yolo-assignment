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
    print(f"Request path: {request.path}")
    print(f"Request URL: {request.build_absolute_uri()}")
    
    if request.method == 'POST':
        print("POST request received")
        print(f"FILES: {list(request.FILES.keys())}")
        print(f"POST keys: {list(request.POST.keys())}")
        print(f"Content type: {request.content_type}")
        
        # Check if image file is present
        if 'image' in request.FILES:
            file = request.FILES['image']
            print(f"File received: {file.name}, size: {file.size}, content_type: {file.content_type}")
        else:
            print("No 'image' file found in request.FILES")
        
        form = ImageUploadForm(request.POST, request.FILES)
        print(f"Form is valid: {form.is_valid()}")
        
        if form.is_valid():
            print("Form is valid, saving...")
            uploaded_image = form.save()
            print(f"Image saved with ID: {uploaded_image.id}, path: {uploaded_image.image.path}")
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
    print(f"Starting detection for image: {uploaded_image.id}")
    
    try:
        service = YOLOInferenceService()
        
        # Get image path
        image_path = uploaded_image.image.path
        print(f"Processing image at path: {image_path}")
        
        # Check if image file exists
        if not os.path.exists(image_path):
            print(f"ERROR: Image file not found at {image_path}")
            raise FileNotFoundError(f"Image file not found at {image_path}")
        
        # Create results directory
        results_dir = os.path.join(settings.MEDIA_ROOT, 'results')
        pytorch_dir = os.path.join(results_dir, 'pytorch')
        onnx_dir = os.path.join(results_dir, 'onnx')
        
        os.makedirs(pytorch_dir, exist_ok=True)
        os.makedirs(onnx_dir, exist_ok=True)
        print(f"Created directories: {pytorch_dir}, {onnx_dir}")
        
        # Generate output filenames
        base_filename = os.path.splitext(uploaded_image.get_filename())[0]
        pytorch_output = os.path.join(pytorch_dir, f"{base_filename}_pytorch_result.jpg")
        onnx_output = os.path.join(onnx_dir, f"{base_filename}_onnx_result.jpg")
        
        print(f"Will save results to: {pytorch_output}, {onnx_output}")
        
        # Run PyTorch inference
        print("Running PyTorch inference...")
        pytorch_detections, pytorch_results = service.run_pytorch_inference(image_path)
        print(f"PyTorch detections: {len(pytorch_detections)} objects found")
        
        # Draw PyTorch results
        if pytorch_detections:
            service.draw_detections(image_path, pytorch_detections, pytorch_output)
            pytorch_result_image = f"results/pytorch/{base_filename}_pytorch_result.jpg"
            print(f"PyTorch result saved to: {pytorch_result_image}")
        else:
            pytorch_result_image = None
            print("No PyTorch detections to save")
        
        # Run ONNX inference
        onnx_detections = []
        onnx_result_image = None
        try:
            print("Running ONNX inference...")
            onnx_detections = service.run_onnx_inference(image_path)
            print(f"ONNX detections: {len(onnx_detections)} objects found")
            
            # Draw ONNX results
            if onnx_detections:
                service.draw_detections(image_path, onnx_detections, onnx_output)
                onnx_result_image = f"results/onnx/{base_filename}_onnx_result.jpg"
                print(f"ONNX result saved to: {onnx_result_image}")
            else:
                print("No ONNX detections to save")
        except Exception as e:
            print(f"ONNX inference failed: {e}")
            onnx_detections = []
            onnx_result_image = None
        
        # Save results to database
        print("Saving results to database...")
        detection_result = DetectionResult.objects.create(
            uploaded_image=uploaded_image,
            pytorch_detections=pytorch_detections,
            onnx_detections=onnx_detections
        )
        
        # Save result images if they exist
        if pytorch_result_image and os.path.exists(pytorch_output):
            # Save the relative path from MEDIA_ROOT
            detection_result.pytorch_result_image = pytorch_result_image
        
        if onnx_result_image and os.path.exists(onnx_output):
            # Save the relative path from MEDIA_ROOT  
            detection_result.onnx_result_image = onnx_result_image
        
        detection_result.save()
        print(f"Detection result saved with ID: {detection_result.id}")
        
        return detection_result
        
    except Exception as e:
        print(f"ERROR in run_detection: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise


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