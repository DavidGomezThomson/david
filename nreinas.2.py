from PIL import Image, ImageDraw, ImageFont

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

    return [
        sol, r90, r180, r270,
        refl, refl90, refl180, refl270
    ]

def es_nueva(sol, unicas):
    for u in unicas:
        for s in generar_simetrias(sol):
            if s == u:
                return False
    return True

def filtrar_unicas(soluciones):
    unicas = []
    for sol in soluciones:
        if es_nueva(sol, unicas):
            unicas.append(sol)
    return unicas


# -------------------- DIBUJAR REINA --------------------

def dibujar_reina(draw, x, y, tamaño):
    cx = x + tamaño // 2

    # corona (tres puntas)
    draw.polygon([
        (cx - tamaño*0.25, y + tamaño*0.35),
        (cx - tamaño*0.35, y + tamaño*0.10),
        (cx - tamaño*0.10, y + tamaño*0.20),
        (cx,             y + tamaño*0.05),
        (cx + tamaño*0.10, y + tamaño*0.20),
        (cx + tamaño*0.35, y + tamaño*0.10),
        (cx + tamaño*0.25, y + tamaño*0.35),
    ], fill="black")

    # cabeza (círculo)
    draw.ellipse([
        cx - tamaño*0.15, y + tamaño*0.33,
        cx + tamaño*0.15, y + tamaño*0.63
    ], fill="black")

    # base
    draw.rectangle([
        x + tamaño*0.20, y + tamaño*0.65,
        x + tamaño*0.80, y + tamaño*0.80
    ], fill="black")


# -------------------- DIBUJAR IMAGEN ÚNICA --------------------

def dibujar_todas(soluciones, filename="todas_las_soluciones.png"):
    n = len(soluciones[0])
    sol_count = len(soluciones)
    tamaño = 70                 # tamaño de cada casilla
    margen = tamaño             # separación entre tableros

    columnas = 3
    filas = (sol_count + columnas - 1) // columnas

    # Tamaño total de la imagen considerando márgenes
    width = columnas * (n * tamaño + margen) + margen
    height = filas * (n * tamaño + margen) + margen

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    for index, sol in enumerate(soluciones):
        fila = index // columnas
        col = index % columnas

        # Offset con márgenes añadidos
        offset_x = col * (n * tamaño + margen) + margen
        offset_y = fila * (n * tamaño + margen) + margen

        for r in range(n):
            for c in range(n):
                color = "#f0d9b5" if (r + c) % 2 == 0 else "#b58863"

                x1 = offset_x + c * tamaño
                y1 = offset_y + r * tamaño
                x2 = x1 + tamaño
                y2 = y1 + tamaño

                draw.rectangle([x1, y1, x2, y2], fill=color)

                # Dibujar reina
                if sol[r] == c:
                    dibujar_reina(draw, x1, y1, tamaño)

    img.save(filename)
    print(f"Imagen guardada como {filename}")



# -------------------- MAIN --------------------

def main():
    n = int(input("Introduce el valor de N: "))

    print("\nCalculando soluciones...")
    soluciones = n_reinas(n)
    unicas = filtrar_unicas(soluciones)

    print(f"\nSoluciones totales: {len(soluciones)}")
    print(f"Soluciones distintas (sin simetrías): {len(unicas)}")

    dibujar_todas(unicas)

if __name__ == "__main__":
    main()
