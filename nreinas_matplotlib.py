import matplotlib.pyplot as plt
import numpy as np

# -------------------- Resolver N-Reinas --------------------

def es_seguro(tablero, fila, col):
    for i in range(fila):
        if tablero[i] == col or abs(tablero[i] - col) == abs(i - fila):
            return False
    return True

def resolver_rec(n, fila, tablero, soluciones):
    if fila == n:
        soluciones.append(tablero.copy())
        return
    for col in range(n):
        if es_seguro(tablero, fila, col):
            tablero[fila] = col
            resolver_rec(n, fila + 1, tablero, soluciones)

def n_reinas(n):
    tablero = [-1] * n
    soluciones = []
    resolver_rec(n, 0, tablero, soluciones)
    return soluciones

# -------------------- Simetrías --------------------

def rotar90(sol):
    n = len(sol)
    r = [0] * n
    for fila, col in enumerate(sol):
        r[col] = n - 1 - fila
    return r

def reflejar(sol):
    n = len(sol)
    return [n - 1 - c for c in sol]

def generar_simetrias(sol):
    r90 = rotar90(sol)
    r180 = rotar90(r90)
    r270 = rotar90(r180)
    refl = reflejar(sol)
    refl90 = rotar90(refl)
    refl180 = rotar90(refl90)
    refl270 = rotar90(refl180)
    return [sol, r90, r180, r270,
            refl, refl90, refl180, refl270]

def es_nueva(sol, unicas):
    for u in unicas:
        if any(s == u for s in generar_simetrias(sol)):
            return False
    return True

def filtrar_unicas(soluciones):
    unicas = []
    for sol in soluciones:
        if es_nueva(sol, unicas):
            unicas.append(sol)
    return unicas

# -------------------- DIBUJO DE LA REINA --------------------

def dibujar_reina(ax, x, y, tamaño):
    ax.plot([x+0.25*tamaño, x+0.15*tamaño, x+0.40*tamaño,
             x+0.50*tamaño, x+0.60*tamaño,
             x+0.85*tamaño, x+0.75*tamaño],
            [y+0.65*tamaño, y+0.90*tamaño, y+0.80*tamaño,
             y+0.95*tamaño, y+0.80*tamaño,
             y+0.90*tamaño, y+0.65*tamaño],
            color="black", linewidth=2)

    circ = plt.Circle((x + 0.50*tamaño, y + 0.55*tamaño), tamaño*0.18, color='black')
    ax.add_patch(circ)

    ax.add_patch(plt.Rectangle((x + 0.20*tamaño, y + 0.20*tamaño),
                               tamaño*0.60, tamaño*0.15, color="black"))

# -------------------- DIBUJADO DE TABLEROS --------------------

def dibujar_tablero(ax, sol, n):
    for i in range(n):
        for j in range(n):
            color = "white" if (i + j) % 2 == 0 else "gray"
            ax.add_patch(plt.Rectangle((j, n-1-i), 1, 1, color=color))

    for i in range(n):
        dibujar_reina(ax, sol[i], n-1-i, 1)

    ax.add_patch(plt.Rectangle((0, 0), n, n,
                               fill=False, linewidth=3, edgecolor="black"))

    ax.set_xticks(np.arange(n) + 0.5)
    ax.set_xticklabels([str(i) for i in range(n)])
    ax.set_yticks(np.arange(n) + 0.5)
    ax.set_yticklabels([str(n-1-i) for i in range(n)])

    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_aspect("equal")
    ax.tick_params(length=0, pad=8)
    ax.grid(False)

# -------------------- MOSTRAR TODAS LAS SOLUCIONES CON PAGINACIÓN --------------------

def mostrar_todas(soluciones, n, por_pagina=12):
    sol_count = len(soluciones)

    for start in range(0, sol_count, por_pagina):
        end = min(start + por_pagina, sol_count)
        subset = soluciones[start:end]
        num = len(subset)

        # Calcular columnas y filas óptimas
        columnas = min(4, num)  # máximo 4 columnas
        filas = (num + columnas - 1) // columnas

        # Tamaño por celda
        cell_size = 5
        fig, axs = plt.subplots(filas, columnas,
                                figsize=(columnas * cell_size, filas * cell_size))
        axs = np.array(axs).reshape(filas, columnas)

        for idx, sol in enumerate(subset):
            r = idx // columnas
            c = idx % columnas
            ax = axs[r, c]
            dibujar_tablero(ax, sol, n)
            ax.set_title(f"Solución {start + idx + 1}", fontsize=12)

        # Ocultar subplots vacíos
        for idx in range(num, filas * columnas):
            axs[idx // columnas, idx % columnas].axis("off")

        plt.tight_layout(pad=3)
        plt.show()



# -------------------- MAIN --------------------

def main():
    n = int(input("Introduce N (ej: 4, 5, 8): "))
    soluciones = n_reinas(n)
    unicas = filtrar_unicas(soluciones)

    print(f"\nSoluciones totales: {len(soluciones)}")
    print(f"Soluciones distintas (sin simetrías): {len(unicas)}")

    modo = input("Modo (1=todas en grid, 2=animadas): ")

    if modo == "2":
        animar_soluciones(unicas, n)
    else:
        mostrar_todas(unicas, n)

if __name__ == "__main__":
    main()
