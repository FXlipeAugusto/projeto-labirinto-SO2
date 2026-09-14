import random
import time

from processos import processo
from gerenciador import GerenciadorProcessos
from labirinto import labirinto
from comunicacao import Comunicacao
from interface import rodar_interface


DIRECOES = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def notificar(fila, p):
    fila.put({
        "pid": p.id,
        "nome": p.nome,
        "posicao": p.posicao,
        "estado": p.estado,
        "tarefasConcluidas": p.tarefasConcluidas,
        "totalTarefas": len(p.tarefas),
    })


def executar_processo(p, mapa, fila):

    p.mudarEstado("Executando")
    notificar(fila, p)

    print(f"{p.nome} iniciado")

    while not mapa.chegouSaida(p.posicao) and not p.todasTarefasConcluidas():

        # simula trabalho: uma tarefa concluída a cada passo dentro do labirinto
        p.executarTarefas()

        print(
            f"{p.nome} executando tarefa "
            f"{p.tarefasConcluidas}/{len(p.tarefas)}"
        )

        # tenta andar para uma célula vizinha válida (movimento aleatório simples)
        linha, coluna = p.posicao
        direcoes = DIRECOES[:]
        random.shuffle(direcoes)

        for dl, dc in direcoes:
            nova_posicao = (linha + dl, coluna + dc)
            if mapa.mover(nova_posicao[0], nova_posicao[1]):
                p.moverPara(nova_posicao)
                break

        notificar(fila, p)
        time.sleep(0.3)

    p.mudarEstado("Terminado")
    notificar(fila, p)

    print(f"{p.nome} terminou")


def main():

    mapa = labirinto()

    gerenciador = GerenciadorProcessos()

    comunicacao = Comunicacao()

    processos = [
        processo(1, "P1", (1, 1), ["Tarefa 1", "Tarefa 2", "Tarefa 3"]),
        processo(2, "P2", (1, 1), ["Tarefa 1", "Tarefa 2", "Tarefa 3"]),
        processo(3, "P3", (1, 1), ["Tarefa 1", "Tarefa 2", "Tarefa 3"]),
        processo(4, "P4", (1, 1), ["Tarefa 1", "Tarefa 2", "Tarefa 3"]),
        processo(5, "P5", (1, 1), ["Tarefa 1", "Tarefa 2", "Tarefa 3"])
    ]

    for p in processos:

        gerenciador.criarProcesso(
            p,
            executar_processo,
            (mapa, comunicacao.fila)
        )

    print("Iniciando processos...\n")

    for p in processos:

        gerenciador.iniciarProcesso(p.id)

    print("\nTodos os processos foram iniciados.\n")

    # a interface roda no processo principal, lendo as atualizações da fila
    rodar_interface(mapa, comunicacao, [p.id for p in processos])

    for p in processos:

        gerenciador.esperarProcesso(p.id)

    print("\nTodos os processos terminaram.")


if __name__ == "__main__":
    main()
