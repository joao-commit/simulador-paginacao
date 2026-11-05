"""Testes da lógica de simulação de paginação."""

import unittest

from simulador import (
    calcular_resultado_processo,
    comparar_tamanhos_pagina,
    simular_tamanho_pagina,
)


class TestCalcularResultadoProcesso(unittest.TestCase):
    """Testes dos cálculos de um processo individual."""

    def test_processo_multiplo_do_tamanho_da_pagina(self):
        resultado = calcular_resultado_processo(8, 4)

        self.assertEqual(resultado.quantidade_paginas, 2)
        self.assertEqual(resultado.memoria_alocada_kb, 8)
        self.assertEqual(resultado.fragmentacao_interna_kb, 0)

    def test_processo_que_nao_preenche_a_ultima_pagina(self):
        resultado = calcular_resultado_processo(10, 4)

        self.assertEqual(resultado.quantidade_paginas, 3)
        self.assertEqual(resultado.memoria_alocada_kb, 12)
        self.assertEqual(resultado.fragmentacao_interna_kb, 2)

    def test_processo_menor_que_uma_pagina(self):
        resultado = calcular_resultado_processo(1, 4)

        self.assertEqual(resultado.quantidade_paginas, 1)
        self.assertEqual(resultado.memoria_alocada_kb, 4)
        self.assertEqual(resultado.fragmentacao_interna_kb, 3)

    def test_processo_um_kb_maior_que_a_pagina(self):
        resultado = calcular_resultado_processo(9, 8)

        self.assertEqual(resultado.quantidade_paginas, 2)
        self.assertEqual(resultado.memoria_alocada_kb, 16)
        self.assertEqual(resultado.fragmentacao_interna_kb, 7)

    def test_arredondamento_para_cima_da_quantidade_de_paginas(self):
        resultado = calcular_resultado_processo(25, 2)

        self.assertEqual(resultado.quantidade_paginas, 13)
        self.assertEqual(resultado.memoria_alocada_kb, 26)
        self.assertEqual(resultado.fragmentacao_interna_kb, 1)

    def test_tamanho_do_processo_invalido(self):
        for tamanho in (0, -1, 4.5, "10", None, True):
            with self.subTest(tamanho=tamanho):
                with self.assertRaises(ValueError):
                    calcular_resultado_processo(tamanho, 4)

    def test_tamanho_da_pagina_invalido(self):
        for tamanho in (0, -1, 4.5, "4", None, False):
            with self.subTest(tamanho=tamanho):
                with self.assertRaises(ValueError):
                    calcular_resultado_processo(10, tamanho)


