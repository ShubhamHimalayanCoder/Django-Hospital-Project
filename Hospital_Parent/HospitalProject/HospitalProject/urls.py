"""
URL configuration for HospitalProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from . import views
# For photo uploading and storing
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home-page'),
    path('about_us/',views.about_us,name='about_us'),
    path('careers/',views.career,name='career'),
    path('faq/',views.faq,name='faq'),
    path('appointment/',views.appointment,name='appointment'),
    path('contact/',views.contact,name='contact_us'),
    path('patient/', include('Patient.urls')),
    path('t&c/',views.terms_and_conditions,name='t&c'),
    path('admin/', admin.site.urls),
]

# For photo uploading and storing
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

