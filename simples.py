import tkinter as tk
from tkinter import ttk, messagebox


class NodoSimple:
    def __init__(self, valor):
        self.valor = valor
        self.sig = None


class ListaSimple:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def esta_vacia(self):
        return self.cabeza is None

    def limpiar(self):
        self.cabeza = None
        self.cola = None

    def nodos(self):
        resultado = []
        actual = self.cabeza
        while actual:
            resultado.append(actual)
            actual = actual.sig
        return resultado

    def buscar_con_anterior(self, referencia):
        anterior = None
        actual = self.cabeza
        while actual:
            if actual.valor == referencia:
                return anterior, actual
            anterior = actual
            actual = actual.sig
        return None, None

    def insertar_inicio(self, valor):
        nuevo = NodoSimple(valor)
        nuevo.sig = self.cabeza
        self.cabeza = nuevo
        if self.cola is None:
            self.cola = nuevo
        return True, "Insertado al inicio.", nuevo, nuevo.sig

    def insertar_final(self, valor):
        nuevo = NodoSimple(valor)
        if self.cola is None:
            self.cabeza = nuevo
            self.cola = nuevo
            return True, "Insertado al final (primer nodo).", nuevo, None

        self.cola.sig = nuevo
        self.cola = nuevo
        return True, "Insertado al final.", self.cola, None

    def insertar_antes(self, referencia, valor):
        anterior, actual = self.buscar_con_anterior(referencia)
        if actual is None:
            return False, "No se encontró el nodo de referencia.", None, None

        if anterior is None:
            return self.insertar_inicio(valor)

        nuevo = NodoSimple(valor)
        anterior.sig = nuevo
        nuevo.sig = actual
        return True, "Insertado antes del nodo de referencia.", anterior, actual

    def insertar_despues(self, referencia, valor):
        _, actual = self.buscar_con_anterior(referencia)
        if actual is None:
            return False, "No se encontró el nodo de referencia.", None, None

        nuevo = NodoSimple(valor)
        nuevo.sig = actual.sig
        actual.sig = nuevo
        if self.cola == actual:
            self.cola = nuevo
        return True, "Insertado después del nodo de referencia.", actual, nuevo

    def eliminar_inicio(self):
        if self.cabeza is None:
            return False, "La lista está vacía.", None, None

        eliminado = self.cabeza
        self.cabeza = self.cabeza.sig
        if self.cabeza is None:
            self.cola = None
        return True, f"Eliminado inicio: {eliminado.valor}", self.cabeza, None

    def eliminar_final(self):
        if self.cabeza is None:
            return False, "La lista está vacía.", None, None

        if self.cabeza == self.cola:
            eliminado = self.cabeza
            self.limpiar()
            return True, f"Eliminado final: {eliminado.valor}", None, None

        anterior = self.cabeza
        while anterior.sig != self.cola:
            anterior = anterior.sig

        eliminado = self.cola
        anterior.sig = None
        self.cola = anterior
        return True, f"Eliminado final: {eliminado.valor}", anterior, None

    def eliminar_nodo(self, referencia):
        anterior, actual = self.buscar_con_anterior(referencia)
        if actual is None:
            return False, "No se encontró el nodo de referencia.", None, None

        if anterior is None:
            return self.eliminar_inicio()

        anterior.sig = actual.sig
        if actual == self.cola:
            self.cola = anterior
        return True, f"Eliminado nodo: {actual.valor}", anterior, actual.sig

    def eliminar_antes(self, referencia):
        if self.cabeza is None or self.cabeza.sig is None:
            return False, "No hay suficientes nodos para eliminar antes.", None, None

        if self.cabeza.valor == referencia:
            return False, "No existe nodo anterior al primero.", None, None

        previo_de_anterior = None
        anterior = self.cabeza
        actual = self.cabeza.sig

        while actual:
            if actual.valor == referencia:
                break
            previo_de_anterior = anterior
            anterior = actual
            actual = actual.sig

        if actual is None:
            return False, "No se encontró el nodo de referencia.", None, None

        if previo_de_anterior is None:
            self.cabeza = actual
        else:
            previo_de_anterior.sig = actual

        if anterior == self.cola:
            self.cola = previo_de_anterior

        return (
            True,
            f"Eliminado antes de {referencia}: {anterior.valor}",
            previo_de_anterior,
            actual,
        )

    def eliminar_despues(self, referencia):
        _, actual = self.buscar_con_anterior(referencia)
        if actual is None:
            return False, "No se encontró el nodo de referencia.", None, None

        if actual.sig is None:
            return False, "No existe nodo después del de referencia.", None, None

        eliminado = actual.sig
        actual.sig = eliminado.sig
        if eliminado == self.cola:
            self.cola = actual
        return (
            True,
            f"Eliminado después de {referencia}: {eliminado.valor}",
            actual,
            actual.sig,
        )


