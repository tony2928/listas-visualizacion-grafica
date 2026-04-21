import tkinter as tk
from tkinter import ttk

from simples import SimplesVisualizer
from circulares import CircularesVisualizer
from dobleligadas import DobleLigadasVisualizer
from dobleligadascirculares import DobleLigadasCircularesVisualizer


class MainMenu:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Visualizador de Listas Enlazadas")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        self.active_window = None

        container = ttk.Frame(self.root, padding=24)
        container.pack(fill="both", expand=True)

        ttk.Label(
            container,
            text="Tipos de Listas",
            font=("Segoe UI", 18, "bold"),
        ).pack(pady=(8, 16))

        ttk.Label(
            container,
            text="Selecciona una visualización para ver operaciones y punteros.",
            font=("Segoe UI", 10),
        ).pack(pady=(0, 18))

        buttons = [
            ("Listas Simples", SimplesVisualizer),
            ("Listas Circulares", CircularesVisualizer),
            ("Listas Doblemente Ligadas", DobleLigadasVisualizer),
            ("Listas Doblemente Ligadas Circulares", DobleLigadasCircularesVisualizer),
        ]

        for label, visualizer in buttons:
            ttk.Button(
                container,
                text=label,
                command=lambda v=visualizer: self.open_visualizer(v),
            ).pack(fill="x", pady=6, ipady=7)

        ttk.Label(
            container,
            text="Cada ventana incluye crear, insertar, eliminar y regreso al menú.",
            font=("Segoe UI", 9),
        ).pack(pady=(18, 0))

    def open_visualizer(self, visualizer_cls):
        if self.active_window is not None:
            return

        self.root.withdraw()
        self.active_window = visualizer_cls(self.root, self.on_visualizer_close)

    def on_visualizer_close(self):
        self.active_window = None
        self.root.deiconify()


if __name__ == "__main__":
    root = tk.Tk()
    MainMenu(root)
    root.mainloop()
