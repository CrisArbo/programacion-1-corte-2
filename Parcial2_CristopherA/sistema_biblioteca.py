
#!/usr/bin/env python3
# sistema_biblioteca.py
from datetime import datetime, timedelta
import os

class ErrorBiblioteca(Exception):
    pass

class LibroNoEncontrado(ErrorBiblioteca):
    def __init__(self, isbn):
        self.isbn = isbn
        super().__init__(f"Libro con ISBN {isbn} no encontrado")

class LibroNoDisponible(ErrorBiblioteca):
    def __init__(self, isbn, titulo):
        self.isbn = isbn; self.titulo = titulo
        super().__init__(f"No hay copias disponibles de '{titulo}'")

class UsuarioNoRegistrado(ErrorBiblioteca):
    def __init__(self, id_usuario):
        self.id_usuario = id_usuario
        super().__init__(f"Usuario con ID '{id_usuario}' no esta registrado")

class LimitePrestamosExcedido(ErrorBiblioteca):
    def __init__(self, id_usuario, limite):
        self.id_usuario = id_usuario; self.limite = limite
        super().__init__(f"Usuario {id_usuario} excede limite de {limite} prestamos")

class PrestamoVencido(ErrorBiblioteca):
    def __init__(self, id_prestamo, dias_retraso):
        self.id_prestamo = id_prestamo; self.dias_retraso = dias_retraso
        super().__init__(f"Prestamo {id_prestamo} esta vencido por {dias_retraso} dias")

