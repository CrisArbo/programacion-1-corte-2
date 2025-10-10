# Nivel 3 - aplicaciones practicas (avanzado)
# Autores: Cristopher Arboleda y Juan Pablo Ruiz

# Ejercicio 3.1 - validacion de formulario (variacion en checks)
def validar_datos(nombre, email, edad, password):
    if not nombre or len(nombre) < 2 or len(nombre) > 30:
        return False
    if not isinstance(email, str) or '@' not in email:
        return False
    if not isinstance(edad, int) or edad < 18:
        return False
    if not password or len(password) < 8:
        return False
    return True

print('E3.1:', validar_datos('Ana', 'ana@email.com', 25, 'secreto123'))
print('E3.1:', validar_datos('', 'no-email', 15, '123'))

# Ejercicio 3.2 - autorizacion (uso names distintos)
def puede_acceder(usuario, permiso, lista_negra):
    if not usuario.get('autenticado'):
        return False
    if usuario.get('id') in lista_negra:
        return False
    if usuario.get('admin'):
        return True
    return permiso in usuario.get('permisos', [])

admin = {'id':1, 'autenticado':True, 'admin':True, 'permisos':['leer','escribir']}
user_norm = {'id':2, 'autenticado':True, 'admin':False, 'permisos':['leer']}
user_block = {'id':3, 'autenticado':True, 'admin':False, 'permisos':['leer','escribir']}
black = [3,4]

print('E3.2:', puede_acceder(admin, 'borrar', black))
print('E3.2:', puede_acceder(user_norm, 'leer', black))
print('E3.2:', puede_acceder(user_norm, 'escribir', black))
print('E3.2:', puede_acceder(user_block, 'leer', black))

# Ejercicio 3.3 - obtener valor seguro (sin usar get en version original)
def obtener_valor_seguro(dic, clave, defecto=None):
    return dic[clave] if clave in dic else defecto

cfg = {'timeout':30, 'retries':3}
print('E3.3:', obtener_valor_seguro(cfg, 'timeout'), obtener_valor_seguro(cfg, 'cache'), obtener_valor_seguro(cfg, 'cache', 60))

# Ejercicio 3.4 - filtrar productos (variacion legible)
def filtrar_productos(lista_prod, pmin, pmax, cat=None):
    out = []
    for item in lista_prod:
        if not item.get('disponible', False):
            continue
        precio = item.get('precio', 0)
        if precio < pmin or precio > pmax:
            continue
        if cat and item.get('categoria') != cat:
            continue
        out.append(item)
    return out

productos = [
    {'nombre':'Laptop','precio':1200,'categoria':'Electronica','disponible':True},
    {'nombre':'Telefono','precio':800,'categoria':'Electronica','disponible':False},
    {'nombre':'Libro','precio':15,'categoria':'Libros','disponible':True},
    {'nombre':'Audifonos','precio':200,'categoria':'Electronica','disponible':True},
]
print('E3.4:', [p['nombre'] for p in filtrar_productos(productos,0,500)])
print('E3.4:', [p['nombre'] for p in filtrar_productos(productos,100,1000,'Electronica')])

# Ejercicio 3.5 - evaluar riesgo (cambiando nombres a anios_historial)
def evaluar_riesgo(cliente):
    if cliente.get('score_crediticio',0) > 700:
        return True
    if cliente.get('ingreso_anual',0) > 50000 and cliente.get('anios_historial',0) > 2:
        return True
    if cliente.get('vip') and not cliente.get('deudas_pendientes'):
        return True
    return False

c1 = {'nombre':'Ana Garcia','score_crediticio':720,'ingreso_anual':45000,'anios_historial':3,'vip':False,'deudas_pendientes':False}
c2 = {'nombre':'Luis Perez','score_crediticio':680,'ingreso_anual':60000,'anios_historial':4,'vip':False,'deudas_pendientes':False}
c3 = {'nombre':'Carmen Ruiz','score_crediticio':690,'ingreso_anual':30000,'anios_historial':1,'vip':True,'deudas_pendientes':False}

print('E3.5:', evaluar_riesgo(c1), evaluar_riesgo(c2), evaluar_riesgo(c3))
