"""
URL configuration for dreamin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from main import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path("home/", views.home_view, name="home"),
    path("create-dream/", views.create_dream_view, name="create_dream"),
    path("dreamjournal/", views.dreamjournal_view, name="dreamjournal"),
    path("dreamplayback/", views.dreamplayback_view, name="dreamplayback"),
    path("dreamjournal/<int:dream_id>/reflection/", views.create_reflection, name="create_reflection"),
    path("dreamjournal/<int:dream_id>/", views.dream_detail, name="dream_detail"),
    path('dream-playback/<int:dream_id>/', views.dreamplayback_view, name='dream_playback'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
