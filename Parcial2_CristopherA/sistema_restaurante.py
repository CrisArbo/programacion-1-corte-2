
#!/usr/bin/env python3
# sistema_restaurante.py
from datetime import datetime

class ErrorRestaurante(Exception): pass

class PlatoNoEncontrado(ErrorRestaurante):
    def __init__(self, codigo): super().__init__(f"Plato con codigo '{codigo}' no encontrado")

class MesaNoDisponible(ErrorRestaurante):
    def __init__(self, numero): super().__init__(f"Mesa {numero} no esta disponible")

class PedidoInvalido(ErrorRestaurante):
    def __init__(self, razon): super().__init__(f"Pedido invalido: {razon}")

class SistemaRestaurante:
    def __init__(self, num_mesas=6, tasa_impuesto=0.16, propina_sugerida=0.1):
        self.menu = {}
        self.mesas = {}
        self.pedidos = {}
        self._ventas_por_plato = {}
        self._next_pedido = 1
        self.tasa_impuesto = float(tasa_impuesto)
        self.propina_sugerida = float(propina_sugerida)
        self._inicializar_menu(num_mesas)
        self.recaudacion_total = 0.0

    def _inicializar_menu(self, num_mesas):
        for i in range(1, num_mesas+1):
            self.mesas[i] = {'capacidad': 4, 'ocupada': False, 'pedido': None}
        platos = [
            ("R01","Taco de Pollo","Entradas",8.0),
            ("R02","Milanesa con papas","Plato fuerte",18.0),
            ("R03","Ensalada mixta","Entradas",9.5),
            ("R04","Risotto de champinones","Plato fuerte",20.0),
            ("R05","Gaseosa","Bebidas",3.5),
            ("R06","Agua mineral","Bebidas",2.5),
            ("R07","Brownie","Postre",6.0),
            ("R08","Cafe americano","Bebidas",2.0)
        ]
        for codigo, nombre, categoria, precio in platos:
            self.menu[codigo] = {'nombre': nombre, 'categoria': categoria, 'precio': float(precio), 'disponible': True}
            self._ventas_por_plato[codigo] = 0

    def mostrar_menu(self):
        print()
        print("=== MENU ===")
        for c, info in self.menu.items():
            if info['disponible']:
                print(f"{c}: {info['nombre']} - ${info['precio']:.2f} ({info['categoria']})")

    def reservar_mesa(self, numero, comensales):
        if numero not in self.mesas:
            raise ValueError("Mesa no existe")
        mesa = self.mesas[numero]
        if mesa['ocupada']:
            raise MesaNoDisponible(numero)
        if comensales > mesa['capacidad']:
            raise ValueError(f"Mesa {numero} capacidad insuficiente")
        mesa['ocupada'] = True
        print(f"Mesa {numero} reservada para {comensales} persona(s)")

    def liberar_mesa(self, numero):
        if numero not in self.mesas:
            raise ValueError("Mesa no existe")
        mesa = self.mesas[numero]
        if not mesa['ocupada']:
            print(f"Mesa {numero} ya esta libre")
            return
        mesa['ocupada'] = False
        mesa['pedido'] = None
        print(f"Mesa {numero} liberada")

    def crear_pedido(self, numero_mesa):
        if numero_mesa not in self.mesas:
            raise ValueError("Mesa no existe")
        mesa = self.mesas[numero_mesa]
        if not mesa['ocupada']:
            raise ValueError("Mesa no esta ocupada")
        pid = f"ORD{self._next_pedido:04d}"
        self._next_pedido += 1
        self.pedidos[pid] = {'mesa': numero_mesa, 'items': [], 'pagado': False, 'hora': datetime.now()}
        mesa['pedido'] = pid
        print(f"Pedido creado: {pid}")
        return pid

    def agregar_item(self, id_pedido, codigo_plato, cantidad):
        if id_pedido not in self.pedidos:
            raise PedidoInvalido("ID de pedido no existe")
        if codigo_plato not in self.menu:
            raise PlatoNoEncontrado(codigo_plato)
        if not self.menu[codigo_plato]['disponible']:
            raise PedidoInvalido("plato no disponible")
        if cantidad < 1:
            raise PedidoInvalido("cantidad invalida")
        pedido = self.pedidos[id_pedido]
        pedido['items'].append((codigo_plato, int(cantidad)))
        self._ventas_por_plato[codigo_plato] += int(cantidad)
        print(f"{cantidad} x {self.menu[codigo_plato]['nombre']} agregado al pedido {id_pedido}")

    def calcular_total(self, id_pedido, propina_porcentaje=None):
        if id_pedido not in self.pedidos:
            raise PedidoInvalido("pedido no encontrado")
        pedido = self.pedidos[id_pedido]
        subtotal = sum(self.menu[c]['precio'] * q for c,q in pedido['items'])
        impuesto = subtotal * self.tasa_impuesto
        propina = subtotal * (propina_porcentaje if propina_porcentaje is not None else self.propina_sugerida)
        total = subtotal + impuesto + propina
        return {'subtotal': round(subtotal,2), 'impuesto': round(impuesto,2), 'propina': round(propina,2), 'total': round(total,2)}

    def pagar_pedido(self, id_pedido, propina_porcentaje=None):
        if id_pedido not in self.pedidos:
            raise PedidoInvalido("pedido no encontrado")
        pedido = self.pedidos[id_pedido]
        if pedido['pagado']:
            raise PedidoInvalido("pedido ya fue pagado")
        tot = self.calcular_total(id_pedido, propina_porcentaje)
        pedido['pagado'] = True
        self.recaudacion_total += tot['total']
        mesa_num = pedido['mesa']
        self.liberar_mesa(mesa_num)
        print(f"Pedido {id_pedido} pagado. Total: ${tot['total']:.2f}")
        return tot

    def platos_mas_vendidos(self, n=5):
        ranked = sorted(self._ventas_por_plato.items(), key=lambda x: x[1], reverse=True)
        return [(c, self.menu[c]['nombre'], q) for c,q in ranked[:n]]

