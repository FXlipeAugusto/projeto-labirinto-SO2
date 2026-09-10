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

        #verifica as dimensoões do labirinto
        if linha < 0 or linha >= self.linhas:
            return False
        
        if coluna < 0 or coluna >= self.colunas:
            return False
        
        return self.mapa[linha][coluna] != "#"

    def chegouSaida(self, posicao):
        ##só vai retornar se a posição for igual a coordenada da saída
        return  posicao == self.saida  
    

