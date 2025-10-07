// Compilar: gcc 05_pi_parallel_mutex.c -o 05_pi_parallel_mutex -lpthread
// Ejecutar: ./05_pi_parallel_mutex <hilos> <n>
// Ejemplo: ./05_pi_parallel_mutex 4 100000000

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>

long long thread_count;
long long n;
double sum;
pthread_mutex_t mutex;

void* Thread_sum(void* rank);

int main(int argc, char* argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Uso: %s <hilos> <n>\n", argv[0]);
        return 1;
    }
    thread_count = strtol(argv[1], NULL, 10);
    n = strtoll(argv[2], NULL, 10);
    
    pthread_t* thread_handles = malloc(thread_count * sizeof(pthread_t));
    sum = 0.0;
    pthread_mutex_init(&mutex, NULL);

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (long thread = 0; thread < thread_count; thread++) {
        pthread_create(&thread_handles[thread], NULL, Thread_sum, (void*)thread);
    }

    for (long thread = 0; thread < thread_count; thread++) {
        pthread_join(thread_handles[thread], NULL);
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double elapsed = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;

    pthread_mutex_destroy(&mutex);
    free(thread_handles);

    double pi_approx = 4.0 * sum;
    printf("Estimación de pi (Mutex, n=%lld, hilos=%ld) = %.15f\n", n, thread_count, pi_approx);
    printf("Tiempo de ejecución: %.6f segundos\n", elapsed);

    return 0;
}

void* Thread_sum(void* rank) {
    long my_rank = (long)rank;
    double factor;
    long long i;
    long long my_n = n / thread_count;
    long long my_first_i = my_n * my_rank;
    long long my_last_i = my_first_i + my_n;
    double my_sum = 0.0;

    if (my_first_i % 2 == 0) {
        factor = 1.0;
    } else {
        factor = -1.0;
    }

    for (i = my_first_i; i < my_last_i; i++) {
        my_sum += factor / (2 * i + 1);
        factor = -factor;
    }
    
    pthread_mutex_lock(&mutex);
    sum += my_sum;
    pthread_mutex_unlock(&mutex);

    return NULL;
}
