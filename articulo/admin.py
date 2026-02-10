from django.contrib import admin
from .models import Articulo

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista
    list_display = (
        'codigo', 
        'nombre', 
        'categoria', 
        'precio_compra', 
        'precio_venta',
        'cantidad_stock',
        'stock_bajo_display',
        'estado',
        'fecha_ultima_compra'
    )
    
    # Filtros laterales
    list_filter = ('categoria', 'estado', 'fecha_creacion')
    
    # Campos de búsqueda
    search_fields = ('codigo', 'nombre', 'descripcion')
    
    # Ordenamiento por defecto
    ordering = ('nombre',)
    
    # Campos editables directamente en la lista
    list_editable = ('estado', 'cantidad_stock')
    
    # Número de items por página
    list_per_page = 25
    
    # Campos de solo lectura
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'valor_inventario_display')
    
    # Agrupación de campos en formulario de edición
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre', 'descripcion', 'categoria')
        }),
        ('Información de Precios', {
            'fields': ('precio_compra', 'precio_venta')
        }),
        ('Control de Inventario', {
            'fields': ('cantidad_stock', 'cantidad_minima', 'estado', 'ubicacion')
        }),
        ('Información de Fechas', {
            'fields': ('fecha_ultima_compra', 'fecha_creacion', 'fecha_actualizacion')
        }),
    )
    
    # Métodos personalizados para list_display
    def stock_bajo_display(self, obj):
        if obj.stock_bajo():
            return ' BAJO'
        elif obj.cantidad_stock == 0:
            return ' AGOTADO'
        else:
            return ' OK'
    stock_bajo_display.short_description = 'Stock'
    
    def valor_inventario_display(self, obj):
        return f"${obj.valor_inventario():,.2f}"
    valor_inventario_display.short_description = 'Valor en Inventario'
    
    # Acciones personalizadas
    actions = ['marcar_como_activo', 'marcar_como_inactivo', 'actualizar_precios_10porciento']
    
    def marcar_como_activo(self, request, queryset):
        queryset.update(estado='activo')
        self.message_user(request, f"{queryset.count()} artículos marcados como activos.")
    marcar_como_activo.short_description = "Marcar como activo"
    
    def marcar_como_inactivo(self, request, queryset):
        queryset.update(estado='inactivo')
        self.message_user(request, f"{queryset.count()} artículos marcados como inactivos.")
    marcar_como_inactivo.short_description = "Marcar como inactivo"
    
    def actualizar_precios_10porciento(self, request, queryset):
        for articulo in queryset:
            articulo.precio_venta = articulo.precio_venta * 1.10
            articulo.save()
        self.message_user(request, f"Precios de {queryset.count()} artículos aumentados en 10%.")
    actualizar_precios_10porciento.short_description = "Aumentar precios 10%"