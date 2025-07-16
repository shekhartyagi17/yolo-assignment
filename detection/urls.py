from django.urls import path
from . import views

app_name = 'detection'

urlpatterns = [
    path('', views.index, name='index'),
    path('result/<int:image_id>/', views.detection_result, name='detection_result'),
    path('api/detect/', views.api_detect, name='api_detect'),
    path('api/convert-model/', views.convert_model, name='convert_model'),
] 