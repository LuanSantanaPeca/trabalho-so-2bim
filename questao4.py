import gc
import sys


class Objeto:
    def __init__(self, nome):
        self.nome = nome
        self.dados = [1]*100
        
        print(f"objeto {nome} foi criado")
        
    def __del__(self):
        print(f"o objeto {self.nome} foi deletado")
        

def main():
    objeto1 = Objeto("objeto01")
    objeto2 = Objeto("objeto02")
    objeto3 = Objeto("objeto03")
    objeto4 = Objeto("objeto04")
    objeto5 = Objeto("objeto05")
    
    objetos = [objeto1, objeto2, objeto3, objeto4, objeto5]
            
            
    # o numero de referencias do objeto1 é 3, uma quando o objeto é declarado, outra quando o incluimos na lista
    # objetos, e por ultimo quando o referenciamos na linha de codigo abaixo. 
    print(sys.getrefcount(objeto1))
    
    del objetos
    print(sys.getrefcount(objeto1))
    
    del objeto1
    print("todas as referencias a objeto1 foram destruidas")
    # perceba que á excluimors todas as referencias de um objeto seu espaço na memoria
    # é limpo automaticamente pela contagem de referências.
    
    
    objeto2.conexao = objeto3
    objeto3.conexao = objeto2
    # perceba que objeto2 esta referenciando objeto3, e objeto3 esta referenciando objeto2.
    # isso vira um ciclo de referencia, o que é um problema já que mesmo se deletassemos  
    # objeto2 e objeto3 a relação entre eles continuaria a existir.
    
    del objeto2
    del objeto3
    # em casos assim se utiliza o coletor de ciclos, que detequeta essas referencias circulares
    # e limpa a memoria utilizada por esses objetos
    coletados = gc.collect()
    print("Objetos coletados:", coletados)
    
    
    
    objeto4.conexao = objeto5
    objeto5.conexao = objeto4
    # note que a coleta de lixo leva em conta o numero de coletas que cada objeto sobreviveu. 
    # sendo eles separados em gerações, então se um objeto é recem criado ele se torna de geração zero, 
    # se ele sobreviveu uma coleta ele é geração 1, e se sobreviveu mais de 2 coletas ele vira geração 2.
    
    gc.collect(0)
    #coleta o lixo de geração 0
    
    gc.collect(1)
    #coleta o lixo de geração 1
    
    print("Limites:", gc.get_threshold())
    print("Contadores:", gc.get_count())
    print("Estatísticas:", gc.get_stats())
    
    del objeto4
    del objeto5
    
    gc.collect(0)
    # perceba que mesmo ao coletar o lixo a referencia em ciclo continuara
    # isso se da porque nos estamos limpando apenas o lixo de geração 0, e não os de geração 2.
    
    gc.collect(2) 
    # note também que a coleta da geração 2 verifica também as gerações mais novas.
    

if __name__ == '__main__':
    main()
    
            