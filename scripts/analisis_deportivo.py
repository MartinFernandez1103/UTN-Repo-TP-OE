import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Importar el archivo con resultados de partidos
df = pd.read_csv("datos/resultados_partidos.csv")

# Inicializar un diccionario para registrar las estadísticas
estadisticas = {}

def inicializar_equipo(equipo):
    if equipo not in estadisticas:
        estadisticas[equipo] = {"Ganados": 0, "Empatados": 0, "Perdidos": 0, "Goles_Favor": 0, "Puntos": 0}

# 2. Procesar los resultados para calcular partidos ganados y tabla de posiciones
for _, fila in df.iterrows():
    local, visitante = fila['equipo_local'], fila['equipo_visitante']
    g_local, g_visitante = int(fila['goles_local']), int(fila['goles_visitante'])
    
    inicializar_equipo(local)
    inicializar_equipo(visitante)
    
    estadisticas[local]["Goles_Favor"] += g_local
    estadisticas[visitante]["Goles_Favor"] += g_visitante
    
    if g_local > g_visitante:
        estadisticas[local]["Ganados"] += 1
        estadisticas[local]["Puntos"] += 3
        estadisticas[visitante]["Perdidos"] += 1
    elif g_local < g_visitante:
        estadisticas[visitante]["Ganados"] += 1
        estadisticas[visitante]["Puntos"] += 3
        estadisticas[local]["Perdidos"] += 1
    else:
        estadisticas[local]["Empatados"] += 1
        estadisticas[local]["Puntos"] += 1
        estadisticas[visitante]["Empatados"] += 1
        estadisticas[visitante]["Puntos"] += 1

#Convertir a DataFrame para ordenar la tabla de posiciones
tabla_posiciones = pd.DataFrame.from_dict(estadisticas, orient='index').sort_values(by="Puntos", ascending=False)

#3. Calcular el promedio de goles por partido global
total_partidos = len(df)
total_goles = df['goles_local'].sum() + df['goles_visitante'].sum()
promedio_goles = total_goles / total_partidos

#Mostrar resultados en consola
print("=== TABLA DE POSICIONES FINAL ===")
print(tabla_posiciones[["Puntos", "Ganados", "Goles_Favor"]])
print(f"\nPromedio global de goles por partido: {promedio_goles:.2f}")

#4. Generar un gráfico comparativo de rendimiento (Puntos por Equipo)
plt.figure(figsize=(8, 5))
plt.bar(tabla_posiciones.index, tabla_posiciones['Puntos'], color=['blue', 'red', 'lightblue', 'red', 'green'])
plt.title('Rendimiento de los Equipos (Puntos en el Torneo)')
plt.xlabel('Equipos')
plt.ylabel('Puntos Totales')
plt.grid(axis='y', linestyle='--', alpha=0.7)

#Asegurar que se guarde el gráfico en la carpeta /resultados
os.makedirs("resultados", exist_ok=True)
plt.savefig("resultados/grafico_rendimiento.png")
print("\n¡Gráfico guardado con éxito en /resultados/grafico_rendimiento.png!")
