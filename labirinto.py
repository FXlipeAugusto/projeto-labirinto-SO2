class labirinto:
    def __init__(self):
        self.mapa = [
            "###############################",
            "# P1        #   # K           #",
            "##### # # ##### ##### #########",
            "#     # #     #       #       #",
            "# ##### ##### ####### # ##### #",
            "#       #     #       #   A   #",
            "####### # ### # ##### ##### ###",
            "#       # #         #       # #",
            "# ##### # ### ##### ####### # #",
            "#   K   #     K #       D     #",
            "##### ####### ##### ###########",
            "#       #     #       #       #",
            "# ##### # ### ####### # ##### #",
            "#       #       #            S#",
            "###############################"
        ]
        self.linhas = len(self.mapa)
        self.colunas = len(self.mapa[0])
        self.saida = (13, 29)

    def mover(self, linha, coluna):
        if linha < 0 or linha >= self.linhas:
            return False
        if coluna < 0 or coluna >= self.colunas:
            return False
        return self.mapa[linha][coluna] != "#"

    def chegouSaida(self, posicao, processos_ativos):
        # Retorna True se a posição atual for a saída E todos os processos estiverem concluídos (ativo == False)
        todos_concluidos = all(not p.ativo for p in processos_ativos)
        return posicao == self.saida and todos_concluidos