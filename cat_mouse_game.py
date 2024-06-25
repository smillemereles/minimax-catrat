import tkinter as tk  # Importar la biblioteca tkinter para la interfaz gráfica
import math  # Importar el módulo math para operaciones matemáticas
import random  # Importar el módulo random para generar números aleatorios

# Definir el tamaño del tablero
TAMAÑO_TABLERO = 7  # Tamaño del tablero cuadrado (7x7 en este caso)

# Crear el tablero y establecer las posiciones iniciales
tablero = [[0 for _ in range(TAMAÑO_TABLERO)] for _ in range(TAMAÑO_TABLERO)]
fila_gato, col_gato = 1, 1  # Posición inicial del gato
fila_raton, col_raton = TAMAÑO_TABLERO - 2, TAMAÑO_TABLERO - 2  # Posición inicial del ratón
fila_salida, col_salida = TAMAÑO_TABLERO - 1, 0  # Posición de la salida

# Establecer los límites y la posición de la salida en el tablero
for fila in range(TAMAÑO_TABLERO):
    for col in range(TAMAÑO_TABLERO):
        if (fila == 0 and col > 0) or (col == 0 and fila > 0) or fila == TAMAÑO_TABLERO - 1 or col == TAMAÑO_TABLERO - 1:
            if (fila, col) != (TAMAÑO_TABLERO - 2, TAMAÑO_TABLERO - 1) and (fila, col) != (fila_salida, col_salida):
                tablero[fila][col] = -1  # Marcar como límite en el tablero

# Función para verificar si un movimiento es válido
def es_movimiento_valido(fila, col):
    return 0 <= fila < TAMAÑO_TABLERO and 0 <= col < TAMAÑO_TABLERO and tablero[fila][col] != -1

# Función para obtener los movimientos posibles desde una posición dada
def obtener_movimientos_posibles(fila, col):
    movimientos = []
    for df, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]:  # Incluir quedarse en el mismo lugar
        nueva_fila, nueva_col = fila + df, col + dc
        if es_movimiento_valido(nueva_fila, nueva_col):
            movimientos.append((nueva_fila, nueva_col))
    return movimientos

# Función para evaluar la posición actual del juego con equilibrio entre el gato y el ratón
def evaluar_posicion_equilibrada(fila_gato, col_gato, fila_raton, col_raton):
    distancia_gato_raton = abs(fila_gato - fila_raton) + abs(col_gato - col_raton)
    distancia_raton_salida = abs(fila_raton - fila_salida) + abs(col_raton - col_salida)
    
    # Calcular el puntaje del gato
    puntuacion_gato = -2 * distancia_gato_raton
    
    # Calcular el puntaje del ratón con una ponderación para llegar a la salida
    puntuacion_raton = distancia_gato_raton - 2 * distancia_raton_salida
    
    # Equilibrar los puntajes del ratón para que busque la salida con más urgencia
    puntuacion_raton += 3 * (TAMAÑO_TABLERO - fila_raton - col_raton) / (TAMAÑO_TABLERO - 2)
    
    return puntuacion_gato if fila_gato == col_gato else puntuacion_raton

# Implementar el algoritmo minimax con poda alfa-beta
def minimax(es_gato, profundidad, fila_gato, col_gato, fila_raton, col_raton, alfa, beta, max_profundidad=4):
    if profundidad == 0 or (fila_gato, col_gato) == (fila_raton, col_raton) or (fila_raton, col_raton) == (fila_salida, col_salida):
        return evaluar_posicion_equilibrada(fila_gato, col_gato, fila_raton, col_raton)

    if es_gato:
        mejor_puntuacion = -math.inf
        movimientos_posibles = obtener_movimientos_posibles(fila_gato, col_gato)
        for nueva_fila, nueva_col in movimientos_posibles:
            puntuacion = minimax(False, profundidad - 1, nueva_fila, nueva_col, fila_raton, col_raton, alfa, beta, max_profundidad)
            mejor_puntuacion = max(mejor_puntuacion, puntuacion)
            alfa = max(alfa, mejor_puntuacion)
            if beta <= alfa:
                break
        return mejor_puntuacion
    else:
        mejor_puntuacion = math.inf
        movimientos_posibles = obtener_movimientos_posibles(fila_raton, col_raton)
        for nueva_fila, nueva_col in movimientos_posibles:
            puntuacion = minimax(True, profundidad - 1, fila_gato, col_gato, nueva_fila, nueva_col, alfa, beta, max_profundidad)
            mejor_puntuacion = min(mejor_puntuacion, puntuacion)
            beta = min(beta, mejor_puntuacion)
            if beta <= alfa:
                break
        return mejor_puntuacion

# Estrategia para el ratón (modificada)
def estrategia_raton(fila_raton, col_raton, fila_gato, col_gato):
    movimientos_posibles = obtener_movimientos_posibles(fila_raton, col_raton)
    if not movimientos_posibles:
        return (fila_raton, col_raton)
    
    # Probabilidad de hacer un movimiento aleatorio
    if random.random() < 0.1:  # 10% de probabilidad de movimiento aleatorio
        return random.choice(movimientos_posibles)
    
    mejores_movimientos = []
    mejor_valor = -math.inf
    
    for movimiento in movimientos_posibles:
        nueva_fila, nueva_col = movimiento
        valor_movimiento = minimax(True, 3, fila_gato, col_gato, nueva_fila, nueva_col, -math.inf, math.inf)
        if valor_movimiento > mejor_valor:
            mejor_valor = valor_movimiento
            mejores_movimientos = [movimiento]
        elif valor_movimiento == mejor_valor:
            mejores_movimientos.append(movimiento)
    
    # Añadir un factor de exploración
    for movimiento in movimientos_posibles:
        if random.random() < 0.2:  # 20% de probabilidad de considerar otros movimientos
            mejores_movimientos.append(movimiento)
    
    return random.choice(mejores_movimientos)

