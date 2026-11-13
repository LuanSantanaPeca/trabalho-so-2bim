    # Análise comparativa:
    # O algoritmo LRU apresenta uma estratégia de substituição mais eficiente em situações nas quais páginas acessadas 
    # recentemente possuem maior probabilidade de serem utilizadas novamente. Diferentemente do FIFO,
    # que remove sempre a página mais antiga na memória, o LRU considera o histórico de acessos para escolher qual página substituir.
    # Isso pode resultar em uma menor quantidade de faltas de página e, consequentemente, em uma menor taxa de falhas. 
    # Entretanto, o LRU exige um controle maior sobre os acessos à memória, tornando sua implementação mais complexa que a do FIFO. 
    # O desempenho de ambos depende da sequência de referências e da quantidade de frames disponíveis.



def LRU(sequencia, frames):

    # para representar a memoria sera usado um dicionario
    memoria = {}
    faltas = 0
    acertos = 0
    total = 0


    
    # Percorre a sequência de páginas, utilizando enumerate para registraro instante de cada acesso. Se a página já 
    # estiver na memória, ocorre um acerto (Page Hit), e seu tempo de acesso é atualizado. Caso contrário,ocorre uma 
    # falta (Page Fault). Se a memória estiver cheia, identifica e remove a página menos recentemente utilizada,
    # liberando espaço para a nova página. Por fim, atualiza o registro de tempo da página inserida
    # e incrementa o total de referências processadas
    for tempo, pagina in enumerate(sequencia):
        if pagina in memoria:
            acertos += 1
            
            memoria[pagina] = tempo

        else:
            faltas += 1

            if len(memoria) == frames:
            
                vitima = min(memoria, key=memoria.get)
                del memoria[vitima]

            memoria[pagina] = tempo

        total += 1

    print(f"\nfaltas: {faltas}")
    print(f"acertos: {acertos}")
    print(f"total de paginas: {total}\n")
    print(f"taxa de falha: {round((faltas / total) * 100, 2)}%")
    print(f"memoria: {memoria}\n")


def main():
    frames = int(input("Insira o número de frames disponíveis na memória: "))
    sequencia = list(map(int, input("Insira a sequência de referências (separadas por espaço): ").split())) 
    
    LRU(sequencia, frames)
    
if __name__ == '__main__':
    main()