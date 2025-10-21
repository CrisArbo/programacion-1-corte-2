
#!/usr/bin/env python3
# run_demo.py - lanzador principal para el proyecto Parcial2_CristopherA
import os, time
from calculadora_cientifica import menu as menu_calculadora, demo as demo_calculadora
from sistema_biblioteca import menu_biblioteca, demo as demo_biblioteca
from sistema_restaurante import menu_restaurante, demo as demo_restaurante

def separador(t):
    print()
    print("="*60)
    print(t)
    print("="*60)

def ejemplo_predeterminado():
    separador("EJEMPLO PREDETERMINADO - INICIO")
    print("Se ejecutaran DEMOS paso a paso: Calculadora -> Biblioteca -> Restaurante")
    time.sleep(0.7)
    try:
        demo_calculadora()
    except Exception as e:
        print("Error demo calculadora:", e)
    try:
        demo_biblioteca()
    except Exception as e:
        print("Error demo biblioteca:", e)
    try:
        demo_restaurante()
    except Exception as e:
        print("Error demo restaurante:", e)
    separador("EJEMPLO PREDETERMINADO - FIN")
    input("Presiona Enter para volver al menu principal...")

def menu_principal():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print()
        print("#"*60)
        print("    PROYECTO PARCIAL 2 - CRISTOPHERA".center(60))
        print("#"*60)
        print("1. Calculadora cientifica (interactiva)")
        print("2. Sistema de biblioteca (interactivo)")
        print("3. Sistema de restaurante (interactivo)")
        print("4. Ejemplo predeterminado (muestra los tres, paso a paso)")
        print("0. Salir")
        op = input("Elige una opcion: ").strip()

        if op == "1":
            try:
                menu_calculadora()
            except Exception as e:
                print("Error al abrir calculadora:", e); input("Presiona Enter...")
        elif op == "2":
            try:
                menu_biblioteca()
            except Exception as e:
                print("Error al abrir biblioteca:", e); input("Presiona Enter...")
        elif op == "3":
            try:
                menu_restaurante()
            except Exception as e:
                print("Error al abrir restaurante:", e); input("Presiona Enter...")
        elif op == "4":
            ejemplo_predeterminado()
        elif op == "0":
            print("Saliendo..."); break
        else:
            print("Opcion no valida."); time.sleep(0.8)

if __name__ == '__main__':
    menu_principal()
