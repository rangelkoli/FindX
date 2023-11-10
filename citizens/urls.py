from django.urls import path,include
from citizens import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.home, name='home'),
    path('scan',views.scan, name='scan'),
    path('uploaded',views.uploaded,name='uploaded'),
    path('scanimage',views.scanimage,name='scanimage'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)