"""
URL configuration for voiceproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from voiceapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('call/', views.upload_audio, name='upload_audio'),
    # path('download/<int:audio_record_id>/', views.download_recording, name='download_recording')
]
    # path('render-phone-call-form/', views.render_phone_call_form, name='render_phone_call_form'),
    # path('initiate-call/', views.initiate_call, name='initiate_call'),  # Use a unique name for the URL pattern
