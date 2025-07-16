from django.contrib import admin
from .models import UploadedImage, DetectionResult


@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_filename', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['image']
    readonly_fields = ['uploaded_at']
    
    def get_filename(self, obj):
        return obj.get_filename()
    get_filename.short_description = 'Filename'


@admin.register(DetectionResult)
class DetectionResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'uploaded_image', 'pytorch_detections_count', 'onnx_detections_count', 'created_at']
    list_filter = ['created_at']
    readonly_fields = ['created_at']
    
    def pytorch_detections_count(self, obj):
        return len(obj.pytorch_detections)
    pytorch_detections_count.short_description = 'PyTorch Detections'
    
    def onnx_detections_count(self, obj):
        return len(obj.onnx_detections)
    onnx_detections_count.short_description = 'ONNX Detections' 