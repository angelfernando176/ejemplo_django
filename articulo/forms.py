from django import forms
from .models import Articulo

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = '__all__'
        exclude = ['fecha_creacion', 'fecha_actualizacion', 'fecha_ultima_compra']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ART-001',
                'title': 'Código único del artículo'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del artículo'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción detallada...'
            }),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'precio_compra': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'precio_venta': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'cantidad_stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'cantidad_minima': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'title': 'Stock mínimo antes de alerta'
            }),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Estante B-3, Pasillo 2'
            }),
        }
        labels = {
            'codigo': 'Código del Artículo',
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'categoria': 'Categoría',
            'precio_compra': 'Precio de Compra ($)',
            'precio_venta': 'Precio de Venta ($)',
            'cantidad_stock': 'Stock Actual',
            'cantidad_minima': 'Stock Mínimo',
            'estado': 'Estado',
            'ubicacion': 'Ubicación en Almacén',
        }
        help_texts = {
            'codigo': 'Ingrese un código único para identificar el artículo',
            'cantidad_minima': 'Cantidad mínima antes de generar alerta',
        }
    
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        # Validar formato (opcional: ART-001)
        if not codigo:
            raise forms.ValidationError("El código es obligatorio")
        
        # Verificar unicidad (excepto en edición)
        if self.instance and self.instance.pk:
            if Articulo.objects.filter(codigo=codigo).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Este código ya está en uso por otro artículo")
        else:
            if Articulo.objects.filter(codigo=codigo).exists():
                raise forms.ValidationError("Este código ya está en uso")
        
        return codigo.upper()  # Convertir a mayúsculas
    
    def clean_precio_venta(self):
        precio_venta = self.cleaned_data.get('precio_venta')
        if precio_venta < 0:
            raise forms.ValidationError("El precio de venta no puede ser negativo")
        return precio_venta
    
    def clean_precio_compra(self):
        precio_compra = self.cleaned_data.get('precio_compra')
        if precio_compra < 0:
            raise forms.ValidationError("El precio de compra no puede ser negativo")
        return precio_compra
    
    def clean(self):
        cleaned_data = super().clean()
        precio_compra = cleaned_data.get('precio_compra')
        precio_venta = cleaned_data.get('precio_venta')
        
        # Validar que precio de venta sea mayor o igual que compra
        if precio_compra and precio_venta:
            if precio_venta < precio_compra:
                self.add_error('precio_venta', 
                    "El precio de venta no puede ser menor al precio de compra")
        
        return cleaned_data