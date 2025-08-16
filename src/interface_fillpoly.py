import tkinter as tk
from tkinter import colorchooser, messagebox

from fillpoly import Poligono


# Classe da tela que serão desenhados os poligonos
def _rgb_to_hex(r, g, b):
    """Converte uma tupla (R, G, B) para uma string de cor hexadecimal."""
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"


# Classe principal da interface
class TelaDesenho:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600, bg="gray20")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.lista_poligonos = []
        self.vertices_poligono_atual = []
        self.cor_selecionada_rgb = (0, 255, 255)  # Ciano

        self.desenhar_arestas = tk.BooleanVar(value=True)
        self.canvas.bind("<Button-1>", self.adicionar_vertice)
        self.root.bind("<space>", self.finalizar_poligono)
        self.canvas.bind("<Button-3>", self.selecionar_poligono)

        self._criar_painel_botoes()

    def _criar_painel_botoes(self):
        """Cria e organiza o painel de botões na interface."""
        frame_botoes = tk.Frame(self.root)
        frame_botoes.grid(row=0, column=1, sticky="n", padx=10, pady=10)

        tk.Button(
            frame_botoes,
            text="Escolher Cor do Vértice",
            command=self.escolher_cor_vertice,
        ).grid(row=0, column=0, pady=5, sticky="ew")

        self.swatch_cor = tk.Label(
            frame_botoes, text="     ", bg=_rgb_to_hex(*self.cor_selecionada_rgb)
        )
        self.swatch_cor.grid(row=1, column=0, pady=(0, 10), sticky="ew")

        tk.Button(frame_botoes, text="Limpar Tela", command=self.limpar_tela).grid(
            row=2, column=0, pady=5, sticky="ew"
        )
        tk.Button(
            frame_botoes, text="Remover Polígono", command=self.remover_poligono
        ).grid(row=4, column=0, pady=5, sticky="ew")
        tk.Checkbutton(
            frame_botoes,
            text="Pintar Arestas",
            variable=self.desenhar_arestas,
            command=self.atualizar_canvas,
        ).grid(row=5, column=0, pady=5)
        self.label_selecao = tk.Label(
            frame_botoes, text="Nenhum Polígono Selecionado", fg="red"
        )
        self.label_selecao.grid(row=8, column=0, pady=10)

    def escolher_cor_vertice(self):
        nova_cor = colorchooser.askcolor(title="Escolha a cor do vértice")
        if nova_cor[0]:
            self.cor_selecionada_rgb = tuple(map(int, nova_cor[0]))
            self.swatch_cor.config(bg=_rgb_to_hex(*self.cor_selecionada_rgb))

    def adicionar_vertice(self, event):
        r, g, b = self.cor_selecionada_rgb
        self.vertices_poligono_atual.append((event.x, event.y, r, g, b))

        # Desenha feedback visual temporário para o vértice e a aresta
        raio = 4
        cor_hex = _rgb_to_hex(r, g, b)
        self.canvas.create_oval(
            event.x - raio,
            event.y - raio,
            event.x + raio,
            event.y + raio,
            fill=cor_hex,
            outline="white",
            tags="desenho_temporario",
        )
        if len(self.vertices_poligono_atual) > 1:
            p1 = self.vertices_poligono_atual[-2]
            p2 = self.vertices_poligono_atual[-1]
            self.canvas.create_line(
                p1[0], p1[1], p2[0], p2[1], fill="white", tags="desenho_temporario"
            )

    def finalizar_poligono(self, event):
        if len(self.vertices_poligono_atual) > 2:
            novo_poligono = Poligono(
                self.vertices_poligono_atual, self.desenhar_arestas.get()
            )
            novo_poligono.calcular_preenchimento()
            self.lista_poligonos.append(novo_poligono)

        self.vertices_poligono_atual = []
        self.atualizar_canvas()

    def atualizar_canvas(self):
        self.canvas.delete("all")
        for poligono in self.lista_poligonos:
            self.desenhar_poligono(poligono)
        # Redesenha os elementos temporários do polígono atual
        self.canvas.delete("desenho_temporario")
        for i, vertice in enumerate(self.vertices_poligono_atual):
            raio = 4
            cor_hex = _rgb_to_hex(vertice[2], vertice[3], vertice[4])
            self.canvas.create_oval(
                vertice[0] - raio,
                vertice[1] - raio,
                vertice[0] + raio,
                vertice[1] + raio,
                fill=cor_hex,
                outline="white",
                tags="desenho_temporario",
            )
            if i > 0:
                p1 = self.vertices_poligono_atual[i - 1]
                p2 = vertice
                self.canvas.create_line(
                    p1[0], p1[1], p2[0], p2[1], fill="white", tags="desenho_temporario"
                )

    def desenhar_poligono(self, poligono):
        """Pega um objeto Poligono e o desenha no canvas."""
        # 1. Desenha o preenchimento calculado
        for x, y, cor in poligono.pixels_calculados:
            hex_color = _rgb_to_hex(cor.r, cor.g, cor.b)
            self.canvas.create_rectangle(x, y, x + 1, y + 1, fill=hex_color, outline="")

        # 2. Desenha as arestas, se aplicável
        poligono.desenhar_arestas = self.desenhar_arestas.get()
        if poligono.desenhar_arestas and len(poligono.vertices) > 1:
            cor_borda = "yellow" if poligono.selecionado else "#FFFFFF"
            largura_borda = 2 if poligono.selecionado else 1
            for i in range(len(poligono.vertices)):
                p1 = poligono.vertices[i]
                p2 = poligono.vertices[(i + 1) % len(poligono.vertices)]
                self.canvas.create_line(
                    p1[0], p1[1], p2[0], p2[1], fill=cor_borda, width=largura_borda
                )

    def selecionar_poligono(self, event):
        selecionou = False
        for poligono in self.lista_poligonos:
            poligono.selecionado = False

        for poligono in reversed(self.lista_poligonos):
            if poligono.ponto_esta_dentro(event.x, event.y):
                poligono.selecionado = True
                selecionou = True
                break

        self.label_selecao.config(
            text=(
                "Polígono Selecionado" if selecionou else "Nenhum Polígono Selecionado"
            ),
            fg="green" if selecionou else "red",
        )
        self.atualizar_canvas()

    def limpar_tela(self):
        self.lista_poligonos.clear()
        self.vertices_poligono_atual.clear()
        self.atualizar_canvas()

    def remover_poligono(self):
        self.lista_poligonos = [p for p in self.lista_poligonos if not p.selecionado]
        self.label_selecao.config(text="Nenhum polígono selecionado", fg="red")
        self.atualizar_canvas()


# --- BLOCO DE EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Editor de Polígonos com Preenchimento Gouraud")
    app = TelaDesenho(root)
    root.mainloop()
