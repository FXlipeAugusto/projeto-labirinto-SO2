import pygame
import sys
import time
from processos import processo
from gerenciador import GerenciadorProcessos
from labirinto import labirinto
from comunicacao import Comunicacao

# Função executada concorrentemente por cada subprocesso
def executar_processo(proc, comunicacao):
    comunicacao.enviar(f"[IPC] {proc.nome} iniciado.")
    for i in range(len(proc.tarefas)):
        proc.executarTarefas()
        comunicacao.enviar(f"[IPC] {proc.nome}: tarefa {proc.tarefasConcluidas}/{len(proc.tarefas)}")
        time.sleep(1.2)
    
    proc.mudarEstado("Terminado")
    comunicacao.enviar(f"[IPC] {proc.nome} finalizado.")
    # Sinaliza encerramento de estado ao processo principal da GUI
    comunicacao.enviar(("TERMINADO", proc.id))

def distancia_manhattan(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def main():
    pygame.init()
    pygame.font.init()

    mapa = labirinto()
    gerenciador = GerenciadorProcessos()
    comunicacao = Comunicacao()

    # Configurações de exibição do Pygame
    TAM_CELULA = 32
    LARGURA_GRID = mapa.colunas * TAM_CELULA
    ALTURA_GRID = mapa.linhas * TAM_CELULA
    LARGURA_PAINEL = 320
    
    LARGURA_JANELA = LARGURA_GRID + LARGURA_PAINEL
    ALTURA_JANELA = ALTURA_GRID

    tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
    pygame.display.set_caption("Simulador SO - Concorrência IPC & Pygame")
    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont("Consolas", 13)

    # Carregamento / fallback de texturas
    try:
        img_ossos = pygame.image.load("ossos.png")
        img_ossos = pygame.transform.scale(img_ossos, (TAM_CELULA, TAM_CELULA))
    except Exception:
        # Fallback visual caso 'ossos.png' não esteja presente no diretório
        img_ossos = pygame.Surface((TAM_CELULA, TAM_CELULA))
        img_ossos.fill((180, 50, 50))

    # Inicialização das entidades (Agente e Subprocessos Estáticos)
    pos_agente = [1, 2]  # Coordenada inicial do Agente Principal (P1)
    
    sub_processos = [
        processo(2, "Kernel (K1)", (1, 16), ["Inic. Memória", "Drivers", "Syscalls"]),
        processo(3, "App (A1)", (5, 25), ["Render GUI", "Input Poll", "Buffer Clear"]),
        processo(4, "Driver (D1)", (9, 23), ["Check Hardware", "I/O Sync", "Interrupts"])
    ]

    for p in sub_processos:
        gerenciador.criarProcesso(p, executar_processo, comunicacao)

    logs = ["=== Terminal de Log IPC ==="]
    jogo_rodando = True

    while jogo_rodando:
        relogio.tick(30)  # Restrição rígida de 30 FPS

        # --- 1. Tratamento de Eventos e Input ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_rodando = False
            elif evento.type == pygame.KEYDOWN:
                nova_linha, nova_coluna = pos_agente[0], pos_agente[1]
                
                if evento.key in (pygame.K_w, pygame.K_UP):
                    nova_linha -= 1
                elif evento.key in (pygame.K_s, pygame.K_DOWN):
                    nova_linha += 1
                elif evento.key in (pygame.K_a, pygame.K_LEFT):
                    nova_coluna -= 1
                elif evento.key in (pygame.K_d, pygame.K_RIGHT):
                    nova_coluna += 1

                # Validação de Colisão imediata por tecla pressionada
                if mapa.mover(nova_linha, nova_coluna):
                    pos_agente = [nova_linha, nova_coluna]


        # --- 2. Lógica de Disparo por Proximidade ---
        for p in sub_processos:
            if p.ativo and not p.iniciado:
                if distancia_manhattan(pos_agente, p.posicao) <= 1:
                    p.iniciado = True
                    gerenciador.iniciarProcesso(p.id)
                    logs.append(f"[GERENCIADOR] Distância <= 1. Disparando {p.nome}")

        # --- 3. Processamento de Mensagens IPC da Fila ---
        msg = comunicacao.receber()
        while msg is not None:
            if isinstance(msg, tuple) and msg[0] == "TERMINADO":
                pid_term = msg[1]
                for p in sub_processos:
                    if p.id == pid_term:
                        p.ativo = False
                        p.mudarEstado("Terminado")
            else:
                logs.append(str(msg))
                if len(logs) > 30:  # Limite de mensagens mantidas na tela
                    logs.pop(1)
            msg = comunicacao.receber()

        # --- 4. Checagem de Condição de Vitória ---
        if mapa.chegouSaida(tuple(pos_agente), sub_processos):
            logs.append("[SISTEMA] Saída liberada! Simulação Concluída.")
            print("Sucesso: Agente alcançou a saída com todos os processos finalizados!")

        # --- 5. Renderização Gráfica ---
        tela.fill((20, 20, 20))

        # Desenhar Labirinto
        for r in range(mapa.linhas):
            for c in range(mapa.colunas):
                rect = pygame.Rect(c * TAM_CELULA, r * TAM_CELULA, TAM_CELULA, TAM_CELULA)
                char = mapa.mapa[r][c]
                
                if char == "#":
                    pygame.draw.rect(tela, (50, 50, 65), rect)
                    pygame.draw.rect(tela, (30, 30, 40), rect, 1)
                elif (r, c) == mapa.saida:
                    pygame.draw.rect(tela, (50, 200, 50), rect)  # Destaque Saída (S)
                else:
                    pygame.draw.rect(tela, (220, 220, 220), rect)
                    pygame.draw.rect(tela, (200, 200, 200), rect, 1)

        # Renderizar Subprocessos Estáticos
        for p in sub_processos:
            pr, pc = p.posicao
            rect_proc = pygame.Rect(pc * TAM_CELULA, pr * TAM_CELULA, TAM_CELULA, TAM_CELULA)
            
            if p.estado == "Terminado":
                tela.blit(img_ossos, rect_proc)
            else:
                cor_proc = (220, 150, 30) if p.iniciado else (100, 100, 250)
                pygame.draw.rect(tela, cor_proc, rect_proc)
                txt = fonte.render(p.nome[0], True, (255, 255, 255))
                tela.blit(txt, (pc * TAM_CELULA + 10, pr * TAM_CELULA + 8))

        # Renderizar Agente Principal (P1)
        rect_agente = pygame.Rect(pos_agente[1] * TAM_CELULA, pos_agente[0] * TAM_CELULA, TAM_CELULA, TAM_CELULA)
        pygame.draw.rect(tela, (230, 40, 40), rect_agente)

        # Painel Lateral de Logs
        rect_painel = pygame.Rect(LARGURA_GRID, 0, LARGURA_PAINEL, ALTURA_JANELA)
        pygame.draw.rect(tela, (10, 14, 20), rect_painel)
        pygame.draw.line(tela, (80, 80, 100), (LARGURA_GRID, 0), (LARGURA_GRID, ALTURA_JANELA), 2)

        y_offset = 10
        for log in logs:
            surf_texto = fonte.render(log, True, (0, 230, 120))
            tela.blit(surf_texto, (LARGURA_GRID + 10, y_offset))
            y_offset += 18

        pygame.display.flip()

    # Finalização de processos pendentes ao fechar
    for p in sub_processos:
        gerenciador.finalizarProcesso(p.id)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()