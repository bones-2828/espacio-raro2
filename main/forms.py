from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import Clientes, Pedidos, Detalles_pedidos


# ---------- FORMULARIO BASE CON ESTILO ----------
class BaseStyledForm(forms.ModelForm):
    """Aplica clases CSS automáticamente a todos los campos del formulario."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})


# ---------- FORMULARIO DE REGISTRO DE USUARIOS ----------
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Usuario'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'}),
        }


# ---------- FORMULARIO CLIENTES ----------
class ClientesForm(BaseStyledForm):
    class Meta:
        model = Clientes
        fields = ['nombre', 'apellido', 'email', 'telefono']


# ---------- FORMULARIO PEDIDOS ----------
class PedidosForm(BaseStyledForm):
    class Meta:
        model = Pedidos
        fields = ['cliente', 'fecha_inicio', 'fecha_entrega', 'fecha_termino', 'estado', 'precio_total']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_entrega': forms.DateInput(attrs={'type': 'date'}),
            'fecha_termino': forms.DateInput(attrs={'type': 'date'}),
            'precio_total': forms.NumberInput(attrs={'step': '0.01'}),
        }


# ---------- FORMULARIO DETALLES DE PEDIDO ----------
class DetallePedidosForm(BaseStyledForm):
    class Meta:
        model = Detalles_pedidos
        fields = ['pedido', 'producto', 'cantidad', 'subtotal']
        widgets = {
            'pedido': forms.Select(attrs={'class': 'form-select'}),
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


# ---------- FORMSET: RELACIÓN 1 Pedido → N Detalles ----------
DetallePedidoFormSet = inlineformset_factory(
    Pedidos,
    Detalles_pedidos,
    form=DetallePedidosForm,
    extra=1,
    can_delete=True,
)
