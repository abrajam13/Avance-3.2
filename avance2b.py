import streamlit as st
import numpy as np
from collections import deque
import re

# Función de resolución integrada para que el código sea funcional
def solve_maze_bfs(maze, start, end):
    queue = deque([(start, [start])])
    visited = {start}
    while queue:
        (r, c), path = queue.popleft()
        if (r, c) == end:
            return path, len(path)
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]:
                if maze[nr, nc] != 1 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), path + [(nr, nc)]))
    return None, 0

def render_maze(maze, start, end, path=None):
    if path is None:
        path = []
    
    display_maze = []
    for r_idx, row in enumerate(maze):
        display_row = []
        for c_idx, col in enumerate(row):
            pos = (r_idx, c_idx)
            if pos == start:
                display_row.append("🚀")
            elif pos == end:
                display_row.append("🏁")
            elif pos in path:
                display_row.append("🟦")
            elif col == 1:
                display_row.append("⬛")
            else:
                display_row.append("⬜")
        display_maze.append("".join(display_row))
    
    maze_str = "\n".join(display_maze)
    st.markdown(f"```\n{maze_str}\n```")

st.title("Visualizador de Algoritmo de Búsqueda")

# Configuración en Sidebar
st.sidebar.header("Carga de Datos")
archivo = st.sidebar.file_uploader("Sube tu laberinto (.txt)", type=["txt"])
algorithm = st.sidebar.selectbox("Algoritmo", ["BFS", "DFS", "A*"])
solve_button = st.sidebar.button("Resolver Laberinto")

if archivo:
    # Procesamiento del archivo
    content = archivo.read().decode("utf-8")
    lines = content.strip().split('\n')
    maze_data = [[int(d) for d in re.findall(r'\d', line)] for line in lines if re.findall(r'\d', line)]
    maze_np = np.array(maze_data)
    
    # Localización dinámica de inicio (2) y fin (3)
    p2 = np.where(maze_np == 2)
    p3 = np.where(maze_np == 3)

    if p2[0].size > 0 and p3[0].size > 0:
        START = (p2[0][0], p2[1][0])
        END = (p3[0][0], p3[1][0])

        if solve_button:
            if algorithm == "BFS":
                path, num_casillas = solve_maze_bfs(maze_np, START, END)
                if path:
                    st.success(f"¡Camino encontrado! Casillas totales: **{num_casillas}**")
                    render_maze(maze_np, START, END, path)
                else:
                    st.error("No se encontró una ruta posible.")
            else:
                st.warning(f"El algoritmo {algorithm} aún no ha sido implementado.")
        else:
            # Renderizado inicial del laberinto cargado
            render_maze(maze_np, START, END)
    else:
        st.warning("El archivo debe contener un '2' (inicio) y un '3' (meta).")
else:
    st.info("Por favor, sube un archivo .txt para visualizar el laberinto.")
