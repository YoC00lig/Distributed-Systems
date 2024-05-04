from generated import shopping_pb2

PINK = '\033[38;2;255;20;147m'  
DEFAULT = '\033[0m'
GREEN = '\033[38;2;0;255;0m'  
RED = '\033[38;2;255;0;0m'  
BLUE = '\033[38;2;0;0;255m'
ORANGE = '\033[38;2;255;165;0m' 

CITIES = ["Cracow", "Hongkong", "London", "Toronto", "Paris", "New York", "Tokio"]
SHOPS = ['SuperSale', 'Louis Vuitton', 'DiscountMart', 'OLX', 'GUESS', 'Zooplus', 'BargainEmporium', 'Amazon', 'Allegro']
SALE_TYPES = [shopping_pb2.DISCOUNT, shopping_pb2.CLEARANCE, shopping_pb2.FLASH_SALE]