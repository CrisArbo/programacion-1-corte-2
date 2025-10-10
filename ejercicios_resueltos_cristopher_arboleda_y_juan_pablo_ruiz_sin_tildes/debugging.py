# Debugging - errores y correcciones
# Autores: Cristopher Arboleda y Juan Pablo Ruiz

# Debug 1 - version con problema (quitamos comprobacion de existencia)
def verificar_permisos_malo(usuario, accion):
    # Este codigo puede fallar si 'permisos' no existe en dict
    if usuario['permisos'] and accion in usuario['permisos']:
        return True
    else:
        return False

# Prueba que causa KeyError si 'permisos' no esta definido
try:
    usuario_err = {'id':1, 'nombre':'Juan'}
    print('\nDebug1 - ejecucion con version mala:')
    print('tiene permiso leer?', verificar_permisos_malo(usuario_err, 'leer'))
except Exception as e:
    print('Debug1 - error detectado:', type(e).__name__, '-', e)

# Correccion alternativa (diferente a la solucion directa)
def verificar_permisos_bueno(usuario, accion):
    # Usamos get para obtener lista vacia si no existe, y evitamos KeyError
    permisos = usuario.get('permisos') or []
    return accion in permisos

print('\nDebug1 - version corregida:')
usuario_ok = {'id':2, 'nombre':'Luis', 'permisos':['leer']}
print('tiene permiso leer?', verificar_permisos_bueno(usuario_ok, 'leer'))
print('tiene permiso borrar?', verificar_permisos_bueno(usuario_ok, 'borrar'))

# Debug 2 - version con problema en filtro de notas
estudiantes = [
    {'nombre':'Ana','nota':85},
    {'nombre':'Luis','nota':None},
    {'nombre':'Carmen','nota':92},
]

# Version original que falla cuando nota es None
try:
    print('\nDebug2 - version mala:')
    aprobados = [e for e in estudiantes if e['nota'] >= 60]
    print('Aprobados:', aprobados)
except Exception as e:
    print('Debug2 - error detectado:', type(e).__name__, '-', e)

# Version corregida alternativa (no identica a la de la guia)
def filtrar_aprobados(est_list, umbral=60):
    salida = []
    for e in est_list:
        nota = e.get('nota')
        if nota is None:
            continue
        if nota >= umbral:
            salida.append(e)
    return salida

print('\nDebug2 - version corregida:')
print('Aprobados:', filtrar_aprobados(estudiantes))
