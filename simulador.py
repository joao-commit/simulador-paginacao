"""Cálculos da simulação de paginação de memória.

Este módulo contém apenas a lógica de cálculo. Não lê entradas nem
imprime resultados; essas responsabilidades ficam para o main.py.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ResultadoProcesso:
    """Resultado da alocação de um único processo."""

    tamanho_processo_kb: int
    tamanho_pagina_kb: int
    quantidade_paginas: int
    memoria_alocada_kb: int
    fragmentacao_interna_kb: int


@dataclass(frozen=True)
class ResultadoConfiguracao:
    """Resultado da simulação para um tamanho de página."""

    tamanho_pagina_kb: int
    resultados_processos: list[ResultadoProcesso]
    total_paginas: int
    memoria_utilizada_kb: int
    memoria_total_alocada_kb: int
    fragmentacao_interna_total_kb: int
    aproveitamento_percentual: float


def validar_inteiro_positivo(valor: int, descricao: str) -> None:
    """Garante que um valor seja um inteiro maior que zero."""
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise ValueError(f"{descricao} deve ser um número inteiro.")
    if valor <= 0:
        raise ValueError(f"{descricao} deve ser maior que zero.")


def validar_tamanhos_processos(tamanhos_processos_kb: list[int]) -> None:
    """Garante que a lista de processos não esteja vazia e seja válida."""
    if not tamanhos_processos_kb:
        raise ValueError("A lista de tamanhos de processos não pode estar vazia.")

    for tamanho_processo_kb in tamanhos_processos_kb:
        validar_inteiro_positivo(tamanho_processo_kb, "O tamanho de cada processo")


def calcular_resultado_processo(
    tamanho_processo_kb: int,
    tamanho_pagina_kb: int,
) -> ResultadoProcesso:
    """Calcula páginas, memória alocada e fragmentação de um processo."""
    validar_inteiro_positivo(tamanho_processo_kb, "O tamanho do processo")
    validar_inteiro_positivo(tamanho_pagina_kb, "O tamanho da página")

    quantidade_paginas = (
        tamanho_processo_kb + tamanho_pagina_kb - 1
    ) // tamanho_pagina_kb
    memoria_alocada_kb = quantidade_paginas * tamanho_pagina_kb
    fragmentacao_interna_kb = memoria_alocada_kb - tamanho_processo_kb

    return ResultadoProcesso(
        tamanho_processo_kb=tamanho_processo_kb,
        tamanho_pagina_kb=tamanho_pagina_kb,
        quantidade_paginas=quantidade_paginas,
        memoria_alocada_kb=memoria_alocada_kb,
        fragmentacao_interna_kb=fragmentacao_interna_kb,
    )


def simular_tamanho_pagina(
    tamanhos_processos_kb: list[int],
    tamanho_pagina_kb: int,
) -> ResultadoConfiguracao:
    """Simula todos os processos para um único tamanho de página."""
    validar_tamanhos_processos(tamanhos_processos_kb)
    validar_inteiro_positivo(tamanho_pagina_kb, "O tamanho da página")

    resultados_processos = [
        calcular_resultado_processo(tamanho_processo_kb, tamanho_pagina_kb)
        for tamanho_processo_kb in tamanhos_processos_kb
    ]

    total_paginas = sum(
        resultado.quantidade_paginas for resultado in resultados_processos
    )
    memoria_utilizada_kb = sum(tamanhos_processos_kb)
    memoria_total_alocada_kb = sum(
        resultado.memoria_alocada_kb for resultado in resultados_processos
    )
    fragmentacao_interna_total_kb = (
        memoria_total_alocada_kb - memoria_utilizada_kb
    )
    aproveitamento_percentual = (
        memoria_utilizada_kb / memoria_total_alocada_kb
    ) * 100

    return ResultadoConfiguracao(
        tamanho_pagina_kb=tamanho_pagina_kb,
        resultados_processos=resultados_processos,
        total_paginas=total_paginas,
        memoria_utilizada_kb=memoria_utilizada_kb,
        memoria_total_alocada_kb=memoria_total_alocada_kb,
        fragmentacao_interna_total_kb=fragmentacao_interna_total_kb,
        aproveitamento_percentual=aproveitamento_percentual,
    )


def comparar_tamanhos_pagina(
    tamanhos_processos_kb: list[int],
    tamanhos_paginas_kb: tuple[int, ...] = (2, 4, 8),
) -> list[ResultadoConfiguracao]:
    """Simula os processos para cada tamanho de página informado."""
    validar_tamanhos_processos(tamanhos_processos_kb)

    if not tamanhos_paginas_kb:
        raise ValueError("A lista de tamanhos de páginas não pode estar vazia.")

    return [
        simular_tamanho_pagina(tamanhos_processos_kb, tamanho_pagina_kb)
        for tamanho_pagina_kb in tamanhos_paginas_kb
    ]
