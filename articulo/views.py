from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Count, Avg
from django.core.paginator import Paginator
from .models import Articulo
from .forms import ArticuloForm

# ========== VISTAS PRINCIPALES ==========

def lista_articulos(request):
    """Lista todos los artículos con filtros y paginación"""
    articulos = Articulo.objects.all().order_by('nombre')
    
    # ========== FILTROS ==========
    categoria = request.GET.get('categoria')
    if categoria:
        articulos = articulos.filter(categoria=categoria)
    
    estado = request.GET.get('estado')
    if estado:
        articulos = articulos.filter(estado=estado)
    
    stock_bajo = request.GET.get('stock_bajo')
    if stock_bajo == '1':
        articulos = [a for a in articulos if a.stock_bajo()]
    
    buscar = request.GET.get('buscar')
    if buscar:
        articulos = articulos.filter(
            nombre__icontains=buscar
        ) | articulos.filter(
            codigo__icontains=buscar
        ) | articulos.filter(
            descripcion__icontains=buscar
        )
    
    # ========== PAGINACIÓN ==========
    paginator = Paginator(articulos, 15)  # 15 artículos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # ========== ESTADÍSTICAS ==========
    total_articulos = Articulo.objects.count()
    total_valor_inventario = sum(a.valor_inventario() for a in Articulo.objects.all())
    
    articulos_stock_bajo = [a for a in Articulo.objects.all() if a.stock_bajo()]
    articulos_agotados = Articulo.objects.filter(estado='agotado').count()
    
    # Estadísticas por categoría
    categorias_stats = {}
    for cat_code, cat_name in Articulo.CATEGORIA_CHOICES:
        articulos_cat = Articulo.objects.filter(categoria=cat_code)
        if articulos_cat.exists():
            categorias_stats[cat_name] = {
                'cantidad': articulos_cat.count(),
                'valor_total': sum(a.valor_inventario() for a in articulos_cat),
                'porcentaje': (articulos_cat.count() / total_articulos * 100) if total_articulos > 0 else 0
            }
    
    context = {
        'page_obj': page_obj,
        'articulos': page_obj.object_list,
        'total_articulos': total_articulos,
        'total_valor_inventario': total_valor_inventario,
        'articulos_stock_bajo': articulos_stock_bajo,
        'articulos_agotados': articulos_agotados,
        'categorias_stats': categorias_stats,
        'categorias': Articulo.CATEGORIA_CHOICES,
        'estados': Articulo.ESTADO_CHOICES,
        'buscar': buscar or '',
        'categoria_filtro': categoria or '',
        'estado_filtro': estado or '',
    }
    
    return render(request, 'articulo/lista.html', context)

def detalle_articulo(request, pk):
    """Muestra el detalle de un artículo específico"""
    articulo = get_object_or_404(Articulo, pk=pk)
    
    # Información relacionada (podría extenderse)
    articulos_similares = Articulo.objects.filter(
        categoria=articulo.categoria
    ).exclude(pk=pk)[:5]
    
    context = {
        'articulo': articulo,
        'articulos_similares': articulos_similares,
        'margen': articulo.margen_ganancia(),
        'valor_total': articulo.valor_inventario(),
        'necesita_reabastecer': articulo.necesita_reabastecer(),
    }
    return render(request, 'articulo/detalle.html', context)

def crear_articulo(request):
    """Crea un nuevo artículo"""
    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        if form.is_valid():
            articulo = form.save()
            messages.success(
                request, 
                f' Artículo "{articulo.nombre}" creado exitosamente.'
            )
            return redirect('lista_articulos')
        else:
            messages.error(
                request, 
                ' Por favor corrige los errores en el formulario.'
            )
    else:
        form = ArticuloForm()
    
    return render(request, 'articulo/crear.html', {'form': form})

def editar_articulo(request, pk):
    """Edita un artículo existente"""
    articulo = get_object_or_404(Articulo, pk=pk)
    
    if request.method == 'POST':
        form = ArticuloForm(request.POST, instance=articulo)
        if form.is_valid():
            articulo = form.save()
            messages.success(
                request, 
                f' Artículo "{articulo.nombre}" actualizado exitosamente.'
            )
            return redirect('lista_articulos')
        else:
            messages.error(
                request, 
                ' Por favor corrige los errores en el formulario.'
            )
    else:
        form = ArticuloForm(instance=articulo)
    
    context = {
        'form': form,
        'articulo': articulo,
        'es_edicion': True,
    }
    return render(request, 'articulo/editar.html', context)

