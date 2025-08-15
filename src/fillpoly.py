import sys


class Cor:
    """Representa cor RGB com valores de 0 a 255."""

    def __init__(self, R=0, G=0, B=0):
        self.R, self.G, self.B = R, G, B

    def __repr__(self):
        return f"Cor: ({self.R},{self.G},{self.B})"


class Vertice:
    """Representa um vértice 2D com cor associada."""

    def __init__(self, x, y, cor=None):
        self.x, self.y = x, y
        self.cor = cor if cor else Cor()

    def __repr__(self):
        return f"Vértice: ({self.X}, {self.Y}, {self.cor})"


def preenchimento_gourand(vertices):
    """
    Executa algoritmo de preenchimento de Scanline com
    sombreamento gourand.
    """

    if not vertices:
        return []

    pixels_para_desenhar = []

    # Aqui encontra os limites verticais do polígono
    y_min = min(v.y for v in vertices)
    y_max = max(v.y for v in vertices)

    # Tabela de arestas (edge table) para armazenar interseçoes.
    tabela_arestas = {y: [] for y in range(y_min, y_max)}

    for i in range(len(vertices)):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % len(vertices)]  # Para garantir que as arestas fechem.

        # Para garantir que o p1 seja o vértice com menor Y.
        if p1.y > p2.y:
            p1, p2 = p2, p1

        # Para ignorar arestas horizontais
        if p1.y == p2.y:
            continue

        # Calcula incrementos de x e para cara componente de cor
        delta_y = p2.y - p1.y
        dx_dy = (p2.x - p1.y) / delta_y

        dr_dy = (p2.r - p1.r) / delta_y
        dg_dy = (p2.g - p1.g) / delta_y
        db_dy = (p2.b - p1.b) / delta_y

        # Aqui inicializa os valores para interpolaçao
        x_atual = p1.x
        r_atual, g_atual, b_atual = p1.cor.r, p1.cor.r, p1.cor.b

        # Itera sobre as scanlines que a aresta cruza
        for y in range(p1.y, p2.y):
            tabela_arestas[y].append(
                {"x": x_atual, "cor": Cor(r_atual, g_atual, b_atual)}
            )

            x_atual += dx_dy
            r_atual += dr_dy
            g_atual += dg_dy
            b_atual += db_dy

    # Preencher o poligono linha por linha
    for y in range(y_min, y_max):
        intersecoes = tabela_arestas[y]

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

            dr_dx = (cor_fim.r - cor_incio.r) / delta_x
            dg_dx = (cor_fim.g - cor_incio.g) / delta_x
            db_dx = (cor_fim.b - cor_incio.b) / delta_x

            r, g, b = cor_inicio.r, cor_inicio.g, cor_inicio.b

            for x in range(x_inicio, x_fim + 1):
                pixels_para_desenhar.append((x, y, Cor(round(r), round(b), round(b))))
                r += dr_dx
                g += dg_dx
                b += db_dx

    return pixels_para_desenhar
