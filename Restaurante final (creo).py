from collections import deque, namedtuple
import json
# Named tuple para los items del menu
MenuSet = namedtuple('MenuSet', ['nombre', 'precio', 'tipo'])

class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def get_price(self):
        return self.price

# Clases para bebidas
class Cafe(MenuItem):
    def __init__(self):
        super().__init__("Cafe", 2.0)
    
    def get_price(self, tiene_plato_principal=False):
        if tiene_plato_principal:
            return 2.0 * 0.9
        return 2.0

class Agua(MenuItem):
    def __init__(self):
        super().__init__("Agua", 1.0)
    
    def get_price(self, tiene_plato_principal=False):
        if tiene_plato_principal:
            return 1.0 * 0.9
        return 1.0

class CocaCola(MenuItem):
    def __init__(self):
        super().__init__("Coca Cola", 1.5)
    
    def get_price(self, tiene_plato_principal=False):
        if tiene_plato_principal:
            return 1.5 * 0.9
        return 1.5

# Clases para comida
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

# Interfaz para manejar el menu
class MenuManager:
    def add_to_menu(self, name, price, category):
        pass
    
    def update_menu_item(self, name, new_price):
        pass
    
    def delete_from_menu(self, name):
        pass
    
    def save_menu(self, filename):
        pass
    
    def load_menu(self, filename):
        pass

# Clase para las ordenes
class Order(MenuManager):
    def __init__(self, order_id):
        self.order_id = order_id
        self.items = []
        self.menu_dict = {}
        
        # Items que usan named tuple
        default_items = [
            MenuSet("Cafe", 2.0, "bebida"),
            MenuSet("Agua", 1.0, "bebida"),
            MenuSet("Coca Cola", 1.5, "bebida"),
            MenuSet("Hamburguesa", 7.5, "plato"),
            MenuSet("Pizza", 9.0, "plato"),
            MenuSet("Ensalada Cesar", 4.0, "plato"),
            MenuSet("Tacos Vegetarianos", 6.5, "plato"),
            MenuSet("Lasagna", 8.0, "plato"),
            MenuSet("Pastel de Chocolate", 4.5, "postre")
        ]
        
        # Aqui se inicializa menu
        for item in default_items:
            self.menu_dict[item.nombre] = {
                'precio': item.precio,
                'tipo': item.tipo
            }
    
    def add_item(self, item):
        self.items.append(item)
    
    # Implementamos los metodos de la interfaz
    def add_to_menu(self, name, price, category):
        self.menu_dict[name] = {'precio': price, 'tipo': category}
        print(f"Se agrego {name} al menu")
    
    def update_menu_item(self, name, new_price):
        if name in self.menu_dict:
            self.menu_dict[name]['precio'] = new_price
            print(f"Se actualizo el precio de {name} a ${new_price}")
        else:
            print(f"No se encontro {name} en el menu")
    
    def delete_from_menu(self, name):
        if name in self.menu_dict:
            del self.menu_dict[name]
            print(f"Se elimino {name} del menu")
        else:
            print(f"No se encontro {name} en el menu")
    
    def save_menu(self, filename):
        try:
            with open(filename, 'w') as f:
                json.dump(self.menu_dict, f, indent=2)
            print(f"Menu guardado en {filename}")
        except Exception as e:
            print(f"Error al guardar: {e}")
    
    def load_menu(self, filename):
        try:
            with open(filename, 'r') as f:
                self.menu_dict = json.load(f)
            print(f"Menu cargado desde {filename}")
        except FileNotFoundError:
            print(f"No se encontro el archivo {filename}")
        except Exception as e:
            print(f"Error al cargar: {e}")
    
    def show_menu(self):
        print(" MENU ")
        for nombre, info in self.menu_dict.items():
            print(f"{nombre}: ${info['precio']} ({info['tipo']})")
        print()
    
    def has_main_course(self):
        platos_principales = ["Hamburguesa", "Pizza", "Ensalada Cesar", "Tacos Vegetarianos", "Lasagna"]
        for item in self.items:
            if item.name in platos_principales:
                return True
        return False
    
    def count_beverages(self):
        bebidas = ["Cafe", "Agua", "Coca Cola"]
        count = 0
        for item in self.items:
            if item.name in bebidas:
                count += 1
        return count
    
    def calculate_total(self):
        total = 0
        has_main = self.has_main_course()
        
        for item in self.items:
            if item.name in ["Cafe", "Agua", "Coca Cola"]:
                total += item.get_price(has_main)
            else:
                total += item.get_price()
        
        return total
    
    def apply_discount(self):
        subtotal = self.calculate_total()
        item_count = len(self.items)
        beverage_count = self.count_beverages()
        
        # Descuento por cantidad
        if item_count > 10:
            total = subtotal * 0.8
        elif item_count >= 5:
            total = subtotal * 0.9
        else:
            total = subtotal
        
        # Descuento extra por bebidas
        if beverage_count > 3:
            total = total * 0.95
        
        return total
    
    def show_order_summary(self):
        print(f"\n--- ORDEN #{self.order_id} ---")
        for item in self.items:
            print(f"- {item.name}: ${item.price}")
        print(f"Subtotal: ${self.calculate_total():.2f}")
        print(f"Total: ${self.apply_discount():.2f}")

# Sistema principal usando cola FIFO
class RestaurantSystem:
    def __init__(self):
        self.orders_queue = deque()  
        self.next_order_id = 1
    
    def create_order(self):
        new_order = Order(self.next_order_id)
        self.next_order_id += 1
        return new_order
    
    def add_order_to_queue(self, order):
        self.orders_queue.append(order)
        print(f"Orden #{order.order_id} agregada a la cola")
    
    def process_next_order(self):
        if self.orders_queue:
            next_order = self.orders_queue.popleft()  
            print(f"Procesando orden #{next_order.order_id}")
            return next_order
        else:
            print("No hay ordenes pendientes")
            return None
    
    def show_queue_status(self):
        print(f"\nOrdenes en cola: {len(self.orders_queue)}")
        for i, order in enumerate(self.orders_queue, 1):
            print(f"  {i}. Orden #{order.order_id} ({len(order.items)} items)")

class Payment:
    def __init__(self, order, method):
        self.order = order
        self.method = method
    
    def process_payment(self):
        total = self.order.apply_discount()
        print(f"\nPago de ${total:.2f} con {self.method}")
        print("Pago completado!")

def main():
    # Crear sistema
    restaurant = RestaurantSystem()
    
    # Creamos la primera orden
    order1 = restaurant.create_order()
    
    # Mostrar menu
    order1.show_menu()
    
    # Agregamos los items
    order1.add_item(Cafe())
    order1.add_item(Hamburguesa())
    order1.add_item(CocaCola())
    order1.add_item(Pizza())
    order1.add_item(Postre())
    
    # Agregamos la orden ala cola
    restaurant.add_order_to_queue(order1)
    
    # Crear la segunda orden
    order2 = restaurant.create_order()
    order2.add_item(TacosVegetarianos())
    order2.add_item(Agua())
    order2.add_item(Ensalada())
    
    restaurant.add_order_to_queue(order2)
    
    # Podemos ver el estado de cola
    restaurant.show_queue_status()
    
    # Procesamos las ordenes (FIFO)
    print(" PROCESANDO ORDENES ")
    while restaurant.orders_queue:
        current_order = restaurant.process_next_order()
        if current_order:
            current_order.show_order_summary()
            
            # Pago
            payment = Payment(current_order, "tarjeta")
            payment.process_payment()
            print("-" * 30)
    
if __name__ == "__main__":
    main()
