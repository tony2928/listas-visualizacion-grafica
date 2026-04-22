import tkinter as tk
from tkinter import ttk, messagebox


class NodoCircular:
    def __init__(self, valor):
        self.valor = valor
        self.sig = None


class ListaCircular:
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
        if self.cabeza is None:
            return resultado
        actual = self.cabeza
        while True:
            resultado.append(actual)
            actual = actual.sig
            if actual == self.cabeza:
                break
        return resultado

    def buscar_nodo(self, referencia):
        if self.cabeza is None:
            return None
        actual = self.cabeza
        while True:
            if actual.valor == referencia:
                return actual
            actual = actual.sig
            if actual == self.cabeza:
                break
        return None

    def buscar_anterior(self, nodo):
        if self.cabeza is None or nodo is None:
            return None
        actual = self.cabeza
        while True:
            if actual.sig == nodo:
                return actual
            actual = actual.sig
            if actual == self.cabeza:
                break
        return None

    def insertar_inicio(self, valor):
        nuevo = NodoCircular(valor)
        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
            nuevo.sig = nuevo
            return True, "Insertado al inicio (primer nodo).", None, nuevo

        nuevo.sig = self.cabeza
        self.cabeza = nuevo
        self.cola.sig = self.cabeza
        return True, "Insertado al inicio.", None, nuevo

    def insertar_final(self, valor):
        nuevo = NodoCircular(valor)
        if self.cola is None:
            self.cabeza = nuevo
            self.cola = nuevo
            nuevo.sig = nuevo
            return True, "Insertado al final (primer nodo).", None, nuevo

        nuevo.sig = self.cabeza
        self.cola.sig = nuevo
        self.cola = nuevo
        return True, "Insertado al final.", None, nuevo

    def insertar_antes(self, referencia, valor):
        objetivo = self.buscar_nodo(referencia)
        if objetivo is None:
            return False, "No se encontró nodo de referencia.", None, None

        if objetivo == self.cabeza:
            return self.insertar_inicio(valor)

        anterior = self.buscar_anterior(objetivo)
        nuevo = NodoCircular(valor)
        anterior.sig = nuevo
        nuevo.sig = objetivo
        return True, "Insertado antes del nodo de referencia.", objetivo, nuevo

    def insertar_despues(self, referencia, valor):
        objetivo = self.buscar_nodo(referencia)
        if objetivo is None:
            return False, "No se encontró nodo de referencia.", None, None

        nuevo = NodoCircular(valor)
        nuevo.sig = objetivo.sig
        objetivo.sig = nuevo
        if objetivo == self.cola:
            self.cola = nuevo
        return True, "Insertado después del nodo de referencia.", objetivo, nuevo

    def _eliminar_nodo(self, nodo):
        if self.cabeza is None or nodo is None:
            return False

        if self.cabeza == self.cola and nodo == self.cabeza:
            self.limpiar()
            return True

        anterior = self.buscar_anterior(nodo)
        if anterior is None:
            return False

        anterior.sig = nodo.sig
        if nodo == self.cabeza:
            self.cabeza = nodo.sig
            self.cola.sig = self.cabeza
        if nodo == self.cola:
            self.cola = anterior
            self.cola.sig = self.cabeza
        return True

    def eliminar_inicio(self):
        if self.cabeza is None:
            return False, "La lista está vacía.", None, None

        eliminado = self.cabeza
        self._eliminar_nodo(eliminado)
        return True, f"Eliminado inicio: {eliminado.valor}", None, eliminado

    def eliminar_final(self):
        if self.cola is None:
            return False, "La lista está vacía.", None, None

        eliminado = self.cola
        self._eliminar_nodo(eliminado)
        return True, f"Eliminado final: {eliminado.valor}", self.cola, self.cabeza

    def eliminar_nodo(self, referencia):
        objetivo = self.buscar_nodo(referencia)
        if objetivo is None:
            return False, "No se encontró nodo de referencia.", None, None

        self._eliminar_nodo(objetivo)
        return True, f"Eliminado nodo: {objetivo.valor}", self.cabeza, self.cola

    def eliminar_antes(self, referencia):
        objetivo = self.buscar_nodo(referencia)
        if objetivo is None:
            return False, "No se encontró nodo de referencia.", None, None

        if self.cabeza == self.cola:
            return False, "No hay suficientes nodos para eliminar antes.", None, None

        antes = self.cola if objetivo == self.cabeza else self.buscar_anterior(objetivo)
        previo_de_antes = self.buscar_anterior(antes)

        self._eliminar_nodo(antes)
        return (
            True,
            f"Eliminado antes de {referencia}: {antes.valor}",
            objetivo,
            antes,
        )

    def eliminar_despues(self, referencia):
        objetivo = self.buscar_nodo(referencia)
        if objetivo is None:
            return False, "No se encontró nodo de referencia.", None, None

        if self.cabeza == self.cola:
            return False, "No hay suficientes nodos para eliminar después.", None, None

        despues = objetivo.sig
        self._eliminar_nodo(despues)
        return (
            True,
            f"Eliminado después de {referencia}: {despues.valor}",
            objetivo,
            despues,
        )


