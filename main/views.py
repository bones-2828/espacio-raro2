from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Clientes, Producto, Pedidos


# ===========================
# VISTAS PRINCIPALES
# ===========================
def homepage(request):
    return render(request, "index.html")

def order(request):
    return render(request, "quickorder.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect("dashboard")
            else:
                return redirect("user_dashboard")
        else:
            messages.error(request, "Credenciales incorrectas.")
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

@login_required
def dashboard(request):
    return render(request, "dashboard.html")

@login_required
def user_dashboard(request):
    return render(request, "user_dashboard.html")

def logout_view(request):
    logout(request)
    return redirect("homepage")


# ===========================
# CRUD CLIENTES
# ===========================
@login_required
def clientes_list(request):
    clientes = Clientes.objects.all()
    return render(request, "clientes_list.html", {"clientes": clientes})

@login_required
def clientes_create(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        email = request.POST.get("email")
        telefono = request.POST.get("telefono")
        Clientes.objects.create(
            nombre=nombre, apellido=apellido, email=email, telefono=telefono
        )
        messages.success(request, "Cliente creado correctamente.")
        return redirect("clientes_list")
    return render(request, "clientes_create.html")

@login_required
def clientes_edit_select(request):
    clientes = Clientes.objects.all()
    return render(request, "clientes_edit_select.html", {"clientes": clientes})

@login_required
def clientes_delete_select(request):
    clientes = Clientes.objects.all()
    return render(request, "clientes_delete_select.html", {"clientes": clientes})


# ===========================
# CRUD PRODUCTOS
# ===========================
@login_required
def productos_list(request):
    productos = Producto.objects.all()
    return render(request, "productos_list.html", {"productos": productos})

@login_required
def productos_create(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        precio = request.POST.get("precio")
        stock = request.POST.get("stock")
        Producto.objects.create(nombre=nombre, precio=precio, stock=stock)
        messages.success(request, "Producto creado correctamente.")
        return redirect("productos_list")
    return render(request, "productos_create.html")

@login_required
def productos_edit_select(request):
    productos = Producto.objects.all()
    return render(request, "productos_edit_select.html", {"productos": productos})

@login_required
def productos_delete_select(request):
    productos = Producto.objects.all()
    return render(request, "productos_delete_select.html", {"productos": productos})


# ===========================
# CRUD PEDIDOS
# ===========================
@login_required
def pedidos_list(request):
    pedidos = Pedidos.objects.all()
    return render(request, "pedidos_list.html", {"pedidos": pedidos})

@login_required
def pedidos_create(request):
    if request.method == "POST":
        cliente_id = request.POST.get("cliente_id")
        producto_id = request.POST.get("producto_id")
        cantidad = request.POST.get("cantidad")
        Pedidos.objects.create(
            cliente_id=cliente_id, producto_id=producto_id, cantidad=cantidad
        )
        messages.success(request, "Pedido creado correctamente.")
        return redirect("pedidos_list")
    return render(request, "pedidos_create.html")

@login_required
def pedidos_edit_select(request):
    pedidos = Pedidos.objects.all()
    return render(request, "pedidos_edit_select.html", {"pedidos": pedidos})

@login_required
def pedidos_delete_select(request):
    pedidos = Pedidos.objects.all()
    return render(request, "pedidos_delete_select.html", {"pedidos": pedidos})
