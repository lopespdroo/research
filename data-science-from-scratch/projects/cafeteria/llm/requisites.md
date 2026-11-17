# O que o programa deve fazer

Gerar logs falsos de pedidos de uma cafeteria, interpretá-los e imprimir um relatório com estatísticas.

## Requisitos

1. Geração dos dados

- Use random.seed(42) para o resultado ser reproduzível.
- Gere 40 linhas no formato "2025-03-14 | ana | latte 2x | 9.50". Os clientes e itens devem ficar em listas, e os preços em um dicionário.
- Insira 3 linhas propositalmente malformadas, escolhidas com random.sample.
- Junte tudo em uma única string multilinha e use random.shuffle na lista antes do join.

2. Modelagem

- Crie uma classe Pedido com __init__, __repr__ e um método total().

3. Parsing

- Escreva parse_linha(linha: str) -> Pedido usando re.match com grupos de captura. Ela deve lançar ValueError se a linha não bater.
- Escreva um generator pedidos_validos(texto) que percorre as linhas, usa try/except, faz yield dos pedidos válidos e conta os erros.

4. Análises

- Counter com os 3 itens mais vendidos (most_common).
- defaultdict(list) com os pedidos agrupados por cliente e defaultdict(float) com a receita por cliente.
- Dois sets de clientes (quem pediu café e quem pediu bolo), mostrando interseção e diferença.
- Ranking dos clientes por receita usando sorted com key=lambda e reverse=True, impresso com enumerate.
- Uma list comprehension (pedidos acima de R$ 20) e uma dict comprehension (cliente → número de pedidos).

5. Estrutura

- Código organizado em funções, com indentação correta e if __name__ == "__main__": para rodar o relatório.
- Docstrings curtas nas funções principais.
