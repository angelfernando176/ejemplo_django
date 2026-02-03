# ejemplos_windows.py - VERSIÓN PARA WINDOWS
import time
import sys

def mostrar_titulo(texto):
    """Muestra título con formato para Windows"""
    print("\n" + "="*60)
    print(f" {texto}")
    print("="*60)

def limpiar_pantalla():
    """Limpia la pantalla en Windows"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Función principal"""
    
    # Limpiar pantalla al inicio
    limpiar_pantalla()
    
    print("\n" + "★"*60)
    print("   EJEMPLOS DE ESTRUCTURAS DE CONTROL - WINDOWS")
    print("★"*60)
    print("\nPresiona Enter para comenzar...")
    input()
    
    # === EJEMPLO 1: IF ===
    limpiar_pantalla()
    mostrar_titulo("1. ESTRUCTURA IF - ELIF - ELSE")
    
    print("TOMA DECISIONES basadas en condiciones\n")
    
    # Simular notas de estudiantes
    estudiantes = [
        ("Ana", 95),
        ("Carlos", 85),
        ("María", 72),
        ("Pedro", 65)
    ]
    
    for nombre, nota in estudiantes:
        print(f" {nombre}: Nota = {nota}")
        
        if nota >= 90:
            print("    EXCELENTE (>= 90)")
        elif nota >= 80:
            print("    BUENO (80-89)")
        elif nota >= 70:
            print("    REGULAR (70-79)")
        else:
            print("    NECESITA MEJORAR (< 70)")
        
        time.sleep(0.5)
    
    input("\n\nPresiona Enter para continuar...")
    
    # === EJEMPLO 2: FOR ===
    limpiar_pantalla()
    mostrar_titulo("2. ESTRUCTURA FOR")
    
    print(" REPITE acciones para cada elemento\n")
    
    print(" Recorriendo días de la semana:")
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    
    for i, dia in enumerate(dias, 1):
        print(f"   {i}. {dia}")
        time.sleep(0.3)
    
    input("\n\nPresiona Enter para continuar...")
    
    # === EJEMPLO 3: WHILE ===
    limpiar_pantalla()
    mostrar_titulo("3. ESTRUCTURA WHILE")
    
    print(" REPITE MIENTRAS condición sea verdadera\n")
    print("  ¡CUIDADO! Si no cambia la condición → BUCLE INFINITO\n")
    
    print(" Contando del 1 al 5:")
    contador = 1
    
    while contador <= 5:
        print(f"   Número: {contador}")
        contador += 1  # IMPORTANTE: Modificar la condición
        time.sleep(0.4)
    
    print(f"\n Bucle terminado. Valor final: {contador}")
    
    input("\n\nPresiona Enter para continuar...")
    
    # === EJEMPLO 4: BREAK ===
    limpiar_pantalla()
    mostrar_titulo("4. INSTRUCCIÓN BREAK")
    
    print(" DETIENE COMPLETAMENTE el bucle\n")
    
    print(" Buscando el número 7 en 1-10:")
    for numero in range(1, 11):
        print(f"   Probando: {numero}")
        
        if numero == 7:
            print(f"    ¡ENCONTRADO! {numero}")
            print("    BREAK: Deteniendo bucle...")
            break
        
        time.sleep(0.3)
    
    input("\n\nPresiona Enter para continuar...")
    
    # === EJEMPLO 5: CONTINUE ===
    limpiar_pantalla()
    mostrar_titulo("5. INSTRUCCIÓN CONTINUE")
    
    print(" SALTA a la siguiente iteración\n")
    
    print(" Procesando solo números mayores a 5:")
    numeros = [3, 8, 1, 9, 4, 7, 2]
    
    for num in numeros:
        if num <= 5:
            print(f"   {num} ≤ 5 → CONTINUE (se salta)")
            continue
        
        print(f"   {num} > 5 → Procesando...")
        time.sleep(0.3)
    
    # === FINAL ===
    limpiar_pantalla()
    mostrar_titulo(" EJEMPLOS COMPLETADOS")
    
    print("\n Has visto todas las estructuras de control:")
    print("   1. IF-ELIF-ELSE → Decisiones")
    print("   2. FOR → Repetición sobre lista")
    print("   3. WHILE → Repetición condicional")
    print("   4. BREAK → Salida temprana")
    print("   5. CONTINUE → Salto de iteración")
    
    print("\n" + "="*60)
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Programa interrumpido por el usuario")
        sys.exit(0)