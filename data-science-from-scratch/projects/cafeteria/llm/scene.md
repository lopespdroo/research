# O cenário

Você trabalha para uma cafeteria pequena. O sistema de caixa registra cada pedido numa linha de texto e, no fim do dia, joga tudo num arquivo de log. O dono quer um relatório simples para responder perguntas como: o que vendemos mais? quem são nossos melhores clientes? Só que o log é bagunçado: as linhas vêm fora de ordem e algumas estão corrompidas (falha do caixa, erro de digitação).

Seu programa faz duas coisas: simula esse log e depois analisa o que foi gerado.

## Fase 1: Simular o log do dia

Como você não tem um log real, seu programa o fabrica.

### O cardápio e os clientes

Defina cerca de 5 clientes.
Defina cerca de 6 itens, com preço fixo para cada um. Precisa haver itens de café (latte, espresso, cappuccino) e de bolo (bolo de cenoura, bolo de chocolate), porque você vai comparar quem pediu cada categoria.
A forma de decidir isso é escolha sua (por exemplo, pelo nome ou por uma lista separada).

### O pedido
Cada linha representa um pedido de um único cliente, de um único item, com uma quantidade (1 a 3 unidades). O valor da linha é preço × quantidade. Formato:

2025-03-14 | ana | latte 2x | 9.50

Data | cliente | item quantidadex | total.

### Linhas ruins
Depois de gerar as 40 linhas boas, você estraga 3 de propósito (por exemplo: faltando um campo, preço escrito “abc”, quantidade ausente). Elas representam as falhas do caixa. O programa precisa sobreviver a elas, não pode quebrar.

### Embaralhar
O log chega desordenado, então as 43 linhas são misturadas antes de virar um texto único.

Resultado da fase 1: uma grande string, como se você tivesse lido um arquivo .txt.

## Fase 2: Ler o log

Seu programa recebe aquela string e precisa transformá-la em dados utilizáveis.

Cada linha boa vira um objeto Pedido (com cliente, item, quantidade e preço).
Cada linha ruim é descartada sem derrubar o programa, e contada. No final, o relatório diz quantas foram aceitas e quantas rejeitadas (esperado: 40 e 3).
A leitura é feita linha a linha, entregando pedidos conforme valida, em vez de montar uma lista gigante de uma vez.

## Fase 3: Responder às perguntas do dono

O relatório final responde, nesta ordem:

Qualidade do log: quantas linhas válidas e quantas inválidas?
Campeões de venda: quais os 3 itens mais vendidos?
Melhores clientes: ranking de clientes por receita total, do que mais gastou ao que menos gastou.
Perfil de consumo: quais clientes pediram café mas nunca pediram bolo? (ótimo alvo para uma promoção de bolo)
Confiabilidade: as verificações automáticas do próprio programa passaram?

Além do relatório principal, o programa também deve calcular alguns extras que sustentam essas respostas: pedidos agrupados por cliente, quantos pedidos cada cliente fez, quais pedidos passaram de R$ 20, quem pediu café e bolo ao mesmo tempo (interseção), e um pareamento de nomes com totais.
