"""
URL configuration for projekt project.

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
from . import views
from .views import kolegij_list
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('ja/', views.ja_view, name='ja'),
    path('kolegij/', views.kolegij_view, name='kolegij'),
    path('pocetna/', views.pocetna_view, name='pocetna'),
 path('kolegij/', views.kolegij_list, name='kolegij_list'),
    path('', views.login_view, name='login'),  # Empty path URL pattern
    path('create_kolegij/', views.create_kolegij, name='create_kolegij'),
    path('create_obavijest/', views.create_obavijest, name='create_obavijest'),
    path('create_profesor/', views.create_profesor, name='create_profesor'),
path('edit_obavijest/<int:obavijest_id>/', views.edit_obavijest_view, name='edit_obavijest'),
path('edit_profesor/<int:profesor_id>/', views.edit_profesor_view, name='edit_profesor'),
path('edit_kolegij/<int:kolegij_id>/', views.edit_kolegij_view, name='edit_kolegij'),

path('get_obavijest/<int:obavijest_id>/', views.get_obavijest_view, name='get_obavijest'),
path('get_profesor/<int:profesor_id>/', views.get_profesor_view, name='get_profesor'),
path('get_kolegij/<int:kolegij_id>/<int:profesor_id>/', views.get_kolegij_view, name='get_kolegij'),
path('logout/', LogoutView.as_view(), name='logout'),
  path('delete_obavijest/<int:obavijest_id>/', views.delete_obavijest, name='delete_obavijest'),
]
