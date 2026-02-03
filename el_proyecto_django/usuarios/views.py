from django.shortcuts import render
from django.http import JsonResponse
from .models import Usuario, Producto
from django.views.decorators.csrf import csrf_exempt

def index(request):
    usuarios = Usuario.objects.all()
    return render(request, "usuarios/index.html", {"usuarios": usuarios})

@csrf_exempt
def crear_usuario_api(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        
        if Usuario.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email ya existe"}, status=400)
        
        Usuario.objects.create(nombre=nombre, email=email)
        return JsonResponse({"estado": "creado"})
    
    return JsonResponse({"error": "Método no permitido"}, status=405)
