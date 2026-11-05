# Simulador de Paginação de Memória

Simulador acadêmico em Python que compara os tamanhos de página de **2 KB, 4 KB e 8 KB** e mostra o impacto dessa escolha na memória alocada, na fragmentação interna e no aproveitamento da memória.

**Autor:** João Pedro Fernandes de Lima
**Licença:** MIT — consulte o arquivo [LICENSE](LICENSE).

## Objetivo acadêmico

Este projeto foi desenvolvido como trabalho da disciplina de **Sistemas Operacionais**. O objetivo é demonstrar, por meio de uma simulação determinística, como o tamanho da página influencia o uso da memória em um sistema com paginação.

A simulação permite observar a relação de compromisso (*trade-off*) do gerenciamento de memória: páginas menores reduzem a fragmentação interna, mas aumentam a quantidade de páginas necessárias; páginas maiores fazem o contrário.

## Conceito de paginação

Na paginação, o espaço de endereçamento de um processo é dividido em blocos de tamanho fixo chamados **páginas**. A memória física é dividida em blocos do mesmo tamanho, chamados **molduras** (*frames*). Uma tabela de páginas associa cada página do processo a uma moldura livre na memória física.

Como o processo pode não ocupar a última página por completo, o espaço restante é desperdiçado. Esse desperdício é chamado de **fragmentação interna**. Ele depende diretamente do tamanho da página e da forma como os processos são dimensionados.

## Funcionamento da simulação

1. O programa solicita a quantidade de processos.
2. Para cada processo, solicita o tamanho em KB (número inteiro positivo).
3. Executa automaticamente a simulação para os três tamanhos de página: 2 KB, 4 KB e 8 KB.
4. Para cada processo e cada tamanho de página, calcula:
   - quantidade de páginas necessárias;
   - memória alocada;
   - fragmentação interna.
5. Exibe os resultados individuais de cada processo.
6. Exibe uma tabela comparativa geral com os totais e o aproveitamento percentual de cada configuração.
7. Indica qual configuração apresentou o maior aproveitamento.

Entradas inválidas (texto, números decimais, zero ou valores negativos) são rejeitadas com uma mensagem em português, e o programa solicita o valor novamente sem ser encerrado.

## Métricas e fórmulas

Sejam:

| Símbolo | Significado |
|---|---|
| `T` | Tamanho do processo em KB |
| `S` | Tamanho da página em KB |
| `P` | Quantidade de páginas do processo |
| `Ma` | Memória alocada para o processo |
| `Mu` | Memória efetivamente utilizada pelo processo |
| `Fi` | Fragmentação interna |
| `A` | Aproveitamento percentual |

As fórmulas utilizadas são:

```text
P  = ceil(T / S)
Ma = P * S
Mu = T
Fi = Ma - T
A  = (Mu / Ma) * 100
```

No código, o arredondamento para cima é feito com aritmética inteira, sem ponto flutuante:

```text
P = (T + S - 1) // S
```

Os totais de uma configuração são obtidos somando os valores de todos os processos:

```text
Total de páginas        = soma de P
Memória utilizada       = soma de T
Memória total alocada   = soma de Ma
Fragmentação total      = Memória total alocada - Memória utilizada
Aproveitamento total    = (Memória utilizada / Memória total alocada) * 100
```

O aproveitamento é calculado sem arredondamento e arredondado para duas casas decimais apenas na apresentação.

## Estrutura do projeto

```text
simulador-paginacao/
├── main.py                  # Interface de terminal: entrada e apresentação
├── simulador.py             # Lógica de cálculo e validações
├── exemplos/
│   ├── entrada.txt          # Exemplo de entrada
│   └── saida_esperada.txt   # Saída de referência para essa entrada
├── tests/
│   └── test_simulador.py    # Testes automatizados com unittest
├── README.md
├── LICENSE
└── .gitignore
```

- `main.py` não realiza cálculos: apenas lê os dados, chama `simulador.py` e formata a saída.
- `simulador.py` concentra as funções de cálculo e a validação dos dados.
- `tests/test_simulador.py` verifica cálculos individuais, totais, os três tamanhos de página e entradas inválidas.

## Requisitos

- **Python 3.10 ou superior** (o projeto usa type hints modernos, como `list[str]` e `str | None`).
- Nenhuma biblioteca externa é necessária. São usados apenas recursos da biblioteca padrão (`dataclasses`, `unittest` e `sys`).
- Terminal para execução interativa.

## Como executar o programa

Na raiz do projeto, execute:

```bash
python3 main.py
```

Em sistemas em que o comando `python` aponta para o Python 3, também é possível usar:

```bash
python main.py
```

Para executar com a entrada de exemplo por redirecionamento:

```bash
python3 main.py < exemplos/entrada.txt
```

Quando a entrada é redirecionada, os prompts de digitação são omitidos; o programa imprime diretamente os resultados. O arquivo [`exemplos/saida_esperada.txt`](exemplos/saida_esperada.txt) corresponde exatamente a essa execução.

## Como executar os testes

Na raiz do projeto:

```bash
python3 -m unittest discover -s tests -v
```

Se o comando `python` estiver disponível e apontar para o Python 3:

```bash
python -m unittest discover -s tests -v
```

## Exemplo de entrada

O arquivo [`exemplos/entrada.txt`](exemplos/entrada.txt) contém:

```text
3
10
18
25
```

A primeira linha indica a quantidade de processos (3), e as linhas seguintes indicam os tamanhos dos processos em KB: 10 KB, 18 KB e 25 KB.

## Exemplo de saída

A saída completa de referência está em [`exemplos/saida_esperada.txt`](exemplos/saida_esperada.txt). A tabela comparativa gerada é:

```text
Tamanho da página (KB) | Total de páginas | Memória utilizada (KB) | Memória alocada (KB) | Fragmentação interna (KB) | Aproveitamento (%)
-----------------------+------------------+------------------------+----------------------+---------------------------+-------------------
                     2 |               27 |                     53 |                   54 |                         1 |              98.15
                     4 |               15 |                     53 |                   60 |                         7 |              88.33
                     8 |                9 |                     53 |                   72 |                        19 |              73.61
```

Interpretação: com páginas de 2 KB, a memória alocada é 54 KB e apenas 1 KB é desperdiçado (98,15% de aproveitamento). Com páginas de 8 KB, a memória alocada sobe para 72 KB e o desperdício para 19 KB (73,61% de aproveitamento). Nesse exemplo, as páginas menores tiveram melhor aproveitamento.

## Limitações e hipóteses

- A simulação considera apenas a **fragmentação interna**; a fragmentação externa não se aplica ao modelo de paginação.
- O custo da tabela de páginas, da TLB e o tempo de acesso à memória **não** são contabilizados. Na prática, páginas menores exigem mais entradas na tabela de páginas.
- Não há limite de memória física: todos os processos são alocados simultaneamente, sem faltas de página, substituição de páginas ou swapping.
- Os tamanhos dos processos são inteiros em KB, sem valores fracionários.
- Os tamanhos de página são fixos em 2 KB, 4 KB e 8 KB.
- Cada processo é tratado de forma independente; não há concorrência, escalonamento ou compartilhamento de memória.
- O programa é determinístico: a mesma entrada sempre produz a mesma saída.
