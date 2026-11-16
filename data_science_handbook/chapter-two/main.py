import random
import re
from collections import defaultdict, Counter
from collections.abc import Iterator
from typing import List, Optional

random.seed(42)

#----GENERATING LOGS----
YEAR: int = 2026
month: int = 1

def verifyDayAndMonth(day: int, month: int) -> int:
    """Updates the day of the month. If greater than 31, resets to 1."""
    if day > 31:
        month +=1
        day -= 31

    return day, month

logs : list[str] = []
MAX_LOGS : int = 41

def maxLogsGenerator(n: int) -> int:
    for i in range(1, n):
        yield i

def createLog(month: int, year: int, clients: list[str], shop_items_keys: list[str], shop_items: list[str]) -> str:
    """Create log to be added onto the list of orders."""
    for i in maxLogsGenerator(MAX_LOGS):
        day: int = i

        day_safe, month_safe = verifyDayAndMonth(day, month)
        client: str = random.choice(clients)
        shop_item: str = random.choice(shop_items_keys)
        qtd: int = random.randint(1, 3)
        shop_item_multiplied: float = shop_items[shop_item] * qtd

        order: str = (f"{year}-{month_safe}-{day_safe} | {client} | {shop_item} {qtd}x | {shop_item_multiplied}")

    return order

def createBadFormattedLog(logs: list[str])-> str:
    """Create a log with an empty space inside."""
    log = str(random.sample(logs, k=1))
    chunks = log.split("|")

    number = random.randint(0, 3)

    for i in range(len(log)):
        if i == number:
            log[i] == " "

    return log

def addLog(order: str, logs: list[str]):
    return logs.append(order)

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

def validateOrder(logs: List[str], INVALID_ORDERS: List[str])-> Iterator[Order]:
    """Makes sure if the log is in the good shape and yields the order to a list."""
    for line in logs:
        try:
            order = parseLine(line)
        except ValueError:
            INVALID_ORDERS.append(line)
            continue
        else:
            yield order

def parseLine(line: str)-> Order:
    """Inspect the log line and returns the Order object of it."""
    match = re.match(r"(\d{4}-\d{1,2}-\d{1,2})\s*\|\s*(\w+)\s*\|\s*(.+?)\s+(\d+)x\s*\|\s*(\d+(?:\.\d+)?)", line)
        
    if not match:
        raise ValueError

    date, client, item, qtt, price = match.groups()

    qtt = int(qtt)
    price = float(price)

    order = Order(date, client, item, qtt, price)

    return order

def main():
    
    clients: list[str] = ["ana", "bruno", "carla", "diego", "elisa"]
    shop_items: dict[str, float] = {"latte" : 9.50,
                                    "espresso" : 10,
                                    "cappuccino" : 8,
                                    "donut" : 5.50,
                                    "bolo de cenoura" : 13.75,
                                    "bolo de chocolate" : 15.50}
    shop_items_keys: list[str] = list(shop_items.keys())

    for i in maxLogsGenerator(MAX_LOGS):
        line = createLog(month, YEAR, clients, shop_items_keys, shop_items)
        addLog(line, logs)

    for i in range(3):
        badFormattedLog = createBadFormattedLog(logs)
        addLog(badFormattedLog, logs)

    random.shuffle(logs)

    INVALID_ORDERS = []
    ORDERS = list(validateOrder(logs, INVALID_ORDERS))

    #----ANALYSING----
    soldItems: list[int] = []

    #top three sellers 
    for order in ORDERS:
        soldItems.append(order.item)

    soldItems = Counter(soldItems)

    print(f"Top 3 sellers: {soldItems.most_common(3)}")
    
    print("---------------------")
    #items bought from each client and total revenue gathered from each client
    itemsBoughtPerClient = defaultdict(list)
    revenuePerClient = defaultdict(float)

    for order in ORDERS:
        itemsBoughtPerClient[order.client].append(order.item)
        revenuePerClient[order.client] += order.price

    for client in itemsBoughtPerClient:
        print(f"Items bought from {client}: {itemsBoughtPerClient[client]}")
    
    print("---------------------")

    for client in revenuePerClient:
        print(f"Total revenue from {client.capitalize()}: {revenuePerClient[client]}")

    print("---------------------")
    #sets of clients who bought coffe and donuts separatedly and both together
    coffeOrders = set()
    donutOrders = set()
    coffeAndDonutOrders = set()

    for client in itemsBoughtPerClient:
        if "espresso" in itemsBoughtPerClient[client] or "cappucino" in itemsBoughtPerClient[client] or "latte" in itemsBoughtPerClient[client]:
               coffeOrders.add(client)
        if "donut" in itemsBoughtPerClient[client]:
            donutOrders.add(client)

    for client in clients:
        if client in coffeOrders and client in donutOrders:
            coffeAndDonutOrders.add(client)

    print(f"Clients who bought coffe: {coffeOrders}")
    print(f"Clients who bought donut: {donutOrders}")
    print(f"Clients who bought both: {coffeAndDonutOrders}")

    print("---------------------")
    #clients listed by revenue
    mostSpenderstoLeastSpenders = sorted(revenuePerClient.items(),
                                  key=lambda revenuePerClient:revenuePerClient[1],
                                  reverse=True)

    print("List of clients from who spent the most to who spent the least: ")
    for item in mostSpenderstoLeastSpenders:
        print(item)
    
    print("---------------------")
    #list comprehension for orders above 20
    ordersAbove20 = [order.price for order in ORDERS if order.price > 20]
    print(f"List of orders above R$ 20.00: {ordersAbove20}")

    print("---------------------")
    #dict comprehension for total number of orders from each client
    totalOrdersByClient = {client: sum(order.qtt for order in ORDERS if order.client == client)
                           for client in clients}
    print(f"Number of orders from each client: {totalOrdersByClient}")

if __name__ == "__main__":
    main()
