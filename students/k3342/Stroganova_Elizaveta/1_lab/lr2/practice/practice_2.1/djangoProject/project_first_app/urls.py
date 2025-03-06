from django.contrib import admin
from django.urls import path

from project_first_app import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
]
