import pygame


CORES = {
    "parede": (40, 40, 40),
    "caminho": (230, 230, 230),
    "chave": (255, 215, 0),
    "armadilha": (200, 50, 50),
    "porta": (120, 80, 40),
    "saida": (50, 200, 90),
    "fundo": (255, 255, 255),
    "texto": (20, 20, 20),
    "painel": (245, 245, 245),
}

CORES_PROCESSOS = [
    (220, 20, 60),
    (30, 144, 255),
    (50, 205, 50),
    (255, 140, 0),
    (148, 0, 211),
]

TAMANHO_CELULA = 28


def cor_da_celula(caractere):
    if caractere == "#":
        return CORES["parede"]
    if caractere == "K":
        return CORES["chave"]
    if caractere == "A":
        return CORES["armadilha"]
    if caractere == "D":
        return CORES["porta"]
    if caractere == "S":
        return CORES["saida"]
    return CORES["caminho"]


def desenhar_labirinto(tela, mapa):
    for linha_idx, linha in enumerate(mapa.mapa):
        for coluna_idx, caractere in enumerate(linha):
            cor = cor_da_celula(caractere)
            rect = pygame.Rect(
                coluna_idx * TAMANHO_CELULA,
                linha_idx * TAMANHO_CELULA,
                TAMANHO_CELULA,
                TAMANHO_CELULA,
            )
            pygame.draw.rect(tela, cor, rect)
            pygame.draw.rect(tela, (200, 200, 200), rect, 1)


def desenhar_processos(tela, fonte, estados):
    for pid, dados in estados.items():
        linha, coluna = dados["posicao"]
        cor = CORES_PROCESSOS[(pid - 1) % len(CORES_PROCESSOS)]

        centro = (
            coluna * TAMANHO_CELULA + TAMANHO_CELULA // 2,
            linha * TAMANHO_CELULA + TAMANHO_CELULA // 2,
        )

        raio = TAMANHO_CELULA // 2 - 3
        pygame.draw.circle(tela, cor, centro, raio)
        pygame.draw.circle(tela, (0, 0, 0), centro, raio, 1)

        texto = fonte.render(str(pid), True, (255, 255, 255))
        texto_rect = texto.get_rect(center=centro)
        tela.blit(texto, texto_rect)


def desenhar_painel(tela, fonte, estados, largura_labirinto, largura_painel, altura):
    painel_rect = pygame.Rect(largura_labirinto, 0, largura_painel, altura)
    pygame.draw.rect(tela, CORES["painel"], painel_rect)

    x = largura_labirinto + 16
    y = 16

    titulo = fonte.render("Processos", True, CORES["texto"])
    tela.blit(titulo, (x, y))
    y += 26

    for pid in sorted(estados):
        dados = estados[pid]
        cor = CORES_PROCESSOS[(pid - 1) % len(CORES_PROCESSOS)]

        pygame.draw.circle(tela, cor, (x + 6, y + 8), 6)

        linha_texto = (
            f"{dados['nome']}: {dados['estado']}"
        )
        texto = fonte.render(linha_texto, True, CORES["texto"])
        tela.blit(texto, (x + 18, y))
        y += 18

        detalhe = (
            f"tarefas {dados['tarefasConcluidas']}/{dados['totalTarefas']}  "
            f"pos={dados['posicao']}"
        )
        texto_detalhe = fonte.render(detalhe, True, (90, 90, 90))
        tela.blit(texto_detalhe, (x + 18, y))
        y += 26


def rodar_interface(mapa, comunicacao, ids_processos, largura_painel=280):
    """
    Roda o loop gráfico no processo principal.
    Consome mensagens de status colocadas na fila (comunicacao.fila) pelos
    processos filhos e desenha o labirinto + posição de cada processo.
    Retorna quando todos os processos avisaram estado "Terminado".
    """

    pygame.init()

    largura_labirinto = mapa.colunas * TAMANHO_CELULA
    altura = mapa.linhas * TAMANHO_CELULA
    largura_total = largura_labirinto + largura_painel

    tela = pygame.display.set_mode((largura_total, altura))
    pygame.display.set_caption("O Labirinto dos Processos")

    fonte_painel = pygame.font.SysFont("consolas", 14)
    fonte_processo = pygame.font.SysFont("consolas", 13, bold=True)

    relogio = pygame.time.Clock()

    estados = {
        pid: {
            "pid": pid,
            "nome": f"P{pid}",
            "posicao": (1, 1),
            "estado": "Novo",
            "tarefasConcluidas": 0,
            "totalTarefas": 3,
        }
        for pid in ids_processos
    }

    processos_ativos = set(ids_processos)
    rodando = True

    while rodando:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # drena todas as mensagens disponíveis na fila sem travar o loop gráfico
        while True:
            mensagem = comunicacao.receber()
            if mensagem is None:
                break

            pid = mensagem["pid"]
            estados[pid] = mensagem

            if mensagem["estado"] == "Terminado":
                processos_ativos.discard(pid)

        tela.fill(CORES["fundo"])
        desenhar_labirinto(tela, mapa)
        desenhar_processos(tela, fonte_processo, estados)
        desenhar_painel(tela, fonte_painel, estados, largura_labirinto, largura_painel, altura)

        pygame.display.flip()
        relogio.tick(30)

        if not processos_ativos:
            rodando = False

    pygame.time.wait(1500)
    pygame.quit()
