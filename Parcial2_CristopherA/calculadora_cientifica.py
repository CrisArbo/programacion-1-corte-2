
#!/usr/bin/env python3
# calculadora_cientifica.py
import math

class CalculadoraCientifica:
    def suma(self, a, b): return a + b
    def resta(self, a, b): return a - b
    def multiplicacion(self, a, b): return a * b
    def division(self, a, b):
        if b == 0:
            raise ZeroDivisionError("No se puede dividir por cero")
        return a / b
    def potencia(self, a, b): return a ** b
    def modulo(self, a, b):
        if b == 0:
            raise ZeroDivisionError("No se puede realizar modulo por cero")
        return a % b
    def raiz_cuadrada(self, x):
        if x < 0:
            raise ValueError("No se puede calcular raiz de numero negativo")
        return math.sqrt(x)
    def log(self, x):
        if x <= 0:
            raise ValueError("Logaritmo indefinido para valores <= 0")
        return math.log(x)
    def trigonometria(self, grados):
        rad = math.radians(grados)
        return {'sin': math.sin(rad), 'cos': math.cos(rad), 'tan': math.tan(rad)}

def _leer_numero(prompt):
    while True:
        v = input(prompt).strip()
        try:
            val = float(eval(v, {"__builtins__":None}, {"sqrt":math.sqrt, "pi":math.pi, "e":math.e}))
            return val
        except Exception:
            try:
                return float(v)
            except Exception:
                print("Entrada invalida. Introduce un numero o expresion valida.")

def menu():
    calc = CalculadoraCientifica()
    while True:
        print()
        print("="*48)
        print("CALCULADORA CIENTIFICA".center(48))
        print("="*48)
        print("1. Suma")
        print("2. Resta")
        print("3. Multiplicacion")
        print("4. Division")
        print("5. Potencia")
        print("6. Modulo")
        print("7. Raiz cuadrada")
        print("8. Log natural")
        print("9. Trigonometria (grados)")
        print("10. Ejemplo predeterminado")
        print("0. Volver")
        op = input("Elige una opcion: ").strip()
        try:
            if op == "1":
                a = _leer_numero("a = "); b = _leer_numero("b = ")
                print("Resultado:", round(calc.suma(a,b), 6))
            elif op == "2":
                a = _leer_numero("a = "); b = _leer_numero("b = ")
                print("Resultado:", round(calc.resta(a,b), 6))
            elif op == "3":
                a = _leer_numero("a = "); b = _leer_numero("b = ")
                print("Resultado:", round(calc.multiplicacion(a,b), 6))
            elif op == "4":
                a = _leer_numero("a = "); b = _leer_numero("b = ")
                print("Resultado:", round(calc.division(a,b), 6))
            elif op == "5":
                a = _leer_numero("base = "); b = _leer_numero("expo = ")
                print("Resultado:", round(calc.potencia(a,b), 6))
            elif op == "6":
                a = _leer_numero("a = "); b = _leer_numero("b = ")
                print("Resultado:", round(calc.modulo(a,b), 6))
            elif op == "7":
                a = _leer_numero("valor = ")
                print("Resultado:", round(calc.raiz_cuadrada(a), 6))
            elif op == "8":
                a = _leer_numero("valor = ")
                print("Resultado:", round(calc.log(a), 6))
            elif op == "9":
                a = _leer_numero("grados = ")
                t = calc.trigonometria(a)
                print("sin:", round(t['sin'],6), " cos:", round(t['cos'],6), " tan:", round(t['tan'],6))
            elif op == "10":
                demo()
            elif op == "0":
                break
            else:
                print("Opcion no valida.")
        except Exception as e:
            print("Error:", e)

def demo():
    calc = CalculadoraCientifica()
    print()
    print("=== DEMO CALCULADORA - PASO A PASO ===")
    print("1) Suma 12 + 7 =", calc.suma(12,7))
    print("2) Division 10 / 3 =", round(calc.division(10,3), 6))
    print("3) Potencia 2 ^ 8 =", calc.potencia(2,8))
    print("4) Raiz cuadrada de 49 =", calc.raiz_cuadrada(49))
    t = calc.trigonometria(30)
    print("5) Trigonometria 30 grados -> sin:", round(t['sin'],6), " cos:", round(t['cos'],6))
    print("Demo calculadora finalizada.")
