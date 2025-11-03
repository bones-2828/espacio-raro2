from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name="homepage"),
    path('quickorder/', views.order, name="quickorder"),
    path('login/', views.login_view, name="login_view"), 
    path('register/', views.register, name="register"), 
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.logout_view, name='logout'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('order/', views.order, name='order'),
    # CRUD Clientes
    path('clientes/crear/', views.clientes_create, name='clientes_create'),
    path('clientes/', views.clientes_list, name='clientes_list'),
    path('clientes/editar/', views.clientes_edit_select, name='clientes_edit_select'),
    path('clientes/eliminar/', views.clientes_delete_select, name='clientes_delete_select'),

    # CRUD Productos
    path('productos/crear/', views.productos_create, name='productos_create'),
    path('productos/', views.productos_list, name='productos_list'),
    path('productos/editar/', views.productos_edit_select, name='productos_edit_select'),
    path('productos/eliminar/', views.productos_delete_select, name='productos_delete_select'),

    # CRUD Pedidos
    path('pedidos/crear/', views.pedidos_create, name='pedidos_create'),
    path('pedidos/', views.pedidos_list, name='pedidos_list'),
    path('pedidos/editar/', views.pedidos_edit_select, name='pedidos_edit_select'),
    path('pedidos/eliminar/', views.pedidos_delete_select, name='pedidos_delete_select'),

]
