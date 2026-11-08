"""
Comparação de desempenho: alocação na PILHA (stack) vs alocação no HEAP.

Parte B - Prática
Linguagem escolhida: Python

IMPORTANTE (contexto sobre Python):
Em Python (CPython), TODOS os objetos vivem no heap. O que muda é o
que acontece em cada teste:
  - Teste "pilha": chamamos uma função que cria variáveis locais. O frame
    da função (com suas variáveis locais) é criado e destruído a cada
    chamada, simulando o comportamento de variáveis na pilha.
  - Teste "heap": criamos e destruímos explicitamente instâncias de uma
    classe, o que exige alocação de memória no heap, execução de
    __init__ e liberação do objeto (contagem de referências).
"""

import gc
import statistics
import time

# ----------------------------------------------------------------------
# CONFIGURAÇÕES
# ----------------------------------------------------------------------
N = 1_000_000        # quantidade de variáveis/objetos por teste
REPETICOES = 10      # número de vezes que cada teste é executado


# ----------------------------------------------------------------------
# TESTE 1: "ALOCAÇÃO NA PILHA"
# ----------------------------------------------------------------------
def funcao_com_locais():
    """
    Cria variáveis locais. Elas existem apenas durante a execução da
    função e são descartadas automaticamente quando ela retorna
    (comportamento análogo ao da pilha de chamadas).
    """
    a = 1
    b = 2
    c = a + b
    return c


def teste_pilha():
    """Chama a função 1.000.000 de vezes e retorna o tempo gasto (s)."""
    inicio = time.perf_counter()          # relógio de alta resolução
    for _ in range(N):
        funcao_com_locais()               # cria e destrói as variáveis locais
    fim = time.perf_counter()
    return fim - inicio


# ----------------------------------------------------------------------
# TESTE 2: ALOCAÇÃO NO HEAP
# ----------------------------------------------------------------------
class Objeto:
    """
    Objeto simples alocado dinamicamente no heap.
    __slots__ evita o dicionário interno por instância, deixando o
    objeto mais leve e o teste mais "justo".
    """
    __slots__ = ("valor",)

    def __init__(self, valor):
        self.valor = valor


def teste_heap():
    """Aloca e desaloca 1.000.000 de objetos e retorna o tempo gasto (s)."""
    inicio = time.perf_counter()
    for i in range(N):
        obj = Objeto(i)   # alocação dinâmica no heap + chamada do __init__
        del obj           # remove a referência -> o objeto é liberado
    fim = time.perf_counter()
    return fim - inicio


# ----------------------------------------------------------------------
# EXECUÇÃO REPETIDA E CÁLCULO DA MÉDIA
# ----------------------------------------------------------------------
def executar_varias_vezes(teste, repeticoes):
    """Executa um teste várias vezes e devolve a lista de tempos."""
    # Aquecimento (warm-up): uma execução descartada para evitar que
    # efeitos de "primeira execução" (caches, etc.) distorçam a média.
    teste()

    tempos = []
    for _ in range(repeticoes):
        tempos.append(teste())
    return tempos


def main():
    # Desativa o coletor de lixo cíclico durante a medição para que
    # ele não interrompa o teste em momentos aleatórios. (A liberação
    # por contagem de referências continua funcionando normalmente.)
    gc.disable()

    print(f"Executando {REPETICOES} repetições de {N:,} operações cada...\n")

    tempos_pilha = executar_varias_vezes(teste_pilha, REPETICOES)
    tempos_heap = executar_varias_vezes(teste_heap, REPETICOES)

    gc.enable()

    # ------------------------------------------------------------------
    # ESTATÍSTICAS
    # ------------------------------------------------------------------
    media_pilha = statistics.mean(tempos_pilha)
    media_heap = statistics.mean(tempos_heap)
    desvio_pilha = statistics.stdev(tempos_pilha)
    desvio_heap = statistics.stdev(tempos_heap)

    # Diferença percentual: quanto o heap é mais lento/rápido que a pilha,
    # tomando a pilha como referência.
    #   (heap - pilha) / pilha * 100
    dif_percentual = (media_heap - media_pilha) / media_pilha * 100

    # Fator de proporção (ex.: 1,8x mais lento)
    fator = media_heap / media_pilha

    # ------------------------------------------------------------------
    # EXIBIÇÃO DOS RESULTADOS
    # ------------------------------------------------------------------
    print("=" * 62)
    print(f"{'RESULTADOS':^62}")
    print("=" * 62)
    print(f"{'Teste':<12}{'Média (s)':>14}{'Desvio (s)':>14}{'Min (s)':>11}{'Max (s)':>11}")
    print("-" * 62)
    print(f"{'Pilha':<12}{media_pilha:>14.4f}{desvio_pilha:>14.4f}"
          f"{min(tempos_pilha):>11.4f}{max(tempos_pilha):>11.4f}")
    print(f"{'Heap':<12}{media_heap:>14.4f}{desvio_heap:>14.4f}"
          f"{min(tempos_heap):>11.4f}{max(tempos_heap):>11.4f}")
    print("-" * 62)

    if dif_percentual >= 0:
        print(f"Heap foi {dif_percentual:.2f}% MAIS LENTO que a pilha "
              f"({fator:.2f}x).")
    else:
        print(f"Heap foi {abs(dif_percentual):.2f}% MAIS RÁPIDO que a pilha "
              f"({fator:.2f}x).")
    print("=" * 62)


if __name__ == "__main__":
    main()


# ======================================================================
# EXPLICAÇÃO DOS RESULTADOS (ITEM 4 DO ENUNCIADO)
# ======================================================================
#
# 1) Por que a "pilha" tende a ser mais rápida?
#    - Variáveis locais vivem no frame da função, que é criado ao chamar
#      e descartado ao retornar. É um processo simples e previsível
#      (empilhar/desempilhar), sem precisar "procurar" espaço livre.
#    - Os valores usados (1, 2, 3) são inteiros pequenos, que o CPython
#      mantém em cache e reutiliza, então praticamente não há alocação.
#
# 2) Por que o heap tende a ser mais lento?
#    - Cada Objeto(i) exige pedir memória ao alocador (pymalloc),
#      inicializar o objeto, executar __init__ (uma chamada de função
#      extra) e depois liberar a memória quando a contagem de
#      referências chega a zero (del).
#    - Ou seja: há mais trabalho por operação do que no teste da pilha.
#
# 3) Observação sobre a linguagem:
#    - Em C, a diferença seria muito mais pronunciada e "pura": a pilha
#      é só mover um ponteiro, enquanto malloc/free envolvem o gerenciador
#      de memória do sistema. Em Python, como tudo é objeto e há o
#      overhead do interpretador, a diferença existe mas é mascarada.
#
# 4) Possíveis variações nos resultados:
#    - Carga do sistema: outros programas abertos competem pela CPU e
#      mudam os tempos entre execuções (por isso usamos média e desvio).
#    - Versão do Python: versões mais novas (3.11+) otimizam chamadas de
#      função e podem reduzir a diferença.
#    - Coletor de lixo: foi desativado aqui; se estivesse ativo, poderia
#      causar picos de tempo no teste do heap.
#    - Cache da CPU e fragmentação de memória: podem alterar o tempo de
#      alocação entre rodadas.
#    - Escala de frequência da CPU (economia de energia, aquecimento).
#    - Tamanho/complexidade do objeto: objetos maiores ou com mais
#      atributos aumentam o custo do heap.
#    - Por isso, os resultados absolutos mudam de máquina para máquina,
#      mas a tendência (heap mais lento que pilha) costuma se manter.
# ======================================================================
