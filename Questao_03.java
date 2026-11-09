//Parte B - Prática

/*
Para compilar e rodar
No terminal, navegar até a pasta em que esse arquivo está (usando cd)
javac Questao3.java (na pasta em que o arquivo estiver)
java Questao3 (na pasta em que o arquivo estiver)

Frames teste > 4, 3
Sequência teste > 7 0 1 2 0 3 0 4 2 3 0 3 2, 3 2 1 0 3 2 4 3 2 1 0 4
*/

/*
De forma geral, esse programa utiliza Queues para armazenar tanto os valores dados inicialmente pelo usuário quanto a fila de frames.

O sistema passa pela sequência de páginas item por item. Para cada item, ele analisa para ver se aquele item já existe dentro da fila. Se existir, é um Page Hit. Caso não exista, é um Page Fault, independentemente do tamanho da fila.

Novos elementos são inseridos na fila até que ela atinja seu limite (definido por num_frames). Quando atinge esse limite, os novos elementos que forem adicionados farão com que o item mais antigo seja apagado da lista (FIFO).

Outros elementos existem para controle da execução, como pageMsg, que define se será exibido Page Hit ou Page Fault, pageFaults, que conta a quantidade de Page Faults registrados e taxaFaults, que é a divisão da quantidade de Page Faults dividida pelo tamanho da sequência.
*/

import java.util.Scanner;
import java.util.Queue;
import java.util.LinkedList;

public class Questao_03{
    public static void main(String[] args){
        //Inicialização do Scanner
        Scanner scanner = new Scanner(System.in);

        //Definição da capacidade máxima de frames
        System.out.println("Insira o número de frames disponíveis na memória:");
        int num_frames = Integer.parseInt(scanner.nextLine());

        //Recebimento da sequência e tranformação dela de uma string para uma Queue. Poderia ser transdormada em um array simplesmente, mas como Queue seria necessário para a próxima parte, manti o padrão.
        System.out.println("Insira a sequência de referências a páginas (separadas somente por espaço):");
        String temp_seq = scanner.nextLine();
        String[] temp_array = temp_seq.split(" ");
        Queue<Integer> seq_pags = new LinkedList<Integer>();
        for(int i=0; i<temp_array.length; i++){
            seq_pags.add(Integer.parseInt(temp_array[i]));
        }
        
        Queue<Integer> fila = new LinkedList<Integer>();//Inicialização da fila de frames
        int pageFaults = 0;
        for(Integer pag : seq_pags){//Repete o looping uma vez para cada item do array da sequência de páginas
            Boolean novoElemento = true;
            String pageMsg = "";
            for(Integer item : fila){//Passa pela fila de frames atual, comparando se o item da sequência atual existe na fila
                if(pag == item){
                    novoElemento = false;
                    pageMsg = "Page Hit";//Caso exista, emite um page hit
                }
            }
            if(novoElemento){//Só é executado caso o item não exista na fila
                pageFaults += 1;
                if(fila.size() >= num_frames){
                    int removido = fila.poll();//Remove o primeiro item da lista e armazena ele em na variável removido
                    pageMsg = ("Page Fault (substituiu " + removido + ")");
                }else{
                    pageMsg = "Page Fault";
                }
                fila.add(pag);//Adiciona o item atual ao final da fila
            }
            System.out.println("Referência: " + pag + " | Frames: " + fila + " | " + pageMsg);
        }
        System.out.println("Total Page Faults: " + pageFaults);
        double taxaFaults = (double)pageFaults/(double)seq_pags.size();
        System.out.println("Taxa Page Faults: " + String.format("%.2f", ((taxaFaults)*100)) + "%");
    }
}