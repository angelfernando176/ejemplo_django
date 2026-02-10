from django.db import models

class Articulo(models.Model):
    """Modelo para representar artículos en el inventario"""
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('agotado', 'Agotado'),
        ('descontinuado', 'Descontinuado'),
    ]
    
    CATEGORIA_CHOICES = [
        ('electronica', 'Electrónica'),
        ('ropa', 'Ropa y Accesorios'),
        ('hogar', 'Hogar y Muebles'),
        ('alimentos', 'Alimentos'),
        ('bebidas', 'Bebidas'),
        ('limpieza', 'Limpieza'),
        ('papeleria', 'Papelería'),
        ('herramientas', 'Herramientas'),
        ('deportes', 'Deportes'),
        ('otros', 'Otros'),
    ]
    
    # Campos principales
    codigo = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Código de Artículo",
        help_text="Código único identificador"
    )
    nombre = models.CharField(
        max_length=200, 
        verbose_name="Nombre del Artículo"
    )
    descripcion = models.TextField(
        verbose_name="Descripción", 
        blank=True, 
        help_text="Descripción detallada del artículo"
    )
    categoria = models.CharField(
        max_length=50, 
        choices=CATEGORIA_CHOICES, 
        default='otros',
        verbose_name="Categoría"
    )
    
    # Campos numéricos
    precio_compra = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Precio de Compra",
        default=0.00
    )
    precio_venta = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Precio de Venta",
        default=0.00
    )
    cantidad_stock = models.IntegerField(
        default=0, 
        verbose_name="Cantidad en Stock"
    )
    cantidad_minima = models.IntegerField(
        default=5, 
        verbose_name="Stock Mínimo",
        help_text="Cantidad mínima antes de alerta"
    )
    
    # Campos de estado
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='activo',
        verbose_name="Estado"
    )
    ubicacion = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Ubicación en Almacén",
        help_text="Ej: Estante A-5, Pasillo 3"
    )
    
    # Campos de auditoría
    fecha_creacion = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Fecha de Creación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True, 
        verbose_name="Última Actualización"
    )
    fecha_ultima_compra = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Fecha Última Compra"
    )
    
    # Métodos personalizados
    def stock_bajo(self):
        """Verifica si el stock está por debajo del mínimo"""
        return self.cantidad_stock < self.cantidad_minima
    
    def valor_inventario(self):
        """Calcula el valor total en inventario"""
        return self.precio_compra * self.cantidad_stock
    
    def margen_ganancia(self):
        """Calcula el margen de ganancia por unidad"""
        if self.precio_compra > 0:
            return ((self.precio_venta - self.precio_compra) / self.precio_compra) * 100
        return 0
    
    def necesita_reabastecer(self):
        """Determina si necesita reabastecimiento urgente"""
        return self.cantidad_stock <= (self.cantidad_minima * 0.5)
    
    # Metadata
    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"
        ordering = ['nombre', 'categoria']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['nombre']),
            models.Index(fields=['categoria']),
            models.Index(fields=['estado']),
        ]
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    def save(self, *args, **kwargs):
        """Override save para lógica adicional"""
        # Actualizar estado si stock es 0
        if self.cantidad_stock <= 0 and self.estado != 'descontinuado':
            self.estado = 'agotado'
        elif self.cantidad_stock > 0 and self.estado == 'agotado':
            self.estado = 'activo'
        
        super().save(*args, **kwargs)