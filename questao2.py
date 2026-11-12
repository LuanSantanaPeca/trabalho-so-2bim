# PARTE A - TEORICA
#
# FRAGMENTACAO INTERNA
# E o espaco desperdicado dentro de uma particao ja alocada a um processo.
# Ocorre quando a particao e maior do que o processo precisa. Esse espaco
# sobrando fica reservado para aquele processo e nenhum outro pode usa-lo.
# E tipica de memoria com particoes fixas, pois os tamanhos sao definidos
# antes e o processo precisa se encaixar neles.
# Exemplo pratico: com particoes de 100, 150 e 200 unidades, um processo de
# 140 unidades vai para a de 150 e deixa 10 unidades inutilizadas dentro da
# particao.
#
# FRAGMENTACAO EXTERNA
# E o espaco livre que existe no total, mas esta espalhado em pedacos
# pequenos e separados, de modo que nenhum pedaco sozinho comporta um novo
# processo. Ocorre em alocacao dinamica (particoes de tamanho variavel):
# conforme processos entram e saem, surgem buracos entre os blocos ocupados.
# Exemplo pratico: a memoria tem tres buracos livres de 100, 80 e 120
# unidades, separados por processos em execucao. A soma e 300 unidades
# livres, mas um processo de 200 unidades nao pode ser alocado, pois nenhum
# buraco isolado chega a 200. Solucoes: compactacao ou paginacao.

TAMANHOS = [100, 150, 200, 250, 300]

memoria = [
    {"id": i + 1, "tamanho": t, "processo": None, "uso": 0}
    for i, t in enumerate(TAMANHOS)
]


def fragmentacao_total():
    return sum(p["tamanho"] - p["uso"] for p in memoria if p["processo"])


def alocar_processo(nome, tamanho):
    if any(p["processo"] == nome for p in memoria):
        print(f"[ERRO] Processo {nome} ja esta alocado.")
        return False

    for p in memoria:
        if p["processo"] is None and p["tamanho"] >= tamanho:
            p["processo"] = nome
            p["uso"] = tamanho
            frag = p["tamanho"] - tamanho
            print(f"[OK] {nome} ({tamanho}) alocado na particao {p['id']} "
                  f"({p['tamanho']}). Fragmentacao interna: {frag}")
            print(f"     Fragmentacao interna total: {fragmentacao_total()}")
            return True

    print(f"[FALHA] Sem particao livre que comporte {nome} ({tamanho}).")
    return False


def liberar_processo(nome):
    for p in memoria:
        if p["processo"] == nome:
            p["processo"] = None
            p["uso"] = 0
            print(f"[OK] {nome} liberado da particao {p['id']}.")
            return True
    print(f"[ERRO] Processo {nome} nao encontrado.")
    return False


def exibir_memoria():
    print("\n--- Estado da memoria ---")
    print(f"{'Part.':<6}{'Tamanho':<9}{'Processo':<10}{'Uso':<6}{'Frag.':<6}")
    for p in memoria:
        if p["processo"]:
            print(f"{p['id']:<6}{p['tamanho']:<9}{p['processo']:<10}"
                  f"{p['uso']:<6}{p['tamanho'] - p['uso']:<6}")
        else:
            print(f"{p['id']:<6}{p['tamanho']:<9}{'(livre)':<10}{'-':<6}{'-':<6}")
    print("-------------------------\n")


if __name__ == "__main__":
    alocar_processo("P1", 90)
    alocar_processo("P2", 140)
    alocar_processo("P3", 180)
    exibir_memoria()

    liberar_processo("P2")
    alocar_processo("P4", 100)
    alocar_processo("P5", 350)
    exibir_memoria()

    print(f"Fragmentacao interna total final: {fragmentacao_total()} unidades")