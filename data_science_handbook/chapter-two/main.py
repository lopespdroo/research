import random
import regex as re
from collections import defaultdict, Counter

random.seed(42)

clients = ["ana",
           "bruno",
           "carla",
           "diego",
           "elisa"]

shop_items = {"latte" : "9.50",
              "espresso" : "10",
              "cappuccino" : "8",
              "donut" : "5.50",
              "bolo de cenoura" : "13.75",
              "bolo de chocolate" : "15.50"}


