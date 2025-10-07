#!/bin/bash

# Script de benchmarking para comparar implementaciones de Pi
# Genera resultados en CSV

OUTPUT_FILE="resultados_benchmark.csv"

# Configuración
ITERATIONS=(1000 2000 5000 10000 20000 50000 80000 100000 200000 500000 1000000 2000000 5000000 10000000)
THREADS=(1 2 3 4 5 6)

echo "==========================================="
echo "Script de Benchmarking - Cálculo de Pi"
echo "==========================================="
echo ""

# Compilar todos los programas
echo "Compilando programas..."
gcc 01_pi_serial.c -o 01_pi_serial -lm
gcc 02_pi_parallel_race.c -o 02_pi_parallel_race -lpthread
gcc 03_pi_parallel_busy.c -o 03_pi_parallel_busy -lpthread
gcc 04_pi_parallel_busy_cs.c -o 04_pi_parallel_busy_cs -lpthread
gcc 05_pi_parallel_mutex.c -o 05_pi_parallel_mutex -lpthread
echo "✓ Compilación completa"
echo ""

# Crear archivo CSV con encabezados
echo "programa,iteraciones,hilos,tiempo_segundos,resultado_pi" > $OUTPUT_FILE

echo "Ejecutando benchmarks..."
echo ""

# Función para extraer tiempo y resultado de la salida
parse_output() {
    local output="$1"
    local tiempo=$(echo "$output" | grep "Tiempo de ejecución" | awk '{print $4}')
    local pi=$(echo "$output" | grep "Estimación de pi" | sed 's/.*= //')
    echo "$tiempo|$pi"
}

# 1. VERSIÓN SERIAL (solo varía iteraciones, hilos=1)
echo "Ejecutando versión serial..."
for n in "${ITERATIONS[@]}"; do
    output=$(./01_pi_serial $n)
    resultado=$(parse_output "$output")
    tiempo=$(echo "$resultado" | cut -d'|' -f1)
    pi=$(echo "$resultado" | cut -d'|' -f2)
    echo "01_pi_serial,$n,1,$tiempo,$pi" >> $OUTPUT_FILE
    echo "  Serial - N=$n: ${tiempo}s"
done
echo ""

# 2. VERSIÓN PARALELA - RACE CONDITION
echo "Ejecutando versión con race condition..."
for n in "${ITERATIONS[@]}"; do
    for t in "${THREADS[@]}"; do
        output=$(./02_pi_parallel_race $t $n)
        resultado=$(parse_output "$output")
        tiempo=$(echo "$resultado" | cut -d'|' -f1)
        pi=$(echo "$resultado" | cut -d'|' -f2)
        echo "02_pi_parallel_race,$n,$t,$tiempo,$pi" >> $OUTPUT_FILE
        echo "  Race - N=$n T=$t: ${tiempo}s"
    done
done
echo ""

# 3. VERSIÓN PARALELA - BUSY-WAIT INEFICIENTE (solo con iteraciones bajas)
echo "Ejecutando versión busy-wait ineficiente (hasta 8000 iteraciones)..."
for n in "${ITERATIONS[@]}"; do
    for t in "${THREADS[@]}"; do
        output=$(./03_pi_parallel_busy $t $n)
        resultado=$(parse_output "$output")
        tiempo=$(echo "$resultado" | cut -d'|' -f1)
        pi=$(echo "$resultado" | cut -d'|' -f2)
        echo "03_pi_parallel_busy,$n,$t,$tiempo,$pi" >> $OUTPUT_FILE
        echo "  Busy-ineficiente - N=$n T=$t: ${tiempo}s"
    done
done
echo ""

# 4. VERSIÓN PARALELA - BUSY-WAIT EFICIENTE
echo "Ejecutando versión busy-wait eficiente..."
for n in "${ITERATIONS[@]}"; do
    for t in "${THREADS[@]}"; do
        output=$(./04_pi_parallel_busy_cs $t $n)
        resultado=$(parse_output "$output")
        tiempo=$(echo "$resultado" | cut -d'|' -f1)
        pi=$(echo "$resultado" | cut -d'|' -f2)
        echo "04_pi_parallel_busy_cs,$n,$t,$tiempo,$pi" >> $OUTPUT_FILE
        echo "  Busy-eficiente - N=$n T=$t: ${tiempo}s"
    done
done
echo ""

# 5. VERSIÓN PARALELA - MUTEX
echo "Ejecutando versión con mutex..."
for n in "${ITERATIONS[@]}"; do
    for t in "${THREADS[@]}"; do
        output=$(./05_pi_parallel_mutex $t $n)
        resultado=$(parse_output "$output")
        tiempo=$(echo "$resultado" | cut -d'|' -f1)
        pi=$(echo "$resultado" | cut -d'|' -f2)
        echo "05_pi_parallel_mutex,$n,$t,$tiempo,$pi" >> $OUTPUT_FILE
        echo "  Mutex - N=$n T=$t: ${tiempo}s"
    done
done
echo ""

echo "==========================================="
echo "Benchmark completado"
echo "Resultados guardados en: $OUTPUT_FILE"
echo "==========================================="
