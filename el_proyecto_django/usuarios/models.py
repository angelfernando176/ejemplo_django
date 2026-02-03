from django.db import models

# Create your models here.
# usuarios/models.py
from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    
    # Estructura de control condicional en método
    def esta_disponible(self):
        if self.stock > 0:
            return True
        else:
            return False
    
    # Ejemplo de estructura de iteración (simulada)
    @classmethod
    def productos_con_descuento(cls, porcentaje):
        productos = cls.objects.all()
        for producto in productos:
            # break si encontramos producto caro
            if producto.precio > 1000:
                break
            producto.precio *= (1 - porcentaje/100)
        return productos

# Ejecutar migraciones
# Terminal: python manage.py makemigrations
# Terminal: python manage.py migrate