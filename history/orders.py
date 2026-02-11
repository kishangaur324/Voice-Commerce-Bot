from datetime import datetime
import uuid

class OrderHistory:
    def __init__(self):
        self.orders = []

    def add_order(self, product_name, quantity, price):
        order = {
            "order_id": str(uuid.uuid4())[:8],
            "product_name": product_name,
            "quantity": quantity,
            "price": price,
            "timestamp": datetime.now().isoformat(timespec="seconds")
        }
        self.orders.append(order)
        return order

    def get_all_orders(self):
        return self.orders

    def is_empty(self):
        return len(self.orders) == 0