# Estrategia para el gato (modificada)
def estrategia_gato(fila_gato, col_gato, fila_raton, col_raton):
    movimientos_posibles = obtener_movimientos_posibles(fila_gato, col_gato)
    if not movimientos_posibles:
        return (fila_gato, col_gato)
    
    # Probabilidad de hacer un movimiento aleatorio
    if random.random() < 0.05:  # 5% de probabilidad de movimiento aleatorio
        return random.choice(movimientos_posibles)
    
    mejores_movimientos = []
    mejor_valor = -math.inf
    
    for movimiento in movimientos_posibles:
        nueva_fila, nueva_col = movimiento
        distancia = abs(nueva_fila - fila_raton) + abs(nueva_col - col_raton)
        valor_movimiento = minimax(False, 4, nueva_fila, nueva_col, fila_raton, col_raton, -math.inf, math.inf)
        valor_ajustado = valor_movimiento - distancia
        if valor_ajustado > mejor_valor:
            mejor_valor = valor_ajustado
            mejores_movimientos = [movimiento]
        elif valor_ajustado == mejor_valor:
            mejores_movimientos.append(movimiento)
    
    # Añadir un factor de exploración
    for movimiento in movimientos_posibles:
        if random.random() < 0.15:  # 15% de probabilidad de considerar otros movimientos
            mejores_movimientos.append(movimiento)
    
    return random.choice(mejores_movimientos)

# Función para verificar si el juego ha terminado
def juego_terminado(fila_gato, col_gato, fila_raton, col_raton):
    if (fila_raton, col_raton) == (fila_salida, col_salida):
        return "¡El ratón ha escapado y ganado!"
    elif (fila_gato, col_gato) == (fila_raton, col_raton):
        return "¡El gato ha atrapado al ratón y ganado!"
    elif len(obtener_movimientos_posibles(fila_gato, col_gato)) <= 1 and len(obtener_movimientos_posibles(fila_raton, col_raton)) <= 1:
        return "¡El juego ha terminado en empate!"
    return None

# Función para dibujar el tablero en tkinter
def dibujar_tablero(lienzo, tamaño_celda):
    lienzo.delete("all")
    for fila in range(TAMAÑO_TABLERO):
        for col in range(TAMAÑO_TABLERO):
            x0, y0 = col * tamaño_celda, fila * tamaño_celda
            x1, y1 = x0 + tamaño_celda, y0 + tamaño_celda
            if (fila, col) == (fila_gato, col_gato):
                lienzo.create_rectangle(x0, y0, x1, y1, fill="orange")  # Color naranja para el gato
            elif (fila, col) == (fila_raton, col_raton):
                lienzo.create_rectangle(x0, y0, x1, y1, fill="gray")  # Color gris para el ratón
            elif (fila, col) == (fila_salida, col_salida):
                lienzo.create_rectangle(x0, y0, x1, y1, fill="green")  # Color verde para la salida
            elif tablero[fila][col] == -1:
                lienzo.create_rectangle(x0, y0, x1, y1, fill="black")  # Color negro para los límites
            else:
                lienzo.create_rectangle(x0, y0, x1, y1, fill="white")  # Celdas vacías en blanco

# Inicializar tkinter y crear la ventana
raiz = tk.Tk()
raiz.title("Juego de Gato y Ratón")
lienzo = tk.Canvas(raiz, width=400, height=400)
lienzo.pack()
tamaño_celda = 400 // TAMAÑO_TABLERO

# Función para manejar los turnos del juego
def jugar_turno():
    global fila_gato, col_gato, fila_raton, col_raton

    # Movimiento del gato basado en la estrategia minimax
    movimiento_gato = estrategia_gato(fila_gato, col_gato, fila_raton, col_raton)
    if movimiento_gato:
        fila_gato, col_gato = movimiento_gato

    # Movimiento del ratón basado en la estrategia minimax
    movimiento_raton = estrategia_raton(fila_raton, col_raton, fila_gato, col_gato)
    if movimiento_raton:
        fila_raton, col_raton = movimiento_raton

    # Imprimir las posiciones actuales
    print(f"Posición del gato: ({fila_gato}, {col_gato}), Posición del ratón: ({fila_raton}, {col_raton})")

    # Dibujar el tablero actualizado
    dibujar_tablero(lienzo, tamaño_celda)

    # Verificar si el juego ha terminado
    estado_juego = juego_terminado(fila_gato, col_gato, fila_raton, col_raton)
    if not estado_juego:
        raiz.after(1000, jugar_turno)  # Esperar un segundo y continuar con el siguiente turno
    else:
        print(estado_juego)  # Imprimir el estado del juego (quién ganó o si hubo empate)
        print("¡Fin del juego!")

# Dibujar el tablero inicial
dibujar_tablero(lienzo, tamaño_celda)

# Iniciar el juego llamando a la función jugar_turno()
jugar_turno()

# Ejecutar el bucle principal de tkinter
raiz.mainloop()
