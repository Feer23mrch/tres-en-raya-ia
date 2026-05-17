import pygame
import sys
import math

# -------------------------------
# Representación del estado
# -------------------------------
# El tablero es una lista de 9 elementos: "X", "O" o None (vacío)
# Índices: 0 1 2
#          3 4 5
#          6 7 8
initial_state = [None] * 9

# -------------------------------
# Funciones requeridas
# -------------------------------
def player(state):
    """Devuelve qué jugador tiene el turno ('X' o 'O')."""
    # X siempre empieza
    count_x = state.count("X")
    count_o = state.count("O")
    if count_x == count_o:
        return "X"
    else:
        return "O"

def actions(state):
    """Devuelve una lista de índices vacíos (movimientos legales)."""
    return [i for i, cell in enumerate(state) if cell is None]

def result(state, action):
    """Devuelve un nuevo estado tras aplicar la acción (índice) en el estado actual."""
    if state[action] is not None:
        raise ValueError("Movimiento inválido")
    new_state = state[:]  # copia
    new_state[action] = player(state)
    return new_state

def terminal(state):
    """Verifica si el juego ha terminado (ganador o empate)."""
    return winner(state) is not None or all(cell is not None for cell in state)

def utility(state):
    """
    Valor numérico para estados terminales.
    1 si gana X, -1 si gana O, 0 si empate.
    """
    win = winner(state)
    if win == "X":
        return 1
    elif win == "O":
        return -1
    else:
        return 0

# Función auxiliar para determinar el ganador
def winner(state):
    """Devuelve 'X', 'O' o None."""
    lines = [
        [0,1,2], [3,4,5], [6,7,8],  # filas
        [0,3,6], [1,4,7], [2,5,8],  # columnas
        [0,4,8], [2,4,6]            # diagonales
    ]
    for line in lines:
        a, b, c = line
        if state[a] and state[a] == state[b] == state[c]:
            return state[a]
    return None

# -------------------------------
# Algoritmo Minimax
# -------------------------------
def minimax_decision(state):
    """
    Dado un estado (turno del jugador actual), devuelve la mejor acción para MAX (X).
    """
    current_player = player(state)
    best_action = None
    if current_player == "X":  # MAX
        best_value = -math.inf
        for action in actions(state):
            value = min_value(result(state, action))
            if value > best_value:
                best_value = value
                best_action = action
    else:  # MIN (O) – pero aquí solo llamamos para la IA (O), aunque la IA también usa minimax)
        # En realidad el humano puede ser X y la IA O; entonces la IA llama minimax para MIN.
        best_value = math.inf
        for action in actions(state):
            value = max_value(result(state, action))
            if value < best_value:
                best_value = value
                best_action = action
    return best_action

def max_value(state):
    if terminal(state):
        return utility(state)
    v = -math.inf
    for action in actions(state):
        v = max(v, min_value(result(state, action)))
    return v

def min_value(state):
    if terminal(state):
        return utility(state)
    v = math.inf
    for action in actions(state):
        v = min(v, max_value(result(state, action)))
    return v

# -------------------------------
# Interfaz gráfica con Pygame
# -------------------------------
# Constantes
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 5
CELL_SIZE = WIDTH // 3
RADIUS = CELL_SIZE // 3
CROSS_WIDTH = 15

# Colores
BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
X_COLOR = (0, 0, 255)
O_COLOR = (255, 0, 0)
TEXT_COLOR = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tres en Raya - Minimax")
font = pygame.font.SysFont("Arial", 40)

def draw_board(state):
    screen.fill(BG_COLOR)
    # Líneas divisorias
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)
    # Dibujar X y O
    for idx, cell in enumerate(state):
        row, col = idx // 3, idx % 3
        center_x = col * CELL_SIZE + CELL_SIZE // 2
        center_y = row * CELL_SIZE + CELL_SIZE // 2
        if cell == "X":
            offset = CELL_SIZE // 4
            pygame.draw.line(screen, X_COLOR, (center_x - offset, center_y - offset),
                             (center_x + offset, center_y + offset), CROSS_WIDTH)
            pygame.draw.line(screen, X_COLOR, (center_x + offset, center_y - offset),
                             (center_x - offset, center_y + offset), CROSS_WIDTH)
        elif cell == "O":
            pygame.draw.circle(screen, O_COLOR, (center_x, center_y), RADIUS, CROSS_WIDTH)
    pygame.display.flip()

def show_message(text):
    screen.fill(BG_COLOR)
    label = font.render(text, True, TEXT_COLOR)
    screen.blit(label, (WIDTH//2 - label.get_width()//2, HEIGHT//2 - label.get_height()//2))
    pygame.display.flip()
    pygame.time.wait(2000)

def get_clicked_cell(pos):
    x, y = pos
    if x < CELL_SIZE:
        col = 0
    elif x < 2 * CELL_SIZE:
        col = 1
    else:
        col = 2
    if y < CELL_SIZE:
        row = 0
    elif y < 2 * CELL_SIZE:
        row = 1
    else:
        row = 2
    return row * 3 + col

def main():
    state = initial_state[:]
    game_over = False
    human_player = "X"   # El humano juega con X
    ai_player = "O"

    # Si la IA empieza (si humano es 'O', pero aquí humano es X y empieza X)
    # No es necesario mover IA primero.

    running = True
    while running:
        draw_board(state)

        if not game_over and terminal(state):
            game_over = True
            win = winner(state)
            if win == human_player:
                show_message("¡Ganaste!")
            elif win == ai_player:
                show_message("Gana la IA...")
            else:
                show_message("Empate")
            # Reiniciar después de 2 segundos
            state = initial_state[:]
            game_over = False
            continue

        # Turno del humano (X)
        if not game_over and player(state) == human_player:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    cell = get_clicked_cell(pygame.mouse.get_pos())
                    if cell in actions(state):
                        state = result(state, cell)
        # Turno de la IA (O)
        elif not game_over and player(state) == ai_player:
            # Pequeña pausa para que se vea el movimiento humano
            pygame.time.wait(200)
            action = minimax_decision(state)
            if action is not None:
                state = result(state, action)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()