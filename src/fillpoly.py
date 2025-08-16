import math


class Cor:
    """Representa cor RGB com valores de 0 a 255."""

    def __init__(self, r=0, g=0, b=0):
        self.r, self.g, self.b = r, g, b

    def __repr__(self):
        return f"Cor: ({self.r},{self.g},{self.b})"


class Vertice:
    """Representa um vértice 2D com cor associada."""

    def __init__(self, x, y, cor=None):
        self.x, self.y = x, y
        self.cor = cor if cor else Cor()

    def __repr__(self):
        return f"Vértice: ({self.x}, {self.y}, {self.cor})"


class Poligono:
    """Classe para lidar com as informaçoes dos poligonos criados na interface"""

    def __init__(self, lista_de_vertices, desenhar_arestas=True):
        self.vertices = lista_de_vertices
        self.desenhar_arestas = desenhar_arestas
        self.selecionado = False
        self.pixels_calculados = []  # Para armazenar resultado do algoritmo

    # Converter os dados dos vértices e chamar Gourand
    def calcular_preenchimento(self):
        # Garantir que exista pelo menos 1 polígono
        if self.pixels_calculados or len(self.vertices) < 3:
            return

        vertices_obj = []
        for v_data in self.vertices:
            x, y, r, g, b = v_data
            cor_obj = Cor(r=r, g=g, b=b)
            vertices_obj.append(Vertice(x=x, y=y, cor=cor_obj))

        self.pixels_calculados = preenchimento_gourand(vertices_obj)

    # Para verificar se um ponto (x,y) está dentro do polígono
    def ponto_esta_dentro(self, x, y):
        n = len(self.vertices)
        dentro = False

        p1x, p1y, _, _, _ = self.vertices[0]
        for i in range(n + 1):
            p2x, p2y, _, _, _ = self.vertices[i % n]
            if y > min(p1y, p2y) and y <= max(p1y, p2y) and x <= max(p1x, p2x):
                if p1y != p2y:
                    x_intersecao = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                if p1x == p2x or x <= x_intersecao:
                    dentro = not dentro
            p1x, p1y = p2x, p2y
        return dentro


def preenchimento_gourand(vertices_obj):
    """
    Executa algoritmo de preenchimento de Scanline com
    sombreamento gourand.
    """

    pixels_para_desenhar = []

    # Aqui encontra os limites verticais do polígono
    y_min = math.ceil(min(v.y for v in vertices_obj))
    y_max = math.floor(max(v.y for v in vertices_obj))

    # Tabela de arestas (edge table) para armazenar interseçoes.
    tabela_arestas = {y: [] for y in range(y_min, y_max)}

    for i in range(len(vertices_obj)):
        p1 = vertices_obj[i]
        p2 = vertices_obj[
            (i + 1) % len(vertices_obj)
        ]  # Para garantir que as arestas fechem.

        # Para garantir que o p1 seja o vértice com menor Y.
        if p1.y > p2.y:
            p1, p2 = p2, p1

        # Para ignorar arestas horizontais
        if p1.y == p2.y:
            continue

        # Calcula incrementos de x e para cara componente de cor
        delta_y = p2.y - p1.y

        if delta_y == 0:
            continue

        dx_dy = (p2.x - p1.x) / delta_y

        dr_dy = (p2.cor.r - p1.cor.r) / delta_y
        dg_dy = (p2.cor.g - p1.cor.g) / delta_y
        db_dy = (p2.cor.b - p1.cor.b) / delta_y

        # Aqui inicializa os valores para interpolaçao
        x, r, g, b = p1.x, p1.cor.r, p1.cor.g, p1.cor.b

        # Itera sobre as scanlines que a aresta cruza
        for y_scan in range(p1.y, p2.y):
            if y_scan in tabela_arestas:
                tabela_arestas[y_scan].append({"x": x, "cor": Cor(r, g, b)})

            x += dx_dy
            r += dr_dy
            g += dg_dy
            b += db_dy

    # Preencher o poligono linha por linha
    for y_scan in range(y_min, y_max - 1):
        intersecoes = tabela_arestas.get(y_scan, [])

        # Ordena as interseçoes pela coordenada x
        intersecoes.sort(key=lambda i: i["x"])

        # Processa as interseçoes em pares para desenhar os segmentos horizontais
        for i in range(0, len(intersecoes), 2):
            if i + 1 >= len(intersecoes):
                continue

            p_inicio = intersecoes[i]
            p_fim = intersecoes[i + 1]

            x_inicio, x_fim = round(p_inicio["x"]), round(p_fim["x"])
            cor_inicio, cor_fim = p_inicio["cor"], p_fim["cor"]

            # Interpolaçao de cor ao longo do segmento horizontal
            delta_x = x_fim - x_inicio
            if delta_x == 0:
                continue

            dr_dx = (cor_fim.r - cor_inicio.r) / delta_x
            dg_dx = (cor_fim.g - cor_inicio.g) / delta_x
            db_dx = (cor_fim.b - cor_inicio.b) / delta_x

            r, g, b = cor_inicio.r, cor_inicio.g, cor_inicio.b

            for x_pixel in range(x_inicio, x_fim + 1):
                pixels_para_desenhar.append(
                    (x_pixel, y_scan, Cor(round(r), round(g), round(b)))
                )
                r += dr_dx
                g += dg_dx
                b += db_dx

    return pixels_para_desenhar
