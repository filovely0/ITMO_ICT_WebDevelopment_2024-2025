from django.contrib import admin
from django.urls import path

from project_first_app import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
    path('owners/', views.owner_list, name='owner_list'),
    path('cars/', views.CarListView.as_view(), name='car_list'),  # для вывода всех автомобилей
    path('car/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),  # для вывода автомобиля по ID
    path('car/<int:pk>/update/', views.CarUpdateView.as_view(), name='car_update'),  # для обновления автомобиля
    path('owners/create/', views.owner_create, name='owner_create'),
    path('cars/create/', views.CarCreateView.as_view(), name='car_create'),  # Форма для создания автомобиля
    path('cars/delete/<int:car_id>/', views.CarDeleteView.as_view(), name='car_delete'),  # Удаление автомобиля

]