def eliminar_articulo(request, pk):
    """Elimina un artículo"""
    articulo = get_object_or_404(Articulo, pk=pk)
    
    if request.method == 'POST':
        nombre_articulo = articulo.nombre
        articulo.delete()
        messages.success(
            request, 
            f' Artículo "{nombre_articulo}" eliminado exitosamente.'
        )
        return redirect('lista_articulos')
    
    return render(request, 'articulo/eliminar.html', {'articulo': articulo})

# ========== VISTAS ADICIONALES ==========

def reporte_inventario(request):
    """Genera reporte completo del inventario"""
    articulos = Articulo.objects.all()
    
    # Estadísticas generales
    total_articulos = articulos.count()
    total_valor = sum(a.valor_inventario() for a in articulos)
    valor_promedio = total_valor / total_articulos if total_articulos > 0 else 0
    
    # Artículos por estado
    por_estado = {}
    for estado_code, estado_nombre in Articulo.ESTADO_CHOICES:
        count = articulos.filter(estado=estado_code).count()
        if count > 0:
            por_estado[estado_nombre] = {
                'cantidad': count,
                'porcentaje': (count / total_articulos * 100) if total_articulos > 0 else 0
            }
    
    # Top 10 artículos por valor
    top_valor = sorted(
        [(a, a.valor_inventario()) for a in articulos],
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    # Artículos que necesitan reabastecimiento urgente
    urgente_reabastecer = [a for a in articulos if a.necesita_reabastecer()]
    
    context = {
        'articulos': articulos,
        'total_articulos': total_articulos,
        'total_valor': total_valor,
        'valor_promedio': valor_promedio,
        'por_estado': por_estado,
        'top_valor': top_valor,
        'urgente_reabastecer': urgente_reabastecer,
        'articulos_stock_bajo': [a for a in articulos if a.stock_bajo()],
    }
    return render(request, 'articulo/reporte.html', context)

def dashboard(request):
    """Dashboard con métricas principales"""
    articulos = Articulo.objects.all()
    
    # Métricas principales
    metricas = {
        'total_articulos': articulos.count(),
        'total_valor_inventario': sum(a.valor_inventario() for a in articulos),
        'articulos_activos': articulos.filter(estado='activo').count(),
        'articulos_agotados': articulos.filter(estado='agotado').count(),
        'articulos_stock_bajo': len([a for a in articulos if a.stock_bajo()]),
        'valor_promedio_articulo': sum(a.valor_inventario() for a in articulos) / articulos.count() if articulos.count() > 0 else 0,
    }
    
    # Distribución por categoría (para gráfico)
    distribucion_categoria = []
    for cat_code, cat_name in Articulo.CATEGORIA_CHOICES:
        count = articulos.filter(categoria=cat_code).count()
        if count > 0:
            distribucion_categoria.append({
                'categoria': cat_name,
                'cantidad': count,
                'valor': sum(a.valor_inventario() for a in articulos.filter(categoria=cat_code))
            })
    
    # Últimos artículos agregados
    ultimos_articulos = articulos.order_by('-fecha_creacion')[:5]
    
    # Artículos que necesitan atención
    atencion_urgente = [a for a in articulos if a.necesita_reabastecer()][:5]
    
    context = {
        'metricas': metricas,
        'distribucion_categoria': distribucion_categoria,
        'ultimos_articulos': ultimos_articulos,
        'atencion_urgente': atencion_urgente,
    }
    return render(request, 'articulo/dashboard.html', context)

# ========== VISTAS API/JSON ==========

def api_articulos_json(request):
    """API simple para obtener artículos en JSON"""
    articulos = Articulo.objects.all().values(
        'id', 'codigo', 'nombre', 'categoria', 
        'precio_compra', 'precio_venta', 'cantidad_stock', 'estado'
    )
    return JsonResponse(list(articulos), safe=False)

def api_stock_bajo_json(request):
    """API para artículos con stock bajo"""
    articulos = [a for a in Articulo.objects.all() if a.stock_bajo()]
    data = [
        {
            'id': a.id,
            'codigo': a.codigo,
            'nombre': a.nombre,
            'stock_actual': a.cantidad_stock,
            'stock_minimo': a.cantidad_minima,
            'diferencia': a.cantidad_minima - a.cantidad_stock,
            'url': f'/articulo/{a.id}/'
        }
        for a in articulos
    ]
    return JsonResponse(data, safe=False)