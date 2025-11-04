from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Clientes
from .forms import ClientesForm

# ---------------------------
# VISTAS GENERALES DEL SITIO
# ---------------------------

def homepage(request):
    return render(request, "index.html")

def order(request):
    return render(request, "quickorder.html")

# ---------------------------
# AUTENTICACIÓN Y USUARIOS
# ---------------------------

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser or user.is_staff:
                return redirect("dashboard")
            else:
                return redirect("user_dashboard")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    
    return render(request, "login.html")


def register_view(request):
    return render(request, "register.html")


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not email or not password1 or not password2:
            messages.error(request, "Todos los campos son obligatorios.")
        elif password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, "Cuenta creada correctamente. Puedes iniciar sesión.")
            return redirect('login_view')

    return render(request, 'register.html')


def is_admin(user):
    return user.is_superuser or user.is_staff


@login_required
@user_passes_test(is_admin)
def dashboard(request):
    return render(request, "dashboard.html")


def logout_view(request):
    logout(request)
    return redirect('login_view')


@login_required
def user_dashboard(request):
    if request.user.is_superuser or request.user.is_staff:
        return redirect('dashboard')
    
    context = {'username': request.user.username}
    return render(request, 'user_dashboard.html', context)

# ---------------------------
# CRUD CLIENTES
# ---------------------------

@login_required
@user_passes_test(is_admin)
def clientes_list(request):
    clientes = Clientes.objects.all()
    return render(request, 'clientes/clientes_list.html', {'clientes': clientes})


@login_required
@user_passes_test(is_admin)
def clientes_create(request):
    if request.method == 'POST':
        form = ClientesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente creado correctamente.")
            return redirect('clientes_list')
        else:
            messages.error(request, "Error al guardar el cliente.")
    else:
        form = ClientesForm()
    return render(request, 'clientes/clientes_form.html', {'form': form, 'titulo': 'Crear Cliente'})


@login_required
@user_passes_test(is_admin)
def clientes_detail(request, pk):
    cliente = get_object_or_404(Clientes, pk=pk)
    return render(request, 'clientes/clientes_detail.html', {'cliente': cliente})


@login_required
@user_passes_test(is_admin)
def clientes_update(request, pk):
    cliente = get_object_or_404(Clientes, pk=pk)
    if request.method == 'POST':
        form = ClientesForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente actualizado correctamente.")
            return redirect('clientes_list')
        else:
            messages.error(request, "Error al actualizar el cliente.")
    else:
        form = ClientesForm(instance=cliente)
    return render(request, 'clientes/clientes_update.html', {'form': form, 'titulo': 'Editar Cliente'})


@login_required
@user_passes_test(is_admin)
def clientes_delete(request, pk):
    cliente = get_object_or_404(Clientes, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, "Cliente eliminado correctamente.")
        return redirect('clientes_list')
    return render(request, 'clientes/clientes_confirm_delete.html', {'cliente': cliente})
