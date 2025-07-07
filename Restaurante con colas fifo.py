from collections import deque

# Clase base de ítems
class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def get_price(self):
        return self.price

# Clases de bebidas
class Cafe(MenuItem):
    def __init__(self):
        super().__init__("Cafe", 2.0)

    def get_price(self, tiene_plato_principal=False):
        return 2.0 * 0.9 if tiene_plato_principal else 2.0

class Agua(MenuItem):
    def __init__(self):
        super().__init__("Agua", 1.0)

    def get_price(self, tiene_plato_principal=False):
        return 1.0 * 0.9 if tiene_plato_principal else 1.0

class CocaCola(MenuItem):
    def __init__(self):
        super().__init__("Coca Cola", 1.5)

    def get_price(self, tiene_plato_principal=False):
        return 1.5 * 0.9 if tiene_plato_principal else 1.5

# Comidas
class Hamburguesa(MenuItem):
    def __init__(self):
        super().__init__("Hamburguesa", 7.5)

class Pizza(MenuItem):
    def __init__(self):
        super().__init__("Pizza", 9.0)

class Ensalada(MenuItem):
    def __init__(self):
        super().__init__("Ensalada Cesar", 4.0)

class TacosVegetarianos(MenuItem):
    def __init__(self):
        super().__init__("Tacos Vegetarianos", 6.5)

class Lasagna(MenuItem):
    def __init__(self):
        super().__init__("Lasagna", 8.0)

class Postre(MenuItem):
    def __init__(self):
        super().__init__("Pastel de Chocolate", 4.5)

# Clase de ordenes
class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def has_main_course(self):
        principales = ["Hamburguesa", "Pizza", "Ensalada Cesar", "Tacos Vegetarianos", "Lasagna"]
        return any(item.name in principales for item in self.items)

    def count_beverages(self):
        bebidas = ["Cafe", "Agua", "Coca Cola"]
        return sum(1 for item in self.items if item.name in bebidas)

    def calculate_total(self):
        total = 0
        tiene_principal = self.has_main_course()
        for item in self.items:
            if item.name in ["Cafe", "Agua", "Coca Cola"]:
                total += item.get_price(tiene_principal)
            else:
                total += item.get_price()
        return total

    def apply_discount(self):
        subtotal = self.calculate_total()
        cantidad = len(self.items)
        bebidas = self.count_beverages()

        if cantidad > 10:
            total = subtotal * 0.8
        elif cantidad >= 5:
            total = subtotal * 0.9
        else:
            total = subtotal

        if bebidas > 3:
            total *= 0.95
        return total

    def show_order_summary(self):
        print(f"\n--- ORDEN #{self.order_id} ---")
        for item in self.items:
            print(f"- {item.name}: ${item.price}")
        print(f"Subtotal: ${self.calculate_total():.2f}")
        print(f"Total: ${self.apply_discount():.2f}")

# Manejo FIFO
class RestaurantSystem:
    def __init__(self):
        self.orders_queue = deque()
        self.next_order_id = 1

    def create_order(self):
        orden = Order(self.next_order_id)
        self.next_order_id += 1
        return orden

    def add_order_to_queue(self, order):
        self.orders_queue.append(order)
        print(f"Orden #{order.order_id} agregada a la cola")

    def process_next_order(self):
        if self.orders_queue:
            orden = self.orders_queue.popleft()
            print(f"Procesando orden #{orden.order_id}")
            return orden
        else:
            print("No hay ordenes pendientes")
            return None

    def show_queue_status(self):
        print(f"\nOrdenes en cola: {len(self.orders_queue)}")
        for i, orden in enumerate(self.orders_queue, 1):
            print(f"  {i}. Orden #{orden.order_id} ({len(orden.items)} items)")

# Pago
class Payment:
    def __init__(self, order, method):
        self.order = order
        self.method = method

    def process_payment(self):
        total = self.order.apply_discount()
        print(f"\nPago de ${total:.2f} con {self.method}")
        print("Pago completado!")

# Programa principal
def main():
    restaurante = RestaurantSystem()

    orden1 = restaurante.create_order()
    orden1.add_item(Cafe())
    orden1.add_item(Hamburguesa())
    orden1.add_item(CocaCola())
    restaurante.add_order_to_queue(orden1)

    orden2 = restaurante.create_order()
    orden2.add_item(TacosVegetarianos())
    orden2.add_item(Agua())
    orden2.add_item(Ensalada())
    restaurante.add_order_to_queue(orden2)

    restaurante.show_queue_status()

    print("\n=== PROCESANDO ORDENES ===")
    while restaurante.orders_queue:
        actual = restaurante.process_next_order()
        if actual:
            actual.show_order_summary()
            pago = Payment(actual, "tarjeta")
            pago.process_payment()
            print("-" * 30)

if __name__ == "__main__":
    main()
