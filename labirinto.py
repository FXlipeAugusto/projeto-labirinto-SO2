class labirinto:

    def __init__(self):
        self.mapa = [
            "###############################",
            "# P1    #       # K           #",
            "##### # # ##### ##### #########",
            "#     # #     #       #       #",
            "# ##### ##### ####### # ##### #",
            "#       #     #       #   A   #",
            "####### # ### # ##### ##### ###",
            "#       # #   #     #       # #",
            "# ##### # ### ##### ####### # #",
            "#   K   #       #       D     #",
            "##### ####### ##### ###########",
            "#       #     #       #       #",
            "# ##### # ### ####### # ##### #",
            "#       #       #       #    S#",
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

    def obter_conteudo(self, linha, coluna):
        """Retorna o caractere na posição (linha, coluna) do mapa."""
        if 0 <= linha < self.linhas and 0 <= coluna < self.colunas:
            return self.mapa[linha][coluna]
        return None

    def chegouSaida(self, posicao):
        return posicao == self.saida