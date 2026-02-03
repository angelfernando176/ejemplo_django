# test_django.py (en la raíz del proyecto)
import sys
print("Python path:", sys.executable)

try:
    import django
    print("Django version:", django.__version__)
    print("✅ Django importado correctamente")
except ImportError as e:
    print("❌ Error importando Django:", e)
    print("Path de búsqueda:", sys.path)