"""Interface de terminal do simulador de paginação de memória."""

import sys

from simulador import ResultadoConfiguracao, comparar_tamanhos_pagina

TAMANHOS_PAGINA_KB = (2, 4, 8)


def imprimir_cabecalho() -> None:
    """Apresenta o nome e a proposta do projeto."""
    print("=" * 66)
    print("SIMULADOR DE PAGINAÇÃO DE MEMÓRIA".center(66))
    print("=" * 66)
    print("Este programa compara os tamanhos de página de 2 KB, 4 KB e 8 KB")
    print("e mostra o impacto na memória alocada e na fragmentação interna.")


def ler_inteiro_positivo(mensagem: str) -> int:
    """Lê um inteiro positivo; o prompt aparece só no uso interativo."""
    while True:
        try:
            prompt = mensagem if sys.stdin.isatty() else ""
            valor = int(input(prompt).strip())
        except ValueError:
            print("Entrada inválida. Digite um número inteiro positivo.")
            continue

        if valor <= 0:
            print("O valor deve ser maior que zero. Tente novamente.")
            continue

        return valor


def imprimir_tabela(
    cabecalhos: list[str],
    linhas: list[list[str]],
    alinhamentos: list[str] | None = None,
) -> None:
    """Imprime uma tabela simples, ajustando a largura das colunas."""
    if alinhamentos is None:
        alinhamentos = ["<"] * len(cabecalhos)

    larguras = []
    for indice, cabecalho in enumerate(cabecalhos):
        larguras.append(
            max([len(cabecalho)] + [len(linha[indice]) for linha in linhas])
        )

    def formatar(valores: list[str]) -> str:
        return " | ".join(
            f"{valor:{alinhamentos[indice]}{larguras[indice]}}"
            for indice, valor in enumerate(valores)
        )

    print(formatar(cabecalhos))
    print("-+-".join("-" * largura for largura in larguras))
    for linha in linhas:
        print(formatar(linha))


def imprimir_resultados_processos(resultado: ResultadoConfiguracao) -> None:
    """Mostra os resultados individuais de um tamanho de página."""
    cabecalhos = [
        "Processo",
        "Tamanho (KB)",
        "Páginas",
        "Memória alocada (KB)",
        "Fragmentação interna (KB)",
    ]
    linhas = []

    for indice, processo in enumerate(resultado.resultados_processos, start=1):
        linhas.append([
            f"P{indice}",
            str(processo.tamanho_processo_kb),
            str(processo.quantidade_paginas),
            str(processo.memoria_alocada_kb),
            str(processo.fragmentacao_interna_kb),
        ])

    imprimir_tabela(cabecalhos, linhas, ["<", ">", ">", ">", ">"])


def imprimir_comparacao(resultados: list[ResultadoConfiguracao]) -> None:
    """Mostra a tabela comparativa entre os tamanhos de página."""
    cabecalhos = [
        "Tamanho da página (KB)",
        "Total de páginas",
        "Memória utilizada (KB)",
        "Memória alocada (KB)",
        "Fragmentação interna (KB)",
        "Aproveitamento (%)",
    ]
    linhas = []

    for resultado in resultados:
        linhas.append([
            str(resultado.tamanho_pagina_kb),
            str(resultado.total_paginas),
            str(resultado.memoria_utilizada_kb),
            str(resultado.memoria_total_alocada_kb),
            str(resultado.fragmentacao_interna_total_kb),
            f"{resultado.aproveitamento_percentual:.2f}",
        ])

    imprimir_tabela(cabecalhos, linhas, [">", ">", ">", ">", ">", ">"])


def main() -> None:
    """Solicita os dados, executa a simulação e apresenta os resultados."""
    imprimir_cabecalho()

    try:
        quantidade_processos = ler_inteiro_positivo(
            "\nQuantidade de processos: "
        )

        print("\nInforme o tamanho de cada processo em KB.")
        tamanhos_processos_kb = []
        for indice in range(1, quantidade_processos + 1):
            tamanho = ler_inteiro_positivo(
                f"Tamanho do processo {indice} (KB): "
            )
            tamanhos_processos_kb.append(tamanho)
    except (KeyboardInterrupt, EOFError):
        print("\n\nExecução encerrada pelo usuário.")
        return

    resultados = comparar_tamanhos_pagina(
        tamanhos_processos_kb,
        TAMANHOS_PAGINA_KB,
    )

    print("\n" + "=" * 66)
    print("RESULTADOS INDIVIDUAIS POR TAMANHO DE PÁGINA")
    print("=" * 66)

    for resultado in resultados:
        print(f"\nPáginas de {resultado.tamanho_pagina_kb} KB:")
        imprimir_resultados_processos(resultado)

    print("\n" + "=" * 66)
    print("TABELA COMPARATIVA GERAL")
    print("=" * 66)
    print()
    imprimir_comparacao(resultados)

    melhor_resultado = max(
        resultados,
        key=lambda resultado: resultado.aproveitamento_percentual,
    )
    print(
        "\nMaior aproveitamento: páginas de "
        f"{melhor_resultado.tamanho_pagina_kb} KB "
        f"({melhor_resultado.aproveitamento_percentual:.2f}%)."
    )


if __name__ == "__main__":
    main()
