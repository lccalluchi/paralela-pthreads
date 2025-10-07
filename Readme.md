# Tarea de Laboratorio: Estimación de Pi con Pthreads

Este proyecto implementa el cálculo de Pi usando diferentes estrategias de paralelismo con Pthreads, basado en el libro "An Introduction to Parallel Programming" de Peter Pacheco.

## Estrategias Implementadas

Se crearon 4 implementaciones principales, como se solicita:

1.  **Secuencial**: `01_pi_serial.c`
2.  **Busy-Waiting dentro del bucle FOR**: `03_pi_parallel_busy.c`
3.  **Busy-Waiting fuera del bucle FOR**: `04_pi_parallel_busy_cs.c`
4.  **MUTEX**: `05_pi_parallel_mutex.c`

Adicionalmente, se incluye `02_pi_parallel_race.c` como una versión preliminar que demuestra el problema de la condición de carrera al no tener sincronización.

---

## Explicación de las Implementaciones

1.  **Secuencial (`01_pi_serial.c`)**:
    *   Un programa de un solo hilo que calcula la estimación de Pi. Sirve como línea base para la comparación de rendimiento.

2.  **Busy-Waiting dentro del bucle FOR (`03_pi_parallel_busy.c`)**:
    *   Solución paralela que usa una variable `flag` para sincronizar los hilos en **cada iteración** del bucle. Se espera que esta estrategia sea muy ineficiente.

3.  **Busy-Waiting fuera del bucle FOR (`04_pi_parallel_busy_cs.c`)**:
    *   Una mejora sobre la anterior. Cada hilo calcula una suma local en su propio bucle `for` sin bloqueos. La espera activa solo se usa **al final**, en una sección crítica muy corta, para sumar el resultado local a la suma global.

4.  **MUTEX (`05_pi_parallel_mutex.c`)**:
    *   La solución estándar. Usa un `pthread_mutex_t` para proteger la sección crítica donde la suma local se agrega a la suma global. Es la forma más eficiente de gestionar el bloqueo.

---

## Comparación y Análisis de Resultados

Para realizar el análisis, se deben seguir los siguientes pasos:

#### 1. Compilar todos los archivos
```bash
# Para el secuencial
gcc 01_pi_serial.c -o 01_pi_serial -lm

# Para las versiones paralelas (repetir para cada archivo)
gcc 02_pi_parallel_race.c -o 02_pi_parallel_race -lpthread
gcc 03_pi_parallel_busy.c -o 03_pi_parallel_busy -lpthread
gcc 04_pi_parallel_busy_cs.c -o 04_pi_parallel_busy_cs -lpthread
gcc 05_pi_parallel_mutex.c -o 05_pi_parallel_mutex -lpthread
```

#### 2. Ejecutar y medir tiempos
Ejecutar cada programa con un número grande de iteraciones (ej. `100000000`) y con diferente número de hilos (1, 2, 4, 8...). Utilizar el comando `time` para medir el tiempo de ejecución de cada uno.

```bash
# Ejemplo de ejecución
time ./05_pi_parallel_mutex 4 100000000
```

#### 3. Analizar los Resultados
*   **Corrección:** Comprobar que la versión `02_pi_parallel_race` produce un resultado numérico incorrecto en comparación con las demás.
*   **Rendimiento:** Registrar los tiempos en una tabla y observar el *Speedup* (mejora de velocidad) de las versiones paralelas respecto a la secuencial.
*   **Comparación de Estrategias:** Notar la gran ineficiencia del busy-waiting dentro del bucle. Comparar el rendimiento del busy-waiting eficiente contra la solución con mutex, que debería ser la más rápida en la mayoría de los casos.