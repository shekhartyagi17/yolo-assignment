from django.db import models
import os
from django.conf import settings


def upload_to(instance, filename):
    """Generate upload path for images"""
    return f'uploads/{filename}'


class UploadedImage(models.Model):
    """Model to store uploaded images"""
    image = models.ImageField(upload_to=upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image uploaded at {self.uploaded_at}"
    
    def get_filename(self):
        return os.path.basename(self.image.name)


class DetectionResult(models.Model):
    """Model to store detection results"""
    uploaded_image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE)
    pytorch_result_image = models.ImageField(upload_to='results/pytorch/', null=True, blank=True)
    onnx_result_image = models.ImageField(upload_to='results/onnx/', null=True, blank=True)
    pytorch_detections = models.JSONField(default=list)  # Store detection data
    onnx_detections = models.JSONField(default=list)     # Store detection data
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Detection result for {self.uploaded_image}" 