def menu_restaurante():
    s = SistemaRestaurante()
    while True:
        print()
        print("="*48)
        print("SISTEMA RESTAURANTE".center(48))
        print("="*48)
        print("1. Mostrar menu")
        print("2. Reservar mesa")
        print("3. Crear pedido (para mesa reservada)")
        print("4. Agregar item a pedido")
        print("5. Pagar pedido")
        print("6. Platos mas vendidos")
        print("0. Volver al menu principal")
        op = input("Elige una opcion: ").strip()

        try:
            if op == "1":
                s.mostrar_menu()
            elif op == "2":
                m = int(input("Numero de mesa: ")); c = int(input("Comensales: "))
                s.reservar_mesa(m, c)
            elif op == "3":
                m = int(input("Numero de mesa: ")); pid = s.crear_pedido(m); print("Pedido:", pid)
            elif op == "4":
                pid = input("ID pedido: "); cod = input("Codigo plato: "); cant = int(input("Cantidad: "))
                s.agregar_item(pid, cod, cant)
            elif op == "5":
                pid = input("ID pedido: "); s.pagar_pedido(pid)
            elif op == "6":
                print("Top platos:", s.platos_mas_vendidos(5))
            elif op == "0":
                break
            else:
                print("Opcion invalida.")
        except Exception as e:
            print("Error:", e)

def demo():
    print()
    print("=== DEMO RESTAURANTE - PASO A PASO ===")
    r = SistemaRestaurante()
    print("1) Reservando mesa 1 para 3 comensales..."); r.reservar_mesa(1,3)
    print("2) Creando pedido en mesa 1..."); pid = r.crear_pedido(1); print("   ID pedido:", pid)
    print("3) Agregando items..."); r.agregar_item(pid, 'R02', 2); r.agregar_item(pid, 'R05', 3)
    print("4) Calculando totales..."); tot = r.calcular_total(pid); print("   Totales:", tot)
    print("5) Pagando..."); pag = r.pagar_pedido(pid); print("   Pago procesado:", pag)
    print("6) Platos mas vendidos:", r.platos_mas_vendidos(5))
    print("Demo restaurante finalizado.")
