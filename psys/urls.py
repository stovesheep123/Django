from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='psys/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('search/', views.customer_search, name='customer_search'),
    path('list/', views.customer_list, name='customer_list'),
    path('create/', views.customer_create, name='customer_create'),
    path('update/<str:pk>/', views.customer_update, name='customer_update'),
    path('delete/<str:pk>/', views.customer_delete, name='customer_delete'),
]