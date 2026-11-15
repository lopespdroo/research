import random
import re
from collections import defaultdict, Counter
from collections.abc import Iterator
from typing import List, Optional

random.seed(42)

#----GENERATING LOGS----

year: int = 2026
month: int = 1

def verify_day_and_month(day: int, month: int) -> int:
    """updates the day of the month. if greater than 31, resets to 1"""
    if day <= 31:
        pass
    else:
        month += 1
        day -= 31

    return day, month

unprocessed_orders: list[str] = []
max_unprocessed_orders: int = 41

def generate_max_unprocessed_orders(n: int) -> int:
    """number generator for function"""
    for i in range(1, n):
        yield i

def create_unprocessed_order(month: int, year: int, clients: list[str], shop_items_keys: list[str], shop_items: list[str]) -> str:
    """create order to be added onto the list of orders"""
    
    for i in generate_max_unprocessed_orders(max_unprocessed_orders):
        day: int = i
        day_safe : int
        month_safe : int

        day_safe, month_safe = verify_day_and_month(day, month)
        client: str = random.choice(clients)
        shop_item: str = random.choice(shop_items_keys)
        qtd: int = random.randint(1, 3)
        shop_item_multiplied: float = shop_items[shop_item] * qtd

        order: str = (f"{year}-{month_safe}-{day_safe} | {client} | {shop_item} {qtd}x | {shop_item_multiplied}")

        add_unprocessed_order(order, unprocessed_orders)

    return

def add_unprocessed_order(order: str, unprocessed_orders: list[str]):
    return unprocessed_orders.append(order)

#----MODELLING----

class Order():
    
    def __init__(self, date, client, item, qtt, price):
        self.date = date
        self.client = client
        self.item = item
        self.qtt = qtt
        self.price = price

    def __repr__(self):
        return f"Order(date={self.date!r},(client={self.client!r}, (item={self.item!r}, (qtt={self.qtt!r}, (price={self.price})"

def valid_orders(unprocessed_orders : List[str], not_valid_orders: List[str])-> Iterator[Order]:
    for line in unprocessed_orders:
        try:
            order = parse_line(line)
        except ValueError:
            not_valid_orders.append(line)
            continue
        else:
            yield order

def parse_line(line: str)-> Order:
    match = re.match(r"(\d{4}-\d{1,2}-\d{1,2})\s*\|\s*(\w+)\s*\|\s*(.+?)\s+(\d+)x\s*\|\s*(\d+(?:\.\d+)?)", line)
        
    if not match:
        raise ValueError

    date, client, item, qtt, price = match.groups()

    qtt = int(qtt)
    price = float(price)

    order = Order(date, client, item, qtt, price)

    return order

def main():
    clients: list[str] = ["ana",
                          "bruno",
                          "carla",
                          "diego",
                          "elisa"]

    shop_items: dict[str, float] = {"latte" : 9.50,
                                    "espresso" : 10,
                                    "cappuccino" : 8,
                                    "donut" : 5.50,
                                    "bolo de cenoura" : 13.75,
                                    "bolo de chocolate" : 15.50}
    shop_items_keys: list[str] = list(shop_items.keys())

    create_unprocessed_order(month, year, clients, shop_items_keys, shop_items)

    #REFACTOR THIS LATER
    #from here
    bad_format_str1: str = "2026-2-11 | | bolo de chocolate 1x | 15.50"
    bad_format_str2: str = "2026-2-12 |  |  | 8"
    bad_format_str3: str = " | diego | 123 | sete"

    add_unprocessed_order(bad_format_str1, unprocessed_orders)
    add_unprocessed_order(bad_format_str2, unprocessed_orders)
    add_unprocessed_order(bad_format_str3, unprocessed_orders)
    #to here

    random.shuffle(unprocessed_orders)

    not_valid_orders = []
    pedidos = list(valid_orders(unprocessed_orders, not_valid_orders))

if __name__ == "__main__":
    main()
