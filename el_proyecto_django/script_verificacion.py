# script_verificacion.py
import sys

print(f"Python version: {sys.version}")
print(f"Version info: {sys.version_info}")

# Verificar versión mínima
REQUIRED_VERSION = (3, 8)
current_version = sys.version_info

if current_version < REQUIRED_VERSION:
    print(f"❌ ERROR: Se requiere Python {REQUIRED_VERSION[0]}.{REQUIRED_VERSION[1]}+")
    print(f"    Versión actual: {current_version.major}.{current_version.minor}")
    sys.exit(1)
else:
    print(f"✅ Python versión compatible: {current_version.major}.{current_version.minor}")
    
# Intentar importar bibliotecas clave
try:
    import django
    print(f"✅ Django {django.__version__} - OK")
except ImportError:
    print("❌ Django no instalado")

try:
    import flask
    print(f"✅ Flask {flask.__version__} - OK")
except ImportError:
    print("❌ Flask no instalado")

try:
    import psycopg2
    print(f"✅ psycopg2 {psycopg2.__version__} - OK")
except ImportError:
    print("❌ psycopg2 no instalado")