class SistemaBiblioteca:
    def __init__(self, dias_prestamo=14, multa_por_dia=1.0, limite_prestamos=3):
        self.dias_prestamo = int(dias_prestamo)
        self.multa_por_dia = float(multa_por_dia)
        self.limite_prestamos = int(limite_prestamos)
        self.catalogo = {}
        self.usuarios = {}
        self.prestamos = {}
        self._contador_prestamos = 0
        self._prestados_por_libro = {}

    def _nuevo_id_prestamo(self):
        self._contador_prestamos += 1
        return f"P{self._contador_prestamos:06d}"

    def agregar_libro(self, isbn, titulo, autor, anio, categoria, copias):
        if not (isinstance(isbn, str) and isbn.isdigit() and len(isbn)==13):
            raise ValueError("ISBN debe ser string de 13 digitos")
        if not titulo or not autor:
            raise ValueError("Titulo y autor no pueden estar vacios")
        current_year = datetime.now().year
        if not (1000 <= int(anio) <= current_year):
            raise ValueError("Anio invalido")
        if copias < 1:
            raise ValueError("Copias debe ser >= 1")
        if isbn in self.catalogo:
            raise KeyError(f"ISBN {isbn} ya existe")
        self.catalogo[isbn] = {'titulo': str(titulo), 'autor': str(autor), 'anio': int(anio), 'categoria': str(categoria), 'copias_total': int(copias), 'copias_disponibles': int(copias)}

    def importar_catalogo(self, archivo='catalogo_inicial.txt'):
        if not os.path.exists(archivo):
            return {'exitosos':0, 'errores':[(0,'Archivo no existe')]}
        exitosos = 0; errores = []
        with open(archivo, 'r', encoding='utf-8') as f:
            for i, linea in enumerate(f, start=1):
                linea=linea.strip()
                if not linea: continue
                partes = linea.split("|")
                if len(partes) != 6:
                    errores.append((i, "Formato incorrecto")); continue
                isbn, titulo, autor, anio_s, categoria, copias_s = partes
                try:
                    if isbn in self.catalogo:
                        errores.append((i, f"ISBN {isbn} ya existe (saltado)")); continue
                    if not isbn.isdigit() or len(isbn)!=13:
                        raise ValueError("ISBN invalido")
                    anio = int(anio_s); copias = int(copias_s)
                    self.agregar_libro(isbn, titulo, autor, anio, categoria, copias)
                    exitosos += 1
                except Exception as e:
                    errores.append((i, str(e)))
        return {'exitosos':exitosos, 'errores':errores}

    def registrar_usuario(self, id_usuario, nombre, email):
        if not nombre:
            raise ValueError("Nombre no puede estar vacio")
        if '@' not in email or '.' not in email.split('@')[-1]:
            raise ValueError("Email invalido")
        if id_usuario in self.usuarios:
            raise ValueError("ID de usuario debe ser unico")
        self.usuarios[id_usuario] = {'nombre': nombre, 'email': email, 'fecha_registro': datetime.now(), 'prestamos_activos': [], 'historial': [], 'multas_pendientes': 0.0}
        return True

    def prestar_libro(self, isbn, id_usuario):
        if id_usuario not in self.usuarios:
            raise UsuarioNoRegistrado(id_usuario)
        if isbn not in self.catalogo:
            raise LibroNoEncontrado(isbn)
        libro = self.catalogo[isbn]
        if libro['copias_disponibles'] <= 0:
            raise LibroNoDisponible(isbn, libro['titulo'])
        usuario = self.usuarios[id_usuario]
        if len(usuario['prestamos_activos']) >= self.limite_prestamos:
            raise LimitePrestamosExcedido(id_usuario, self.limite_prestamos)
        if usuario.get('multas_pendientes', 0.0) > 50:
            raise ValueError("Usuario tiene multas pendientes mayores a 50")
        id_p = self._nuevo_id_prestamo()
        fecha_p = datetime.now()
        fecha_v = fecha_p + timedelta(days=self.dias_prestamo)
        self.prestamos[id_p] = {'isbn': isbn, 'id_usuario': id_usuario, 'fecha_prestamo': fecha_p, 'fecha_vencimiento': fecha_v, 'fecha_devolucion': None, 'multa': 0.0}
        libro['copias_disponibles'] -= 1
        usuario['prestamos_activos'].append(id_p)
        usuario['historial'].append(id_p)
        self._prestados_por_libro[isbn] = self._prestados_por_libro.get(isbn,0) + 1
        return id_p

    def devolver_libro(self, id_prestamo):
        if id_prestamo not in self.prestamos:
            raise KeyError("Prestamo no existe")
        prest = self.prestamos[id_prestamo]
        if prest['fecha_devolucion'] is not None:
            raise ValueError("Prestamo ya fue devuelto")
        ahora = datetime.now()
        dias_retraso = 0; multa = 0.0
        if ahora > prest['fecha_vencimiento']:
            dias_retraso = (ahora - prest['fecha_vencimiento']).days
            multa = dias_retraso * self.multa_por_dia
        prest['fecha_devolucion'] = ahora
        prest['multa'] = round(multa,2)
        isbn = prest['isbn']
        if isbn in self.catalogo:
            self.catalogo[isbn]['copias_disponibles'] += 1
        id_usuario = prest['id_usuario']
        if id_usuario in self.usuarios:
            if id_prestamo in self.usuarios[id_usuario]['prestamos_activos']:
                self.usuarios[id_usuario]['prestamos_activos'].remove(id_prestamo)
            if multa > 0:
                self.usuarios[id_usuario]['multas_pendientes'] += multa
        return {'dias_retraso': dias_retraso, 'multa': round(multa,2), 'mensaje': "Devolucion procesada"}

    def libros_mas_prestados(self, n=10):
        items = sorted(self._prestados_por_libro.items(), key=lambda x: x[1], reverse=True)
        return [(isbn, self.catalogo.get(isbn,{}).get('titulo','Titulo desconocido'), cnt) for isbn, cnt in items[:n]]

    def reporte_financiero(self, fecha_inicio=None, fecha_fin=None):
        total_multas = 0.0; multas_pagadas = 0.0; multas_pendientes = 0.0; prestamos_con_multa = 0
        for prest in self.prestamos.values():
            fecha_ref = prest['fecha_devolucion'] if prest['fecha_devolucion'] is not None else prest['fecha_prestamo']
            if fecha_inicio and fecha_ref < fecha_inicio: continue
            if fecha_fin and fecha_ref > fecha_fin: continue
            multa = prest.get('multa',0.0)
            if multa > 0:
                prestamos_con_multa += 1; total_multas += multa
                if prest.get('fecha_devolucion') is not None: multas_pagadas += multa
        for u in self.usuarios.values():
            multas_pendientes += u.get('multas_pendientes',0.0)
        return {'total_multas': round(total_multas + multas_pendientes,2), 'multas_pagadas': round(multas_pagadas,2), 'multas_pendientes': round(multas_pendientes,2), 'prestamos_con_multa': prestamos_con_multa, 'promedio_multa': round((total_multas / prestamos_con_multa),2) if prestamos_con_multa else 0.0}

