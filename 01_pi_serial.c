// Compilar: gcc 01_pi_serial.c -o 01_pi_serial -lm
// Ejecutar: ./01_pi_serial <n>
// Ejemplo: ./01_pi_serial 100000000

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Uso: %s <n>\n", argv[0]);
        return 1;
    }
    long long n = strtoll(argv[1], NULL, 10);
    double sum = 0.0;
    double factor = 1.0;

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (long long i = 0; i < n; i++) {
        sum += factor / (2 * i + 1);
        factor = -factor;
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double elapsed = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;

    double pi_approx = 4.0 * sum;
    printf("Estimación de pi (Serial, n=%lld) = %.15f\n", n, pi_approx);
    printf("Tiempo de ejecución: %.6f segundos\n", elapsed);

    return 0;
}
