# Crear un archivo ejemplos.py en la app usuarios
# usuarios/ejemplos.py

from usuarios.models import Usuario, Producto

# --- INSERCIÓN ---
def crear_usuario(): 
    # Crear y guardar
    usuario = Usuario(nombre="Juan", email="juan@email.com")
    usuario.save()
    
    # Método create
    Usuario.objects.create(nombre="María", email="maria@email.com")
    
    # Bulk create (múltiples)
    usuarios_lista = [
        Usuario(nombre="Pedro", email="pedro@email.com"),
        Usuario(nombre="Ana", email="ana@email.com")
    ]
    Usuario.objects.bulk_create(usuarios_lista)

# --- CONSULTA ---
def consultar_usuarios():
    # Todos los usuarios
    todos = Usuario.objects.all()
    
    # Filtrado
    juanes = Usuario.objects.filter(nombre="Juan")
    
    # Excluir
    sin_maria = Usuario.objects.exclude(nombre="María")
    
    # Obtener uno
    try:
        usuario = Usuario.objects.get(email="juan@email.com")
    except Usuario.DoesNotExist:
        print("Usuario no encontrado")
    
    # Usar for para iterar
    for usuario in Usuario.objects.all()[:5]:  # primeros 5
        print(f"Usuario: {usuario.nombre}")

# --- ACTUALIZACIÓN ---
def actualizar_usuario():
    # Actualizar uno
    usuario = Usuario.objects.get(id=1)
    usuario.nombre = "Juan Actualizado"
    usuario.save()
    
    # Actualizar múltiples
    Usuario.objects.filter(nombre__startswith="J").update(nombre="Inicial J")
    
    # Usar while para actualización condicional
    productos = Producto.objects.filter(stock__lt=10)
    while productos.exists():
        for producto in productos:
            producto.stock += 5
            producto.save()
        # Actualizar la consulta
        productos = Producto.objects.filter(stock__lt=10)

# --- BORRADO ---
def borrar_registros():
    # Borrar uno
    usuario = Usuario.objects.get(id=1)
    usuario.delete()
    
    # Borrar múltiples
    Usuario.objects.filter(email__contains="test").delete()
    
    # Borrar todos
    Usuario.objects.all().delete()

# --- USO DE BREAK Y CONTINUE ---
def procesar_usuarios():
    usuarios = Usuario.objects.all()
    
    for usuario in usuarios:
        if usuario.email is None:
            continue  # Saltar al siguiente si no tiene email
        
        print(f"Procesando: {usuario.nombre}")
        
        if usuario.nombre == "STOP":
            break  # Detener el bucle
        
        # Lógica de procesamiento