# Nivel 1 - operadores logicos (basico)
# Autores: Cristopher Arboleda y Juan Pablo Ruiz
# Comentarios: version ligeramente modificada para entrega

# Ejercicio 1.1 - booleanos simples
print('E1.1:', True and False)   # False
print('E1.1:', True or False)    # True
print('E1.1:', not True)         # False
print('E1.1:', not False)        # True

# Ejercicio 1.2 - combinaciones
p, q, r = True, False, True
print('E1.2:', p and q)   # False
print('E1.2:', p or q)    # True
print('E1.2:', q or r)    # True
print('E1.2:', p and r)   # True

# Ejercicio 1.3 - precedencia
p, q, r = True, False, True
print('E1.3:', (p and q) or r)   # True
print('E1.3:', p or (q and r))   # True
print('E1.3:', (not p) or q)     # False
print('E1.3:', not (p or q))     # False

# Ejercicio 1.4 - comparaciones
val = 5
print('E1.4:', val > 3 and val < 10)  # True
print('E1.4:', val < 3 or val > 10)   # False
print('E1.4:', not (val > 3))         # False

# Ejercicio 1.5 - encadenadas
val = 5
print('E1.5:', 3 < val < 10)   # True
print('E1.5:', 1 <= val <= 3)  # False
print('E1.5:', 10 > val > 3)   # True
