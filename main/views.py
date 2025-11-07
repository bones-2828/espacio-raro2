from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Clientes, Producto, Pedidos, Detalles_pedidos
from .forms import ClientesForm, PedidosForm, DetallePedidosForm

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


#Crud productos

# LISTAR PRODUCTOS
def productos_list(request):
    productos = Producto.objects.all()
    return render(request, 'productos/productos_list.html', {'productos': productos})

# CREAR PRODUCTO
def productos_create(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        tipo_producto = request.POST['tipo_producto']
        talla = request.POST['talla']
        color = request.POST['color']
        precio_unitario = request.POST['precio_unitario']
        cantidad_stock = request.POST['cantidad_stock']
        distribuidor = request.POST['distribuidor']
        contacto_distribuidor = request.POST['contacto_distribuidor']
        stock_critico = request.POST['stock_critico']
        margen_ganancia = request.POST['margen_ganancia']

        Producto.objects.create(
            nombre=nombre,
            tipo_producto=tipo_producto,
            talla=talla,
            color=color,
            precio_unitario=precio_unitario,
            cantidad_stock=cantidad_stock,
            distribuidor=distribuidor,
            contacto_distribuidor=contacto_distribuidor,
            stock_critico=stock_critico,
            margen_ganancia=margen_ganancia
        )

        messages.success(request, 'Producto creado correctamente.')
        return redirect('productos_list')

    return render(request, 'productos/productos_form.html')

# EDITAR PRODUCTO
def productos_update(request, id_producto):
    producto = get_object_or_404(Producto, id_producto=id_producto)

    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.tipo_producto = request.POST['tipo_producto']
        producto.talla = request.POST['talla']
        producto.color = request.POST['color']
        producto.precio_unitario = request.POST['precio_unitario']
        producto.cantidad_stock = request.POST['cantidad_stock']
        producto.distribuidor = request.POST['distribuidor']
        producto.contacto_distribuidor = request.POST['contacto_distribuidor']
        producto.stock_critico = request.POST['stock_critico']
        producto.margen_ganancia = request.POST['margen_ganancia']

        producto.save()
        messages.success(request, 'Producto actualizado correctamente.')
        return redirect('productos_list')

    return render(request, 'productos/productos_form.html', {'producto': producto})

# ELIMINAR PRODUCTO
def productos_delete(request, id_producto):
    producto = get_object_or_404(Producto, id_producto=id_producto)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('productos_list')

    return render(request, 'productos/productos_confirm_delete.html', {'producto': producto})


#Crud Pedidos y detalles de pedidos

def pedidos_list(request):
    pedidos = Pedidos.objects.select_related('cliente').all()
    return render(request, 'pedidos/pedidos_list.html', {'pedidos': pedidos})

def pedidos_create(request):
    if request.method == 'POST':
        form = PedidosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedidos_list')
    else:
        form = PedidosForm()
    return render(request, 'pedidos/pedidos_form.html', {'form': form})

def pedidos_detail(request, pk):
    pedido = get_object_or_404(Pedidos, pk=pk)
    detalles = pedido.detalles.select_related('producto').all()
    return render(request, 'pedidos/pedidos_detail.html', {'pedido': pedido, 'detalles': detalles})

def pedidos_update(request, pk):
    pedido = get_object_or_404(Pedidos, pk=pk)
    if request.method == 'POST':
        form = PedidosForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('pedidos_list')
    else:
        form = PedidosForm(instance=pedido)
    return render(request, 'pedidos/pedidos_form.html', {'form': form})

def pedidos_delete(request, pk):
    pedido = get_object_or_404(Pedidos, pk=pk)
    if request.method == 'POST':
        pedido.delete()
        return redirect('pedidos_list')
    return render(request, 'pedidos/pedidos_confirm_delete.html', {'pedido': pedido})



# ======== CRUD DETALLES DE PEDIDOS ========

def detalles_pedidos_list(request):
    detalles = Detalles_pedidos.objects.all()
    return render(request, 'detalles_pedidos/detalles_pedidos_list.html', {'detalles': detalles})



def detalles_pedidos_create(request):
    form = DetallePedidosForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Detalle de pedido creado correctamente.")
            return redirect('detalles_pedidos_list')
        else:
            messages.error(request, "Error al crear el detalle del pedido.")
    return render(request, 'detalles_pedidos/detalles_form.html', {'form': form})



def detalles_pedidos_update(request, pk):
    detalle = get_object_or_404(Detalles_pedidos, pk=pk)

    if request.method == 'POST':
        form = DetallePedidosForm(request.POST, instance=detalle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Detalle de pedido actualizado correctamente.')
            return redirect('detalles_pedidos_list')
    else:
        form = DetallePedidosForm(instance=detalle)

    return render(request, 'detalles_pedidos/detalles_form.html', {'form': form})


# --- ELIMINAR DETALLE ---
def detalles_pedidos_delete(request, pk):
    detalle = get_object_or_404(Detalles_pedidos, pk=pk)

    if request.method == 'POST':
        detalle.delete()
        messages.success(request, 'Detalle de pedido eliminado correctamente.')
        return redirect('detalles_pedidos_list')

    return render(request, 'detalles_pedidos/detalles_confirm_delete.html', {'detalle': detalle})
