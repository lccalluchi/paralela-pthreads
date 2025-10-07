#!/usr/bin/env python3
"""
Script para generar gráficos del benchmark de Pi
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

# Configuración de estilo
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Función para formatear el eje Y (tiempo)
def format_time(value, pos):
    """Formatea valores de tiempo para el eje Y"""
    if value >= 1:
        return f'{value:.1f}s'
    elif value >= 0.001:
        return f'{value*1000:.0f}ms'
    elif value >= 0.000001:
        return f'{value*1000000:.0f}µs'
    else:
        return f'{value*1000000:.2f}µs'

# Leer datos
df = pd.read_csv('resultados_benchmark.csv')

# Mapeo de nombres para gráficos
nombres_programas = {
    '01_pi_serial': 'Serial',
    '02_pi_parallel_race': 'Race Condition',
    '03_pi_parallel_busy': 'Busy-Wait Ineficiente',
    '04_pi_parallel_busy_cs': 'Busy-Wait Eficiente',
    '05_pi_parallel_mutex': 'Mutex'
}

# Colores por programa
colores = {
    '01_pi_serial': '#2E86AB',
    '02_pi_parallel_race': '#A23B72',
    '03_pi_parallel_busy': '#F18F01',
    '04_pi_parallel_busy_cs': '#C73E1D',
    '05_pi_parallel_mutex': '#6A994E'
}

print("Generando gráficos...")

# ============================================================
# GRÁFICO 1: Tiempo vs Iteraciones (todas las versiones)
# ============================================================
print("1. Tiempo vs Iteraciones...")

fig, ax = plt.subplots(figsize=(12, 8))

for programa in df['programa'].unique():
    # Para cada programa, agrupar por iteraciones y promediar tiempos
    data = df[df['programa'] == programa].groupby('iteraciones')['tiempo_segundos'].mean()

    ax.plot(data.index, data.values,
            marker='o', linewidth=2, markersize=6,
            label=nombres_programas[programa],
            color=colores[programa])

ax.set_xlabel('Número de Iteraciones', fontsize=12, fontweight='bold')
ax.set_ylabel('Tiempo de Ejecución', fontsize=12, fontweight='bold')
ax.set_title('Rendimiento: Tiempo vs Iteraciones (promedio por número de hilos)',
             fontsize=14, fontweight='bold', pad=20)
ax.set_xscale('log')
ax.set_yscale('log')

# Mejorar etiquetas del eje X
ax.set_xticks([1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000, 2000000, 5000000, 10000000])
ax.set_xticklabels(['1K', '2K', '5K', '10K', '20K', '50K', '100K', '200K', '500K', '1M', '2M', '5M', '10M'], rotation=45)

# Formatear eje Y
ax.yaxis.set_major_formatter(FuncFormatter(format_time))

ax.legend(loc='upper left', fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('grafico_1_tiempo_vs_iteraciones.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# GRÁFICO 2: Speedup vs Hilos (10M iteraciones)
# ============================================================
print("2. Speedup vs Hilos...")

# Filtrar solo 10M iteraciones
df_10M = df[df['iteraciones'] == 10000000].copy()

# Obtener tiempo serial como referencia
tiempo_serial = df_10M[df_10M['programa'] == '01_pi_serial']['tiempo_segundos'].values[0]

fig, ax = plt.subplots(figsize=(12, 8))

# Línea ideal
hilos_range = range(1, 7)
ax.plot(hilos_range, hilos_range, 'k--', linewidth=2, label='Speedup Ideal', alpha=0.5)

# Calcular speedup para cada versión paralela
for programa in ['02_pi_parallel_race', '04_pi_parallel_busy_cs', '05_pi_parallel_mutex']:
    speedups = []
    hilos_list = []

    for hilos in range(1, 7):
        data = df_10M[(df_10M['programa'] == programa) & (df_10M['hilos'] == hilos)]
        if not data.empty:
            tiempo = data['tiempo_segundos'].values[0]
            speedup = tiempo_serial / tiempo
            speedups.append(speedup)
            hilos_list.append(hilos)

    ax.plot(hilos_list, speedups,
            marker='o', linewidth=2, markersize=8,
            label=nombres_programas[programa],
            color=colores[programa])

ax.set_xlabel('Número de Hilos', fontsize=12, fontweight='bold')
ax.set_ylabel('Speedup', fontsize=12, fontweight='bold')
ax.set_title('Speedup vs Número de Hilos (10M iteraciones)',
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(range(1, 7))
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('grafico_2_speedup_vs_hilos.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# GRÁFICO 3: Comparativa por Hilos (10M iteraciones) - SIN BUSY INEFICIENTE
# ============================================================
print("3. Comparativa por Hilos (barras)...")

fig, ax = plt.subplots(figsize=(14, 8))

# EXCLUIR busy-wait ineficiente para mejor visualización
programas_comparar = ['02_pi_parallel_race', '04_pi_parallel_busy_cs', '05_pi_parallel_mutex']
hilos_vals = sorted(df_10M['hilos'].unique())

x = np.arange(len(hilos_vals))
width = 0.25

for i, programa in enumerate(programas_comparar):
    tiempos = []
    for hilos in hilos_vals:
        data = df_10M[(df_10M['programa'] == programa) & (df_10M['hilos'] == hilos)]
        if not data.empty:
            tiempos.append(data['tiempo_segundos'].values[0])
        else:
            tiempos.append(0)

    offset = (i - len(programas_comparar)/2 + 0.5) * width
    ax.bar(x + offset, tiempos, width,
           label=nombres_programas[programa],
           color=colores[programa])

# Línea horizontal para el tiempo serial
ax.axhline(y=tiempo_serial, color=colores['01_pi_serial'],
           linestyle='--', linewidth=2, label='Serial (referencia)', alpha=0.7)

ax.set_xlabel('Número de Hilos', fontsize=12, fontweight='bold')
ax.set_ylabel('Tiempo de Ejecución (segundos)', fontsize=12, fontweight='bold')
ax.set_title('Comparativa de Tiempo por Estrategia (10M iteraciones)\n(Excluyendo Busy-Wait Ineficiente para mejor visualización)',
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(hilos_vals)
ax.legend(fontsize=11, loc='upper right')
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('grafico_3_comparativa_barras.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# GRÁFICO 4: Eficiencia Paralela (10M iteraciones)
# ============================================================
print("4. Eficiencia Paralela...")

fig, ax = plt.subplots(figsize=(12, 8))

# Eficiencia ideal = 100%
ax.axhline(y=100, color='black', linestyle='--', linewidth=2, label='Eficiencia Ideal (100%)', alpha=0.5)

for programa in ['02_pi_parallel_race', '04_pi_parallel_busy_cs', '05_pi_parallel_mutex']:
    eficiencias = []
    hilos_list = []

    for hilos in range(1, 7):
        data = df_10M[(df_10M['programa'] == programa) & (df_10M['hilos'] == hilos)]
        if not data.empty:
            tiempo = data['tiempo_segundos'].values[0]
            speedup = tiempo_serial / tiempo
            eficiencia = (speedup / hilos) * 100
            eficiencias.append(eficiencia)
            hilos_list.append(hilos)

    ax.plot(hilos_list, eficiencias,
            marker='o', linewidth=2, markersize=8,
            label=nombres_programas[programa],
            color=colores[programa])

ax.set_xlabel('Número de Hilos', fontsize=12, fontweight='bold')
ax.set_ylabel('Eficiencia (%)', fontsize=12, fontweight='bold')
ax.set_title('Eficiencia Paralela vs Número de Hilos (10M iteraciones)',
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(range(1, 7))
ax.set_ylim(0, 120)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('grafico_4_eficiencia_paralela.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# GRÁFICO 5: Overhead de Paralelización (iteraciones bajas)
# ============================================================
print("5. Overhead de Paralelización...")

# Filtrar iteraciones bajas
df_bajo = df[df['iteraciones'] <= 10000].copy()

fig, ax = plt.subplots(figsize=(14, 8))

iteraciones_vals = sorted(df_bajo['iteraciones'].unique())
programas_comparar = ['01_pi_serial', '02_pi_parallel_race',
                      '04_pi_parallel_busy_cs', '05_pi_parallel_mutex']

x = np.arange(len(iteraciones_vals))
width = 0.2

for i, programa in enumerate(programas_comparar):
    tiempos = []
    for iter_val in iteraciones_vals:
        data = df_bajo[(df_bajo['programa'] == programa) & (df_bajo['iteraciones'] == iter_val)]
        if not data.empty:
            # Promediar sobre todos los hilos
            tiempo_promedio = data['tiempo_segundos'].mean()
            # Convertir a microsegundos para mejor visualización
            tiempos.append(tiempo_promedio * 1000000)
        else:
            tiempos.append(0)

    offset = (i - len(programas_comparar)/2 + 0.5) * width
    ax.bar(x + offset, tiempos, width,
           label=nombres_programas[programa],
           color=colores[programa])

ax.set_xlabel('Número de Iteraciones', fontsize=12, fontweight='bold')
ax.set_ylabel('Tiempo de Ejecución Promedio (microsegundos)', fontsize=12, fontweight='bold')
ax.set_title('Overhead de Paralelización con Pocas Iteraciones\n(Promedio de todos los hilos - en microsegundos)',
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels([f'{int(i):,}' for i in iteraciones_vals])
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('grafico_5_overhead_paralelizacion.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# GRÁFICO EXTRA: Desastre del Busy-Wait Ineficiente
# ============================================================
print("6. BONUS: Desastre Busy-Wait Ineficiente...")

# Filtrar solo versión 3 vs serial y mutex
df_comparacion = df[df['programa'].isin(['01_pi_serial', '03_pi_parallel_busy', '05_pi_parallel_mutex'])].copy()

fig, ax = plt.subplots(figsize=(12, 8))

for programa in ['01_pi_serial', '05_pi_parallel_mutex']:
    data = df_comparacion[df_comparacion['programa'] == programa].groupby('iteraciones')['tiempo_segundos'].mean()
    ax.plot(data.index, data.values,
            marker='o', linewidth=2, markersize=6,
            label=nombres_programas[programa],
            color=colores[programa])

# Versión 3 con línea especial
data_v3 = df_comparacion[df_comparacion['programa'] == '03_pi_parallel_busy'].groupby('iteraciones')['tiempo_segundos'].mean()
ax.plot(data_v3.index, data_v3.values,
        marker='X', linewidth=3, markersize=10,
        label=nombres_programas['03_pi_parallel_busy'] + ' (¡DESASTRE!)',
        color=colores['03_pi_parallel_busy'],
        linestyle='--')

ax.set_xlabel('Número de Iteraciones', fontsize=12, fontweight='bold')
ax.set_ylabel('Tiempo de Ejecución', fontsize=12, fontweight='bold')
ax.set_title('El Desastre del Busy-Wait dentro del Bucle',
             fontsize=14, fontweight='bold', pad=20)
ax.set_xscale('log')
ax.set_yscale('log')

# Mejorar etiquetas del eje X
ax.set_xticks([1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000, 2000000, 5000000, 10000000])
ax.set_xticklabels(['1K', '2K', '5K', '10K', '20K', '50K', '100K', '200K', '500K', '1M', '2M', '5M', '10M'], rotation=45)

# Formatear eje Y
ax.yaxis.set_major_formatter(FuncFormatter(format_time))

ax.legend(loc='upper left', fontsize=11)
ax.grid(True, alpha=0.3)

# Anotación
ax.annotate('¡2.68s vs 0.049s!\n(54x más lento)',
            xy=(10000000, 2.68), xytext=(1000000, 10),
            arrowprops=dict(arrowstyle='->', color='red', lw=2),
            fontsize=12, color='red', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))

plt.tight_layout()
plt.savefig('grafico_6_desastre_busy_wait.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n" + "="*50)
print("✅ ¡Gráficos generados exitosamente!")
print("="*50)
print("\nArchivos creados:")
print("  1. grafico_1_tiempo_vs_iteraciones.png")
print("  2. grafico_2_speedup_vs_hilos.png")
print("  3. grafico_3_comparativa_barras.png")
print("  4. grafico_4_eficiencia_paralela.png")
print("  5. grafico_5_overhead_paralelizacion.png")
print("  6. grafico_6_desastre_busy_wait.png (BONUS)")
print("="*50)
