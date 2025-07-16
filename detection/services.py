import cv2
import numpy as np
import torch
import onnxruntime as ort
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings
import json
from pathlib import Path


class YOLOInferenceService:
    """Service for running YOLO inference with PyTorch and ONNX"""
    
    def __init__(self):
        self.pytorch_model = None
        self.onnx_model = None
        self.onnx_session = None
        self.model_path = settings.YOLO_MODEL_PATH
        self.onnx_path = settings.ONNX_MODEL_PATH
        
    def load_pytorch_model(self):
        """Load PyTorch YOLO model"""
        if self.pytorch_model is None:
            self.pytorch_model = YOLO(self.model_path)
        return self.pytorch_model
    
    def convert_to_onnx(self):
        """Convert PyTorch model to ONNX format"""
        if not os.path.exists(self.onnx_path):
            model = self.load_pytorch_model()
            # Export to ONNX
            model.export(format='onnx', dynamic=True, simplify=True)
            print(f"Model converted to ONNX and saved at {self.onnx_path}")
        return self.onnx_path
    
    def load_onnx_model(self):
        """Load ONNX model"""
        if self.onnx_session is None:
            if not os.path.exists(self.onnx_path):
                self.convert_to_onnx()
            
            # Create ONNX Runtime session
            providers = ['CPUExecutionProvider']
            if 'CUDAExecutionProvider' in ort.get_available_providers():
                providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
            
            self.onnx_session = ort.InferenceSession(self.onnx_path, providers=providers)
        return self.onnx_session
    
    def run_pytorch_inference(self, image_path):
        """Run inference using PyTorch model"""
        model = self.load_pytorch_model()
        results = model(image_path)
        
        # Extract detection results
        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    detection = {
                        'bbox': box.xyxy[0].cpu().numpy().tolist(),  # [x1, y1, x2, y2]
                        'confidence': float(box.conf[0]),
                        'class_id': int(box.cls[0]),
                        'class_name': model.names[int(box.cls[0])]
                    }
                    detections.append(detection)
        
        return detections, results
    
    def run_onnx_inference(self, image_path):
        """Run inference using ONNX model"""
        session = self.load_onnx_model()
        
        # Load and preprocess image
        image = cv2.imread(image_path)
        original_height, original_width = image.shape[:2]
        
        # Resize to model input size (640x640 for YOLOv8)
        input_size = (640, 640)
        resized_image = cv2.resize(image, input_size)
        
        # Normalize and transpose
        input_data = resized_image.astype(np.float32) / 255.0
        input_data = np.transpose(input_data, (2, 0, 1))  # HWC to CHW
        input_data = np.expand_dims(input_data, axis=0)  # Add batch dimension
        
        # Run inference
        input_name = session.get_inputs()[0].name
        outputs = session.run(None, {input_name: input_data})
        
        # Process outputs (this is a simplified version - you might need to adjust based on your model)
        detections = self._process_onnx_outputs(outputs[0], original_width, original_height)
        
        return detections
    
    def _process_onnx_outputs(self, outputs, original_width, original_height):
        """Process ONNX model outputs to extract detections"""
        detections = []
        
        # This is a simplified processing - you'll need to adjust based on your specific model output format
        # For YOLOv8, the output is typically [batch, num_detections, 85] where 85 = 4 (bbox) + 1 (conf) + 80 (classes)
        
        if len(outputs.shape) == 3:
            # Remove batch dimension
            outputs = outputs[0]
        
        # Filter by confidence threshold
        confidence_threshold = 0.25
        for detection in outputs:
            confidence = detection[4]  # Assuming confidence is at index 4
            if confidence > confidence_threshold:
                # Get class with highest probability
                class_scores = detection[5:]
                class_id = np.argmax(class_scores)
                class_confidence = class_scores[class_id]
                
                if class_confidence > confidence_threshold:
                    # Extract bounding box (normalized coordinates)
                    x1, y1, x2, y2 = detection[:4]
                    
                    # Convert to pixel coordinates
                    x1 = int(x1 * original_width)
                    y1 = int(y1 * original_height)
                    x2 = int(x2 * original_width)
                    y2 = int(y2 * original_height)
                    
                    detection_data = {
                        'bbox': [x1, y1, x2, y2],
                        'confidence': float(confidence),
                        'class_id': int(class_id),
                        'class_name': f'class_{class_id}'  # You might want to load class names
                    }
                    detections.append(detection_data)
        
        return detections
    
    def draw_detections(self, image_path, detections, output_path):
        """Draw bounding boxes on image"""
        image = cv2.imread(image_path)
        
        for detection in detections:
            bbox = detection['bbox']
            confidence = detection['confidence']
            class_name = detection['class_name']
            
            # Draw bounding box
            cv2.rectangle(image, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0), 2)
            
            # Draw label
            label = f"{class_name}: {confidence:.2f}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            cv2.rectangle(image, (int(bbox[0]), int(bbox[1] - label_size[1] - 10)), 
                         (int(bbox[0]) + label_size[0], int(bbox[1])), (0, 255, 0), -1)
            cv2.putText(image, label, (int(bbox[0]), int(bbox[1] - 5)), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        cv2.imwrite(output_path, image)
        return output_path 