class TestSimularTamanhoPagina(unittest.TestCase):
    """Testes da simulação completa para um tamanho de página."""

    def test_resultado_para_paginas_de_2_kb(self):
        resultado = simular_tamanho_pagina([10, 25, 100], 2)

        self.assertEqual(resultado.tamanho_pagina_kb, 2)
        self.assertEqual(
            [item.quantidade_paginas for item in resultado.resultados_processos],
            [5, 13, 50],
        )
        self.assertEqual(resultado.total_paginas, 68)
        self.assertEqual(resultado.memoria_utilizada_kb, 135)
        self.assertEqual(resultado.memoria_total_alocada_kb, 136)
        self.assertEqual(resultado.fragmentacao_interna_total_kb, 1)
        self.assertAlmostEqual(
            resultado.aproveitamento_percentual,
            99.26470588235294,
            places=10,
        )

    def test_resultado_para_paginas_de_4_kb(self):
        resultado = simular_tamanho_pagina([10, 25, 100], 4)

        self.assertEqual(
            [item.quantidade_paginas for item in resultado.resultados_processos],
            [3, 7, 25],
        )
        self.assertEqual(resultado.total_paginas, 35)
        self.assertEqual(resultado.memoria_total_alocada_kb, 140)
        self.assertEqual(resultado.fragmentacao_interna_total_kb, 5)
        self.assertAlmostEqual(
            resultado.aproveitamento_percentual,
            96.42857142857143,
            places=10,
        )

    def test_resultado_para_paginas_de_8_kb(self):
        resultado = simular_tamanho_pagina([10, 25, 100], 8)

        self.assertEqual(
            [item.quantidade_paginas for item in resultado.resultados_processos],
            [2, 4, 13],
        )
        self.assertEqual(resultado.total_paginas, 19)
        self.assertEqual(resultado.memoria_total_alocada_kb, 152)
        self.assertEqual(resultado.fragmentacao_interna_total_kb, 17)
        self.assertAlmostEqual(
            resultado.aproveitamento_percentual,
            88.81578947368421,
            places=10,
        )

    def test_totais_sao_a_soma_dos_resultados_individuais(self):
        resultado = simular_tamanho_pagina([7, 13, 20, 45], 4)

        self.assertEqual(
            resultado.total_paginas,
            sum(
                item.quantidade_paginas
                for item in resultado.resultados_processos
            ),
        )
        self.assertEqual(
            resultado.memoria_total_alocada_kb,
            sum(
                item.memoria_alocada_kb
                for item in resultado.resultados_processos
            ),
        )
        self.assertEqual(
            resultado.fragmentacao_interna_total_kb,
            sum(
                item.fragmentacao_interna_kb
                for item in resultado.resultados_processos
            ),
        )

    def test_aproveitamento_de_cem_por_cento(self):
        resultado = simular_tamanho_pagina([8, 16, 32], 8)

        self.assertEqual(resultado.fragmentacao_interna_total_kb, 0)
        self.assertAlmostEqual(
            resultado.aproveitamento_percentual,
            100.0,
            places=10,
        )

    def test_lista_de_processos_vazia(self):
        with self.assertRaises(ValueError):
            simular_tamanho_pagina([], 4)

    def test_processo_invalido_na_lista(self):
        for tamanhos in ([10, 0], [10, -5], [10, "20"], [10, 2.5]):
            with self.subTest(tamanhos=tamanhos):
                with self.assertRaises(ValueError):
                    simular_tamanho_pagina(tamanhos, 4)

    def test_tamanho_de_pagina_invalido(self):
        for tamanho_pagina in (0, -1, 2.5, "4", None):
            with self.subTest(tamanho_pagina=tamanho_pagina):
                with self.assertRaises(ValueError):
                    simular_tamanho_pagina([10, 20], tamanho_pagina)


class TestCompararTamanhosPagina(unittest.TestCase):
    """Testes da comparação entre os tamanhos de página."""

    def test_comparacao_padrao_usa_2_4_e_8_kb(self):
        resultados = comparar_tamanhos_pagina([10, 25, 100])

        self.assertEqual(len(resultados), 3)
        self.assertEqual(
            [resultado.tamanho_pagina_kb for resultado in resultados],
            [2, 4, 8],
        )

    def test_comparacao_padrao_mantem_os_mesmos_processos(self):
        resultados = comparar_tamanhos_pagina([10, 25, 100])

        for resultado in resultados:
            self.assertEqual(
                [
                    item.tamanho_processo_kb
                    for item in resultado.resultados_processos
                ],
                [10, 25, 100],
            )
            self.assertEqual(resultado.memoria_utilizada_kb, 135)

    def test_memoria_alocada_cresce_com_o_tamanho_da_pagina(self):
        resultados = comparar_tamanhos_pagina([10, 25, 100])
        memorias_alocadas = [
            resultado.memoria_total_alocada_kb for resultado in resultados
        ]

        self.assertEqual(memorias_alocadas, [136, 140, 152])

    def test_aproveitamento_e_maior_com_paginas_menores_neste_exemplo(self):
        resultados = comparar_tamanhos_pagina([10, 25, 100])
        aproveitamentos = [
            resultado.aproveitamento_percentual for resultado in resultados
        ]

        self.assertEqual(aproveitamentos, sorted(aproveitamentos, reverse=True))
        self.assertEqual(resultados[0].aproveitamento_percentual,
                         max(aproveitamentos))

    def test_comparacao_com_tamanhos_personalizados(self):
        resultados = comparar_tamanhos_pagina([10, 25, 100], (1, 16))

        self.assertEqual(
            [resultado.tamanho_pagina_kb for resultado in resultados],
            [1, 16],
        )
        self.assertEqual(resultados[0].fragmentacao_interna_total_kb, 0)
        self.assertEqual(resultados[1].memoria_total_alocada_kb, 160)

    def test_lista_de_processos_vazia(self):
        with self.assertRaises(ValueError):
            comparar_tamanhos_pagina([])

    def test_lista_de_paginas_vazia(self):
        with self.assertRaises(ValueError):
            comparar_tamanhos_pagina([10, 20], ())

    def test_tamanho_de_pagina_invalido_na_lista(self):
        with self.assertRaises(ValueError):
            comparar_tamanhos_pagina([10, 20], (2, 0, 8))


if __name__ == "__main__":
    unittest.main()
