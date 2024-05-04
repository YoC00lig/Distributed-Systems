from generated import shopping_pb2, shopping_pb2_grpc 
import grpc
from Constants import SHOPS, CITIES, SALE_TYPES, PINK, BLUE, RED
from concurrent import futures
import random
import time
import os

class SaleInformerServer:
    def __init__(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        shopping_pb2_grpc.add_SaleInformerServicer_to_server(self, self.server)
        self.port = os.environ.get("SERVER_PORT", "50051")
        self.server.add_insecure_port('[::]:' + self.port)

    def start(self):
        self.server.start()
        print(f"{PINK}Server started, listening on " + self.port)
        self.server.wait_for_termination()

    def stop(self):
        self.server.stop(0)

    def Subscribe(self, request, context):
        print(f"{BLUE}Subscription (peer: {context.peer()})")
        if any(city not in CITIES for city in request.cities):
            context.set_details(f"{RED}One or more cities do not exist")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return

        while context.is_active():
            for city in request.cities:
                sale_event = self._generate_sale_event(city)
                if sale_event:
                    yield sale_event
                    print(f"{BLUE}Sent notification for {city}, peer: {context.peer()}")
            time.sleep(random.randint(5, 15))

    def _generate_sale_event(self, city):
        if city not in CITIES:
            return None
        sale_event = shopping_pb2.SaleEvent(city=city, sale_type=random.choice(SALE_TYPES))
        sale_event.shop_name = f"{random.choice(SHOPS)} in {city}"
        sale_event.details.extend([self._generate_sale_details() for _ in range(random.randint(1, 5))])
        return sale_event

    def _generate_sale_details(self):
        details = shopping_pb2.SaleDetails()
        details.product_name = f"Product {random.randint(1, 5)}"
        details.original_price = round(random.uniform(10.0, 100.0), 2)
        details.sale_price = round(details.original_price * random.uniform(0.5, 0.9), 2)
        details.end_time = int(time.time() + random.randint(3600, 86400))
        return details

if __name__ == '__main__':
    server = SaleInformerServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()