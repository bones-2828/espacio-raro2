from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),

    # Sitio general
    path('', views.homepage, name="homepage"),
    path('quickorder/', views.order, name="quickorder"),

    # Autenticación
    path('login/', views.login_view, name="login_view"), 
    path('register/', views.register, name="register"), 
    path('logout/', views.logout_view, name='logout'),

    # Paneles
    path('dashboard/', views.dashboard, name="dashboard"),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),

    # CRUD Clientes
    path('clientes/', views.clientes_list, name='clientes_list'),
    path('clientes/nuevo/', views.clientes_create, name='clientes_create'),
    path('clientes/<int:pk>/', views.clientes_detail, name='clientes_detail'),
    path('clientes/<int:pk>/editar/', views.clientes_update, name='clientes_update'),
    path('clientes/<int:pk>/eliminar/', views.clientes_delete, name='clientes_delete'),
]
