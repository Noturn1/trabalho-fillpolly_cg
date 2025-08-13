import tkinter as tk
from tkinter import colorchooser

# Pegar as posições X e Y que o usuário está clicando com o mouse
# Marcar os pontos que o usário selecionar com o mouse
# Botão para utilizar o algoritmo do FillPoly
# Botão para definir a cor do vertice selecionado

# Classe da tela que serão desenhados os poligonos
class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Trabalho FillPoly - Computação Gráfica")
        self.root.configure(bg="#f0f0f0")

        self.lista_vertices = [] # Lista para armazenar os vérices
        self.vertex_color = "black" # Cor para o vértice inicial ---------------------------------------------> talvez mudar depois

        # Quadro branco onde serão exibidos os vértices e poligonos (Canva cental)
        self.canvas = tk.Canvas(root, width=1000, height=600, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Painel dos Botões laterais
        self.button_position = tk.Frame(root, bg="#cccccc")
        self.button_position.pack(side="right", fill="y")

        # Botões
        self.clearScreen_button()
        self.selectVertex_color()
        self.FillPoly_button()

        # Captura de cliques
        self.canvas.bind("<Button-1>", self.canva_click)

    # Método para armazenar o clique do usuário numa lista de vértices e desenhá-lo no Canvas
    def canva_click(self, event):
        x, y = event.x, event.y
        self.lista_vertices.append((x, y))
        r = 3  # raio do ponto
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=self.vertex_color, outline="black")

    # Botão para limpar a tela
    def clearScreen_button(self):
        clearScreen_b = tk.Button(
            self.button_position, text="🧹 Limpar Tela",
            command=self.clearScreen, font=("Arial", 12, "bold"),
            bg="#ff6666", fg="white", relief="flat", padx=10, pady=5
        )
        clearScreen_b.pack(pady=5)

    # Lógica para o botão de limpar a tela
    def clearScreen(self):
        self.canvas.delete("all")
        self.lista_vertices.clear()

    # Botão para selecionar a cor do vértice 
    def selectVertex_color(self):
        color_b = tk.Button(
            self.button_position, text="🎨 Selecionar Cor do Vértice",
            command=self.select_color, font=("Segoe UI", 12, "bold"),
            bg="#4da6ff", fg="white", relief="flat", padx=10, pady=5
        )
        color_b.pack(pady=5)

    # Lógica para o botão de selecionar a cor do vértice
    def select_color(self):
        color = colorchooser.askcolor(title="Escolha a cor do vértice")[1]
        if color:
            self.vertex_color = color

    # Botão para preencher o poligono com o FillPoly
    def FillPoly_button(self):
        fill_b = tk.Button(
            self.button_position, text="🖌 Preencher Polígono (FillPoly)",
            command=self.FillPoly_algorithm, font=("Segoe UI", 12, "bold"),
            bg="#66cc66", fg="white", relief="flat", padx=10, pady=5
        )
        fill_b.pack(pady=5)

    # Lógica do FillPoly
    def FillPoly_algorithm(self):
        pass
