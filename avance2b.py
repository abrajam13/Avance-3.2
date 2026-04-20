import streamlit as st
import numpy as np
from collections import deque
import time
import re
import heapq  # Necesario para A*

# Implementación de BFS
def solve_maze_bfs(maze, start, end):
    start_time = time.time()
    queue = deque([(start, [start])])
    visited = {start}
    while queue:
        (r, c), path = queue.popleft()
        if (r, c) == end:
            return path, len(path), (time.time() - start_time)
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]:
                if maze[nr, nc] != 1 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), path + [(nr, nc)]))
    return None, 0, 0

# Implementación de DFS
def solve_maze_dfs(maze, start, end):
    start_time = time.time()
    stack = [(start, [start])]
    visited = {start}
    while stack:
        (r, c), path = stack.pop()
        if (r, c) == end:
            return path, len(path), (time.time() - start_time)
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]:
                if maze[nr, nc] != 1 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    stack.append(((nr, nc), path + [(nr, nc)]))
    return None, 0, 0

# Implementación de A* (A Estrella)
def solve_maze_astar(maze, start, end):
    start_time = time.time()
    # Heurística: Distancia de Manhattan
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # priority_queue guarda: (prioridad, posicion_actual, camino_recorrido)
    pq = [(0 + heuristic(start, end), 0, start, [start])]
    visited = {start: 0} # Guardamos el costo g (pasos dados)

    while pq:
        f, g, (r, c), path = heapq.heappop(pq)

        if (r, c) == end:
            return path, len(path), (time.time() - start_time)

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1] and maze[nr, nc] != 1:
                new_g = g + 1
                if nr not in visited or new_g < visited[(nr, nc)]:
                    visited[(nr, nc)] = new_g
                    f = new_g + heuristic((nr, nc), end)
                    heapq.heappush(pq, (f, new_g, (nr, nc), path + [(nr, nc)]))
    return None, 0, 0

def render_maze(maze, start, end, path=None):
    if path is None: path = []
    display_maze = []
    for r_idx, row in enumerate(maze):
        display_row = []
        for c_idx, col in enumerate(row):
            pos = (r_idx, c_idx)
            if pos == start: display_row.append("🚀")
            elif pos == end: display_row.append("🏁")
            elif pos in path: display_row.append("🟦")
            elif col == 1: display_row.append("⬛")
            else: display_row.append("⬜")
        display_maze.append("".join(display_row))
    st.markdown(f"```\n{chr(10).join(display_maze)}\n```")

st.title("Visualizador de Algoritmo de Búsqueda")
st.sidebar.header("Carga de Datos")
archivo = st.sidebar.file_uploader("Sube tu laberinto (.txt)", type=["txt"])
algorithm = st.sidebar.selectbox("Algoritmo", ["BFS", "DFS", "A*"])
solve_button = st.sidebar.button("Resolver Laberinto")

if archivo:
    content = archivo.read().decode("utf-8")
    lines = content.strip().split('\n')
    maze_data = [[int(d) for d in re.findall(r'\d', line)] for line in lines if re.findall(r'\d', line)]
    maze_np = np.array(maze_data)
    p2, p3 = np.where(maze_np == 2), np.where(maze_np == 3)

    if p2[0].size > 0 and p3[0].size > 0:
        START, END = (p2[0][0], p2[1][0]), (p3[0][0], p3[1][0])
        if solve_button:
            if algorithm == "BFS": path, num_casillas, tiempo = solve_maze_bfs(maze_np, START, END)
            elif algorithm == "DFS": path, num_casillas, tiempo = solve_maze_dfs(maze_np, START, END)
            elif algorithm == "A*": path, num_casillas, tiempo = solve_maze_astar(maze_np, START, END)
            
            if path:
                st.success(f"¡{algorithm} completado! Pasos: **{num_casillas}** | Tiempo: **{tiempo:.6f}s**")
                render_maze(maze_np, START, END, path)
            else: st.error("No se encontró ruta.")
        else: render_maze(maze_np, START, END)
    else: st.warning("Falta inicio (2) o meta (3).")
else: st.info("Sube tu archivo .txt.")
