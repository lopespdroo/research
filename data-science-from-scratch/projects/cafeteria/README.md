# Mini Report-System of a Cafeteria

To consolidate my understanding of the chapter I just finished reading, I decided to build a quick, small project using some of the things I learned in the book.

I prompted a LLM to give me a quick project idea that would let me practice the concepts adressed in the begginig of the book. You can find the prompt and the response in the [`llm`](data-science-from-scratch/projects/cafeteria/lmm) directory. I asked for two files: one describing the scene of the project and one listing the concepts I should use while building it. On this pange I only cover the scenario file.

## The scenario

I work for a small cafeteria. The cash register records every order as a line of text, and at the end of the day everything is dumped into a log file. The owner wants a simple report that answers questions lile: *what do we sell the most? who are our best costumers?*

The catch: the log is messy because lines arrive out of order and some of them are corrupted.

The program does two things: it simulates that log, and then analyzes what was generated.

```
simulate -> parse -> analyze -> report
```

## What the project should do 

## Part 1: Generating logs

Since there is no real log, the program fabicrates one.

- 5 costumers, 6 menus items, each item with a fixed price. The menu includes both coffe items and cake items (since I prompted the llm in my native language, the code has some things translated to brazilian portuguese).
- Each line is one order.
- 40 valid lines are generated in this format:

```
2025-03-14 | ana | latte 2x | 9.50
```

(`date | costumer | item quantityx | total`)

- 3 lines are deliberately corrupted (it has missing fields)
- All 43 log lines are shuffled and joined into a single multiline string, as if it came from a `.txt` file.

## Part 2: Read the log

- Each valid line becomes an `Order` object (costumer, item, quantity, price).
- Each invalid line is discarded without crashing the program.
- Parsing is done line by line, yielding orders as they are validated instead of building one giant list up front.

## Part 3: Answer the owner's questions

The final report answers, in this order:

1. **Best sellers:** the top 3 items by units sold
2. **Best costumers:** ranking of costumers by total revenue, from highest to lowest.
3. **Comsuption profile:** which costumers orderde coffe but **never** donut.
4. **Reliability:** did the program's own automated check pass?

Besides the main report, the program also computes a few supporting results: orders grouped by costumer, number of orders per costumer and orders above R$ 20.

## Rules

- Running the program should produce **exactly the same report** everytime (because `random()` uses a fixed seed).
- An invalid line never interrupts execution.
- Standard library only.

## Running it

```bash
python3 app.py
```