class SimplesVisualizer(tk.Toplevel):
    def __init__(self, parent, on_close):
        super().__init__(parent)
        self.title("Listas Simples")
        self.geometry("1280x680")
        self.minsize(1120, 640)

        self.on_close = on_close
        self.lista = ListaSimple()
        self.punteros = {"P": None, "Q": None, "F": None, "T": None}

        self.protocol("WM_DELETE_WINDOW", self.cerrar)

        self._build_ui()
        self.redibujar("Lista simple inicializada.")

    def _build_ui(self):
        root_frame = ttk.Frame(self, padding=10)
        root_frame.pack(fill="both", expand=True)

        controls = ttk.LabelFrame(root_frame, text="Operaciones")
        controls.pack(fill="x", pady=(0, 8))

        ttk.Label(controls, text="Valor:").grid(row=0, column=0, padx=4, pady=6)
        self.valor_entry = ttk.Entry(controls, width=18)
        self.valor_entry.grid(row=0, column=1, padx=4, pady=6)

        ttk.Label(controls, text="Referencia:").grid(row=0, column=2, padx=4, pady=6)
        self.ref_entry = ttk.Entry(controls, width=18)
        self.ref_entry.grid(row=0, column=3, padx=4, pady=6)

        ttk.Button(controls, text="Crear lista", command=self.crear_lista).grid(
            row=0, column=4, padx=4, pady=6
        )
        ttk.Button(controls, text="Insertar inicio", command=self.insertar_inicio).grid(
            row=0, column=5, padx=4, pady=6
        )
        ttk.Button(controls, text="Insertar final", command=self.insertar_final).grid(
            row=0, column=6, padx=4, pady=6
        )
        ttk.Button(controls, text="Insertar antes", command=self.insertar_antes).grid(
            row=0, column=7, padx=4, pady=6
        )
        ttk.Button(
            controls, text="Insertar después", command=self.insertar_despues
        ).grid(row=0, column=8, padx=4, pady=6)

        ttk.Button(controls, text="Eliminar inicio", command=self.eliminar_inicio).grid(
            row=1, column=4, padx=4, pady=6
        )
        ttk.Button(controls, text="Eliminar final", command=self.eliminar_final).grid(
            row=1, column=5, padx=4, pady=6
        )
        ttk.Button(controls, text="Eliminar antes", command=self.eliminar_antes).grid(
            row=1, column=6, padx=4, pady=6
        )
        ttk.Button(
            controls, text="Eliminar después", command=self.eliminar_despues
        ).grid(row=1, column=7, padx=4, pady=6)
        ttk.Button(controls, text="Eliminar nodo", command=self.eliminar_nodo).grid(
            row=1, column=8, padx=4, pady=6
        )

        ttk.Button(controls, text="Regresar al menú", command=self.cerrar).grid(
            row=1, column=0, columnspan=2, padx=4, pady=6, sticky="we"
        )

        self.canvas = tk.Canvas(root_frame, bg="white", height=420)
        self.canvas.pack(fill="both", expand=True)

        self.estado_var = tk.StringVar(value="")
        ttk.Label(root_frame, textvariable=self.estado_var).pack(fill="x", pady=(8, 2))

        self.punteros_var = tk.StringVar(value="")
        ttk.Label(
            root_frame, textvariable=self.punteros_var, font=("Consolas", 10)
        ).pack(fill="x")

    def obtener_valor(self):
        valor = self.valor_entry.get().strip()
        if not valor:
            messagebox.showwarning("Valor requerido", "Ingresa un valor.")
            return None
        return valor

    def obtener_referencia(self):
        referencia = self.ref_entry.get().strip()
        if not referencia:
            messagebox.showwarning(
                "Referencia requerida", "Ingresa el valor de referencia."
            )
            return None
        return referencia

    def crear_lista(self):
        contenido = self.valor_entry.get().strip()
        self.lista.limpiar()
        if contenido:
            tokens = [x.strip() for x in contenido.split(",") if x.strip()]
            for token in tokens:
                self.lista.insertar_final(token)
        self.punteros = {
            "P": self.lista.cabeza,
            "Q": self.lista.cabeza.sig if self.lista.cabeza else None,
            "F": self.lista.cabeza,
            "T": self.lista.cola,
        }
        self.redibujar("Lista creada/reiniciada.")

    def ejecutar_con_valor(self, fn):
        valor = self.obtener_valor()
        if valor is None:
            return
        ok, mensaje, p, q = fn(valor)
        self.actualizar_punteros(p, q)
        self.redibujar(mensaje, ok)

    def ejecutar_con_referencia(self, fn):
        referencia = self.obtener_referencia()
        if referencia is None:
            return
        ok, mensaje, p, q = fn(referencia)
        self.actualizar_punteros(p, q)
        self.redibujar(mensaje, ok)

    def ejecutar_valor_y_referencia(self, fn):
        valor = self.obtener_valor()
        referencia = self.obtener_referencia()
        if valor is None or referencia is None:
            return
        ok, mensaje, p, q = fn(referencia, valor)
        self.actualizar_punteros(p, q)
        self.redibujar(mensaje, ok)

    def insertar_inicio(self):
        self.ejecutar_con_valor(self.lista.insertar_inicio)

    def insertar_final(self):
        self.ejecutar_con_valor(self.lista.insertar_final)

    def insertar_antes(self):
        self.ejecutar_valor_y_referencia(self.lista.insertar_antes)

    def insertar_despues(self):
        self.ejecutar_valor_y_referencia(self.lista.insertar_despues)

    def eliminar_inicio(self):
        ok, mensaje, p, q = self.lista.eliminar_inicio()
        self.actualizar_punteros(p, q)
        self.redibujar(mensaje, ok)

    def eliminar_final(self):
        ok, mensaje, p, q = self.lista.eliminar_final()
        self.actualizar_punteros(p, q)
        self.redibujar(mensaje, ok)

    def eliminar_nodo(self):
        self.ejecutar_con_referencia(self.lista.eliminar_nodo)

    def eliminar_antes(self):
        self.ejecutar_con_referencia(self.lista.eliminar_antes)

    def eliminar_despues(self):
        self.ejecutar_con_referencia(self.lista.eliminar_despues)

    def actualizar_punteros(self, p, q):
        self.punteros["P"] = p
        self.punteros["Q"] = q
        self.punteros["F"] = self.lista.cabeza
        self.punteros["T"] = self.lista.cola

    def redibujar(self, mensaje, exito=True):
        self.estado_var.set(("✔ " if exito else "✖ ") + mensaje)

        self.canvas.delete("all")
        nodos = self.lista.nodos()

        if not nodos:
            self.canvas.create_text(
                520, 190, text="Lista vacía", font=("Segoe UI", 16, "bold"), fill="#666"
            )
            self.punteros_var.set("P=None  Q=None  F=None  T=None")
            return

        posiciones = {}
        x, y = 40, 180
        ancho, alto, gap = 95, 56, 70

        for nodo in nodos:
            self.canvas.create_rectangle(
                x, y, x + ancho, y + alto, width=2, outline="#1f2937"
            )
            self.canvas.create_line(
                x + 65, y, x + 65, y + alto, width=2, fill="#1f2937"
            )
            self.canvas.create_text(
                x + 32,
                y + alto / 2,
                text=str(nodo.valor),
                font=("Segoe UI", 11, "bold"),
            )
            self.canvas.create_text(
                x + 80, y + alto / 2, text="•", font=("Segoe UI", 14), fill="#374151"
            )
            posiciones[nodo] = (x, y)
            x += ancho + gap

        for i in range(len(nodos) - 1):
            x1, y1 = posiciones[nodos[i]]
            x2, y2 = posiciones[nodos[i + 1]]
            self.canvas.create_line(
                x1 + ancho,
                y1 + alto / 2,
                x2,
                y2 + alto / 2,
                width=2,
                arrow=tk.LAST,
                fill="#2563eb",
            )

        colores = {"P": "#7c3aed", "Q": "#b91c1c", "F": "#047857", "T": "#d97706"}
        offsets = {"P": 0, "Q": 16, "F": 32, "T": 48}

        for nombre, nodo in self.punteros.items():
            if nodo in posiciones:
                nx, ny = posiciones[nodo]
                ytxt = ny - 22 - offsets[nombre]
                self.canvas.create_text(
                    nx + 48,
                    ytxt,
                    text=nombre,
                    fill=colores[nombre],
                    font=("Segoe UI", 10, "bold"),
                )
                self.canvas.create_line(
                    nx + 48, ytxt + 4, nx + 48, ny, fill=colores[nombre], arrow=tk.LAST
                )

        estado = []
        for nombre in ("P", "Q", "F", "T"):
            nodo = self.punteros.get(nombre)
            estado.append(f"{nombre}={nodo.valor if nodo else 'None'}")
        self.punteros_var.set("  ".join(estado))

    def cerrar(self):
        self.destroy()
        self.on_close()
