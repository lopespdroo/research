import random
import re
from collections import defaultdict, Counter
from collections.abc import Iterator
from typing import List, Optional

# - add menu, if possible

# ---- MACROS AND CONFIGURATION ----

random.seed(42)

YEAR: int = 2026
month: int = 1
MAX_LOGS : int = 41

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

#----GENERATING LOGS----

def verify_date(day: int, month: int) -> int:
    """Updates the day of the month. If greater than 31, resets to 1."""
    if day > 31:
        month +=1
        day -= 31

    return day, month


def generator_logs(n: int) -> int:
    for i in range(1, n):
        yield i


def create_log(month: int,
              year: int,
              clients: list[str],
              shop_items: dict[str, float]
             ) -> str:
    """Create log to be added onto the list of orders."""
    for i in generator_logs(MAX_LOGS):
        day = i

        day_safe, month_safe = verify_date(day, month)
        client = random.choice(clients)
        shop_item = random.choice(list(shop_items.keys()))
        qtd = random.randint(1, 3)

        total_price: float = shop_items[shop_item] * qtd

        order = (f"{year}-{month_safe}-{day_safe} | {client} | {shop_item} {qtd}x | {total_price}")

    return order


def create_bad_formatted_log(logs: list[str])-> str:
    """Create a log with an empty space inside."""
    log = str(random.sample(logs, k=1))
    chunks = log.split("|")

    number = random.randint(0, 3)

    for i in range(len(log)):
        if i == number:
            log[i] == " "

    return log


def add_log(order: str, logs: list[str]):
    return logs.append(order)

# ---- VALIDATION AND PARSING

def validate_order(logs: List[str], INVALID_ORDERS: List[str])-> Iterator[Order]:
    """Makes sure if the log is in the good shape and yields the order to a list."""
    for line in logs:
        try:
            order = parse_line(line)
        except ValueError:
            INVALID_ORDERS.append(line)
            continue
        else:
            yield order


def parse_line(line: str)-> Order:
    """Inspect the log line and returns the Order object of it."""
    match = re.match(r"(\d{4}-\d{1,2}-\d{1,2})\s*\|\s*(\w+)\s*\|\s*(.+?)\s+(\d+)x\s*\|\s*(\d+(?:\.\d+)?)", line)
        
    if not match:
        raise ValueError

    date, client, item, qtt, price = match.groups()

    qtt = int(qtt)
    price = float(price)

    order = Order(date, client, item, qtt, price)

    return order

# ---- MAIN ----

def main():
    
    clients: list[str] = ["ana", "bruno", "carla", "diego", "elisa"]
    shop_items: dict[str, float] = {"latte" : 9.50,
                                    "espresso" : 10,
                                    "cappuccino" : 8,
                                    "donut" : 5.50,
                                    "bolo de cenoura" : 13.75,
                                    "bolo de chocolate" : 15.50}

    # ---- LOG GENERATION ----

    logs : list[str] = []

    for i in generator_logs(MAX_LOGS):
        line = create_log(month, YEAR, clients, shop_items)
        add_log(line, logs)

    for i in range(3):
        bad_formatted_log = create_bad_formatted_log(logs)
        add_log(bad_formatted_log, logs)

    random.shuffle(logs)

    # ---- VALIDATION OF LOGS ----

    INVALID_ORDERS: list[str] = []
    ORDERS = list(validate_order(logs, INVALID_ORDERS))

    # ---- TESTS FOR VALIDATION OF LOGS ----

    assert len(logs) == 43
    assert len(ORDERS) == 40
    assert len(INVALID_ORDERS) == 3

    assert len(ORDERS) + len(INVALID_ORDERS) == len(logs)

    assert all(order.client in clients for order in ORDERS)

    assert all(order.item in shop_items for order in ORDERS)

    assert all(1 <= order.qtt <= 3 for order in ORDERS)

    # ---- ANALYSING ----
    sold_items: list[int] = []

    # top three sellers 
    for order in ORDERS:
        sold_items.append(order.item)

    sold_items= Counter(sold_items)

    print(f"Top 3 sellers: {sold_items.most_common(3)}")
    
    print("---------------------")
    # items bought from each client and total revenue gathered from each client
    items_bought_per_client = defaultdict(list)
    revenue_per_client = defaultdict(float)

    for order in ORDERS:
        items_bought_per_client[order.client].append(order.item)
        revenue_per_client[order.client] += order.price

    for client in items_bought_per_client:
        print(f"Items bought from {client}: {items_bought_per_client[client]}")
    
    print("---------------------")

    for client in revenue_per_client:
        print(f"Total revenue from {client.capitalize()}: {revenue_per_client[client]}")

    print("---------------------")
    # sets of clients who bought coffe and donuts separatedly and both together
    coffe_orders = set()
    donut_orders = set()
    coffe_and_donut_orders = set()

    for client in items_bought_per_client:
        if "espresso" in items_bought_per_client[client] or "cappucino" in items_bought_per_client[client] or "latte" in items_bought_per_client[client]:
               coffe_orders.add(client)
        if "donut" in items_bought_per_client[client]:
            donut_orders.add(client)

    for client in clients:
        if client in coffe_orders and client in donut_orders:
            coffe_and_donut_orders.add(client)

    print(f"Clients who bought coffe: {coffe_orders}")
    print(f"Clients who bought donut: {donut_orders}")
    print(f"Clients who bought both: {coffe_and_donut_orders}")

    # ---- TESTS FOR SETS ----
    assert coffe_orders >= coffe_and_donut_orders
    assert donut_orders >= coffe_and_donut_orders

    print("---------------------")
    # clients listed by revenue
    most_to_least_spenders = sorted(revenue_per_client.items(),
                                  key=lambda revenue_per_client:revenue_per_client[1],
                                  reverse=True)

    print("List of clients from who spent the most to who spent the least: ")
    for item in most_to_least_spenders:
        print(item)
    
    print("---------------------")
    # list comprehension for orders above 20
    orders_above_20 = [order.price for order in ORDERS if order.price > 20]
    print(f"List of orders above R$ 20.00: {orders_above_20}")

    print("---------------------")
    # dict comprehension for total number of orders from each client
    total_orders_by_client = {client: sum(order.qtt for order in ORDERS if order.client == client)
                           for client in clients}
    print(f"Number of orders from each client: {total_orders_by_client}")

    print("---------------------")
    print("All tests passed!")

if __name__ == "__main__":
    main()
