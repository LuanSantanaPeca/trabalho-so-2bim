#include <stdio.h>
#include <stdlib.h>   // malloc, free, exit codes
#include <stdint.h>   // uintptr_t, uintmax_t

int main(void) {
    /* ---------- 1. Array "estático" de 5 inteiros (valores 1 a 5)*/
    int estatico[5];
    for (int i = 0; i < 5; i++) {
        estatico[i] = i + 1;
    }

    /*2. Alocação dinâmica de 10 inteiros */
    int *dinamico = malloc(10 * sizeof(int));

    /* Verifica se a alocação foi bem-sucedida ANTES de usar o ponteiro */
    if (dinamico == NULL) {
        fprintf(stderr, "Erro: falha ao alocar memória.\n");
        return EXIT_FAILURE;
    }

    /*3. Preenche o array dinâmico com 10 a 19*/
    for (int i = 0; i < 10; i++) {
        dinamico[i] = 10 + i;
    }

    /* Exibe os valores de cada array */
    printf("=== Array estatico (valores) ===\n");
    for (int i = 0; i < 5; i++) {
        printf("estatico[%d] = %d (endereco: %p)\n", i, estatico[i], (void *)&estatico[i]);
    }

    printf("\n=== Array dinamico (valores) ===\n");
    for (int i = 0; i < 10; i++) {
        printf("dinamico[%d] = %d (endereco: %p)\n", i, dinamico[i], (void *)&dinamico[i]);
    }

    /*  4. Endereços base de ambos os arrays */
    printf("\n=== Enderecos base ===\n");
    printf("Array estatico: %p\n", (void *)estatico);
    printf("Array dinamico: %p\n", (void *)dinamico);

    /* 5. Diferença entre os endereços (em bytes)  */
    /* Converto para uintptr_t para subtrair como números (em bytes),
       e não como ponteiros (que dariam resultado em "elementos"). */
    uintptr_t end_est = (uintptr_t)estatico;
    uintptr_t end_din = (uintptr_t)dinamico;
    uintptr_t diferenca = (end_est > end_din) ? (end_est - end_din)
                                              : (end_din - end_est);

    printf("\nDiferenca entre os enderecos: %ju bytes\n", (uintmax_t)diferenca);
    printf("(Distancia grande => estao em regioes diferentes: stack x heap)\n");

    /* 6. Libera a memória dinâmica*/
    free(dinamico);
    dinamico = NULL;   // evita uso acidental de ponteiro "pendurado"

    return EXIT_SUCCESS;
} 
