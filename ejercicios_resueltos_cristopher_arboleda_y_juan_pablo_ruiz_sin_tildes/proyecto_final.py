# Proyecto final - sistema de control de acceso
# Autores: Cristopher Arboleda y Juan Pablo Ruiz

usuarios = [
    {'id':1,'nombre':'Admin','roles':['admin'],'permisos':['leer','escribir','eliminar'],'plan':'premium','activo':True,'edad':35},
    {'id':2,'nombre':'Usuario Regular','roles':['usuario'],'permisos':['leer'],'plan':'basico','activo':True,'edad':17},
    {'id':3,'nombre':'Invitado','roles':['invitado'],'permisos':[],'plan':'gratis','activo':False,'edad':20},
]

recursos = [
    {'id':1,'nombre':'Panel Admin','requiere_rol':['admin'],'requiere_permiso':'eliminar','solo_premium':False,'solo_adultos':False},
    {'id':2,'nombre':'Contenido Premium','requiere_rol':['usuario','admin'],'requiere_permiso':'leer','solo_premium':True,'solo_adultos':False},
    {'id':3,'nombre':'Contenido Adultos','requiere_rol':['usuario','admin'],'requiere_permiso':'leer','solo_premium':False,'solo_adultos':True},
]

def puede_acceder_recurso(usuario, recurso):
    # verificar activo
    if not usuario.get('activo', False):
        return False, 'usuario inactivo'
    # verificar roles (al menos uno en comun)
    if 'requiere_rol' in recurso:
        allowed = False
        for r in usuario.get('roles', []):
            if r in recurso.get('requiere_rol', []):
                allowed = True
                break
        if not allowed:
            return False, 'rol no permitido'
    # verificar permiso especifico
    if recurso.get('requiere_permiso') and recurso.get('requiere_permiso') not in usuario.get('permisos', []):
        return False, 'falta permiso'
    # verificar plan premium
    if recurso.get('solo_premium', False) and usuario.get('plan') != 'premium':
        return False, 'requiere plan premium'
    # verificar edad
    if recurso.get('solo_adultos', False) and usuario.get('edad', 0) < 18:
        return False, 'solo mayores'
    return True, 'acceso permitido'

def probar_accesos():
    resultados = []
    for u in usuarios:
        for r in recursos:
            ok, motivo = puede_acceder_recurso(u, r)
            print(f'Usuario: {u["nombre"]} -> Recurso: {r["nombre"]} -> Acceso: {ok} -> Motivo: {motivo}')
            resultados.append({'usuario':u['nombre'],'recurso':r['nombre'],'acceso':ok,'motivo':motivo})
    return resultados

if __name__ == '__main__':
    probar_accesos()
    # no somos expertos pero sabemos cositas :P