def menu_biblioteca():
    sistema = SistemaBiblioteca()
    sistema.importar_catalogo()

    while True:
        print()
        print("="*54)
        print("SISTEMA DE BIBLIOTECA".center(54))
        print("="*54)
        print("1. Importar catalogo desde archivo")
        print("2. Agregar libro manualmente")
        print("3. Registrar usuario")
        print("4. Prestar libro")
        print("5. Devolver libro")
        print("6. Libros mas prestados")
        print("7. Reporte financiero (multas)")
        print("0. Volver al menu principal")
        op = input("Elige una opcion: ").strip()

        try:
            if op == "1":
                res = sistema.importar_catalogo(); print(f"Importados: {res['exitosos']}, Errores: {len(res['errores'])}")
            elif op == "2":
                isbn = input("ISBN (13 digitos): "); titulo = input("Titulo: "); autor = input("Autor: ")
                anio = int(input("Anio: ")); categoria = input("Categoria: "); copias = int(input("Copias: "))
                sistema.agregar_libro(isbn, titulo, autor, anio, categoria, copias); print("Libro agregado.")
            elif op == "3":
                uid = input("ID usuario: "); nombre = input("Nombre: "); email = input("Email: ")
                sistema.registrar_usuario(uid, nombre, email); print("Usuario registrado.")
            elif op == "4":
                isbn = input("ISBN: "); uid = input("ID usuario: ")
                pid = sistema.prestar_libro(isbn, uid); print("Prestamo creado:", pid)
            elif op == "5":
                pid = input("ID prestamo: ")
                res = sistema.devolver_libro(pid); print("Devolucion:", res)
            elif op == "6":
                top = sistema.libros_mas_prestados(10)
                for isbn, titulo, cnt in top:
                    print(f"{titulo} ({isbn}) - {cnt} prestamos")
            elif op == "7":
                r = sistema.reporte_financiero(); print("Reporte financiero:", r)
            elif op == "0":
                break
            else:
                print("Opcion no valida.")
        except Exception as e:
            print("Error:", e)

def demo():
    print()
    print("=== DEMO BIBLIOTECA - PASO A PASO ===")
    s = SistemaBiblioteca(dias_prestamo=7, multa_por_dia=2.0, limite_prestamos=3)
    print("1) Importando catalogo...")
    res = s.importar_catalogo('catalogo_inicial.txt'); print("   Resultado:", res)
    print("2) Registrando usuarios...")
    s.registrar_usuario('U001','Ana Garcia','ana@example.com'); s.registrar_usuario('U002','Carlos Lopez','carlos@example.com')
    print("3) Realizando prestamos...")
    try:
        p1 = s.prestar_libro('9780134685991','U001'); print(f"   Prestamo creado: {p1}")
        p2 = s.prestar_libro('9780135404676','U001'); print(f"   Prestamo creado: {p2}")
    except Exception as e:
        print("   Error al prestar:", e)
    print("4) Forzando retraso en el primer prestamo y devolviendo...")
    s.prestamos[p1]['fecha_vencimiento'] = datetime.now() - timedelta(days=4)
    dev = s.devolver_libro(p1); print("   Resultado devolucion:", dev)
    print("5) Libros mas prestados:", s.libros_mas_prestados(5))
    print("6) Reporte financiero:", s.reporte_financiero())
    print("Demo biblioteca finalizada.")
