from django.db import models

class Clientes(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25)
    apellido = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    tipo_producto = models.CharField(max_length=100)
    talla = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_stock = models.IntegerField()
    distribuidor = models.CharField(max_length=30)
    contacto_distribuidor = models.CharField(max_length=50)
    stock_critico = models.IntegerField()
    margen_ganancia = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nombre


class Pedidos(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, related_name="pedidos")
    fecha_inicio = models.DateField()
    fecha_entrega = models.DateField()
    fecha_termino = models.DateField()
    estado = models.CharField(max_length=50)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido #{self.id_pedido} - {self.cliente.nombre}"


class Detalles_pedidos(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle #{self.id_detalle} - Pedido {self.pedido.id_pedido}"
