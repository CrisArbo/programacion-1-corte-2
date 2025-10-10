# Nivel 2 - valores y cortocircuito (intermedio)
# Autores: Cristopher Arboleda y Juan Pablo Ruiz

# Ejercicio 2.1 - valores retornados por and/or
print('E2.1:', 'hola' and 'mundo')   # 'mundo'
print('E2.1:', 'hola' and '')        # ''
print('E2.1:', '' and 'mundo')       # ''
print('E2.1:', 'hola' or 'mundo')    # 'hola'
print('E2.1:', '' or 'mundo')        # 'mundo'

# Ejercicio 2.2 - truthy/falsy
print('E2.2:', bool(0), bool(''), bool([]), bool([0]), bool(' '), bool(None))

# Ejercicio 2.3 - cortocircuito con funciones (ligera variacion en nombres)
def func_a():
    print('func_a ejecutada')
    return True

def func_b():
    print('func_b ejecutada')
    return False

print('\nE2.3 Caso A:')
resA = func_a() and func_b()
print('Resultado A:', resA)

print('\nE2.3 Caso B:')
resB = func_b() and func_a()
print('Resultado B:', resB)

print('\nE2.3 Caso C:')
resC = func_a() or func_b()
print('Resultado C:', resC)

# Ejercicio 2.4 - pertenencia
numbers = [1,2,3,4,5]
txt = 'Python'
print('E2.4:', 3 in numbers, 6 in numbers, 6 not in numbers)
print('E2.4:', 'P' in txt, 'p' in txt, 'th' in txt)

# Ejercicio 2.5 - identidad vs igualdad (variacion de nombres)
list_a = [1,2,3]
list_b = [1,2,3]
list_c = list_a
print('E2.5:', list_a == list_b, list_a is list_b, list_a == list_c, list_a is list_c)
