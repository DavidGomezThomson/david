import matplotlib.pyplot as plt

# -------------------- ALGORITMO N-REINAS --------------------

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


# -------------------- SIMETRÍAS --------------------

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
    return [sol, r90, r180, r270, refl, refl90, refl180, refl270]

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


# -------------------- DIBUJO DEL TABLERO --------------------

def dibujar_tablero(ax, sol, n):
    # Dibujar casillas del tablero
    for i in range(n):
        for j in range(n):
            color = "#f0d9b5" if (i + j) % 2 == 0 else "#b58863"
            ax.add_patch(plt.Rectangle((j, n - 1 - i), 1, 1, color=color))

    # Ajustar tamaño de la reina proporcional al tablero
    factor = 155  # Ajusta este número para que quede más grande o más pequeño
    fontsize = max(8, factor / n)

    # Dibujar reinas con ♛
    for fila in range(n):
        col = sol[fila]
        ax.text(
            col + 0.5,
            n - 1 - fila + 0.425,
            "♛",
            fontsize=fontsize,
            ha="center",
            va="center",
            color="black"
        )

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_aspect("equal")
