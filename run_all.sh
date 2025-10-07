#!/bin/bash

# Script para ejecutar todas las versiones del cálculo de Pi
# Uso: ./run_all.sh [n_iteraciones] [num_hilos]

# Valores por defecto
N=${1:-100000000}  # 100 millones de iteraciones por defecto
THREADS=${2:-4}    # 4 hilos por defecto

echo "=========================================="
echo "Comparación de Implementaciones de Pi"
echo "=========================================="
echo "Iteraciones: $N"
echo "Hilos (versiones paralelas): $THREADS"
echo "=========================================="
echo ""

# Compilar todos si es necesario
echo "Compilando programas..."
gcc 01_pi_serial.c -o 01_pi_serial -lm
gcc 02_pi_parallel_race.c -o 02_pi_parallel_race -lpthread
gcc 03_pi_parallel_busy.c -o 03_pi_parallel_busy -lpthread
gcc 04_pi_parallel_busy_cs.c -o 04_pi_parallel_busy_cs -lpthread
gcc 05_pi_parallel_mutex.c -o 05_pi_parallel_mutex -lpthread
echo "✓ Compilación completa"
echo ""

# Ejecutar versión serial
echo "1. VERSIÓN SERIAL"
echo "----------------------------------------"
./01_pi_serial $N
echo ""

# Ejecutar versión con race condition
echo "2. VERSIÓN PARALELA - RACE CONDITION"
echo "----------------------------------------"
./02_pi_parallel_race $THREADS $N
echo ""

# Ejecutar busy-waiting ineficiente (comentado por defecto - muy lento)
echo "3. VERSIÓN PARALELA - BUSY-WAIT INEFICIENTE"
echo "----------------------------------------"
echo "⚠️  ADVERTENCIA: Esta versión es extremadamente lenta"
echo "⚠️  Descomenta la línea en el script para ejecutarla"
./03_pi_parallel_busy $THREADS $N
echo "(Ejecución omitida - descomentar para ejecutar)"
echo ""

# Ejecutar busy-waiting eficiente
echo "4. VERSIÓN PARALELA - BUSY-WAIT EFICIENTE"
echo "----------------------------------------"
./04_pi_parallel_busy_cs $THREADS $N
echo ""

# Ejecutar versión con mutex
echo "5. VERSIÓN PARALELA - MUTEX"
echo "----------------------------------------"
./05_pi_parallel_mutex $THREADS $N
echo ""

echo "=========================================="
echo "Ejecución completada"
echo "=========================================="