class CircularesVisualizer(tk.Toplevel):
    def __init__(self, parent, on_close):
        super().__init__(parent)
        self.title("Listas Circulares")
        self.geometry("1280x680")
        self.minsize(1120, 640)

        self.on_close = on_close
        self.lista = ListaCircular()
        self.punteros = {"P": None, "Q": None, "F": None, "T": None}

        self.protocol("WM_DELETE_WINDOW", self.cerrar)

        self._build_ui()
        self.redibujar("Lista circular inicializada.")

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

        self.canvas = tk.Canvas(root_frame, bg="white", height=420)
        self.canvas.pack(fill="both", expand=True)

        self.estado_var = tk.StringVar(value="")
        ttk.Label(root_frame, textvariable=self.estado_var).pack(fill="x", pady=(8, 2))

        self.punteros_var = tk.StringVar(value="")
        ttk.Label(
            root_frame, textvariable=self.punteros_var, font=("Consolas", 10)
        ).pack(fill="x")

        button_frame = ttk.Frame(root_frame)
        button_frame.pack(fill="x", pady=(8, 0))
        ttk.Button(button_frame, text="Regresar al menú", command=self.cerrar).pack(
            side="left", padx=4, pady=6
        )
        ttk.Button(button_frame, text="Cerrar Programa", command=self.cerrar_todo).pack(
            side="left", padx=4, pady=6
        )

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

    def limpiar_campos(self):
        self.valor_entry.delete(0, tk.END)
        self.ref_entry.delete(0, tk.END)

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
        self.limpiar_campos()

    def ejecutar_con_valor(self, fn):
        valor = self.obtener_valor()
        if valor is None:
            return
        ok, mensaje, p, q = fn(valor)
        self.actualizar_punteros(p, q)
        self.redibujar(mensaje, ok)
        self.limpiar_campos()

    def ejecutar_con_referencia(self, fn):
        referencia = self.obtener_referencia()
        if referencia is None:
            return
        ok, mensaje, p, q = fn(referencia)
        self.actualizar_punteros(p, q)
        self.redibujar(mensaje, ok)
        self.limpiar_campos()

    def ejecutar_valor_y_referencia(self, fn):
        valor = self.obtener_valor()
        referencia = self.obtener_referencia()
        if valor is None or referencia is None:
            return
        ok, mensaje, p, q = fn(referencia, valor)
        self.actualizar_punteros(p, q)
        self.redibujar(mensaje, ok)
        self.limpiar_campos()

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
        self.limpiar_campos()

    def eliminar_final(self):
        ok, mensaje, p, q = self.lista.eliminar_final()
        self.actualizar_punteros(p, q)
        self.redibujar(mensaje, ok)
        self.limpiar_campos()

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
            self.canvas.create_text(
                x + ancho / 2,
                y + alto / 2,
                text=str(nodo.valor),
                font=("Segoe UI", 11, "bold"),
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

        if len(nodos) > 1:
            xh, yh = posiciones[nodos[0]]
            xt, yt = posiciones[nodos[-1]]
            self.canvas.create_line(
                xt + ancho,
                yt + alto / 2,
                xt + ancho + 30,
                yt + alto / 2,
                xt + ancho + 30,
                yt + alto + 45,
                xh - 30,
                yh + alto + 45,
                xh - 30,
                yh + alto / 2,
                xh,
                yh + alto / 2,
                width=2,
                arrow=tk.LAST,
                fill="#0891b2",
            )
        else:
            x1, y1 = posiciones[nodos[0]]
            self.canvas.create_line(
                x1 + ancho,
                y1 + alto / 2,
                x1 + ancho + 30,
                y1 + alto / 2,
                x1 + ancho + 30,
                y1 - 32,
                x1 - 30,
                y1 - 32,
                x1 - 30,
                y1 + alto / 2,
                x1,
                y1 + alto / 2,
                fill="#0891b2",
                width=2,
                arrow=tk.LAST,
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

    def cerrar_todo(self):
        self.master.quit()
