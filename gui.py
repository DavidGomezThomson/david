import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from physics import n_reinas, filtrar_unicas, dibujar_tablero


class NReinasGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Problema de las N-Reinas")
        self.root.configure(bg="white")

        # Marco marrón alrededor
        border = tk.Frame(root, bg="#b38764", width=1100, height=750)
        border.pack(fill="both", expand=True, padx=10, pady=10)

        # Contenedor principal
        container = tk.Frame(border, bg="white")
        container.pack(fill="both", expand=True)

        # Título
        title = tk.Label(
            container,
            text="Problema de las N-Reinas",
            font=("Comic Sans MS", 32, "bold"),
            bg="white",
            fg="black"
        )
        title.pack(pady=20)

        # Entrada superior
        frame_top = tk.Frame(container, bg="white")
        frame_top.pack(pady=15)

        tk.Label(
            frame_top,
            text="Introduce N:",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="black"
        ).grid(row=0, column=0, padx=5)

        self.entry_n = tk.Entry(
            frame_top,
            font=("Arial", 16),
            width=10,
            bg="#e8ddbe",
            relief="flat"
        )
        self.entry_n.grid(row=0, column=1, padx=10)

        btn = tk.Button(
            frame_top,
            text="Resolver",
            font=("Arial", 14, "bold"),
            bg="#e8ddbe",
            fg="#1e1a33",
            relief="flat",
            padx=20,
            pady=5,
            command=self.resolver
        )
        btn.grid(row=0, column=2, padx=10)

        # Info
        self.lbl_info = tk.Label(container, text="", font=("Arial", 14), bg="white")
        self.lbl_info.pack(pady=10)

        # Scroll
        self.frame_scroll = tk.Frame(container, bg="white")
        self.frame_scroll.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame_scroll, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.frame_scroll, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.inner_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.soluciones = []
        self.n = 0

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-event.delta / 120), "units")

    def resolver(self):
        try:
            n = int(self.entry_n.get())
            if n <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Introduce un número entero positivo.")
            return

        self.n = n
        todas = n_reinas(n)
        unicas = filtrar_unicas(todas)
        self.soluciones = unicas

        self.lbl_info.config(text=f"Soluciones únicas: {len(unicas)}")

        self.mostrar_todas()

    def mostrar_todas(self):
        # Limpiar el área
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        columnas = 4
        fig_size = 2.8

        for idx, sol in enumerate(self.soluciones):
            fila = idx // columnas
            col = idx % columnas

            cont = tk.Frame(self.inner_frame, bg="white")
            cont.grid(row=fila, column=col, padx=20, pady=20)

            fig = plt.Figure(figsize=(fig_size, fig_size))
            ax = fig.add_subplot(111)
            dibujar_tablero(ax, sol, self.n)

            canvas = FigureCanvasTkAgg(fig, master=cont)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack()

            tk.Label(
                cont,
                text=f"Solución {idx + 1}",
                bg="white",
                fg="black",
                font=("Arial", 12, "bold")
            ).pack(pady=5)
