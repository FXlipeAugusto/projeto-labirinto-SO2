from processos import processo
from gerenciador import GerenciadorProcessos
from labirinto import labirinto
from comunicacao import Comunicacao
import time


def executar_processo(processo):

    print(f"{processo.nome} iniciado")

    for i in range(3):

        processo.executarTarefas()

        print(
            f"{processo.nome} executando tarefa "
            f"{processo.tarefasConcluidas}/{len(processo.tarefas)}"
        )

        time.sleep(1)

    processo.mudarEstado("Terminado")

    print(f"{processo.nome} terminou")


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
            executar_processo
        )

    print("Iniciando processos...\n")

    for p in processos:

        gerenciador.iniciarProcesso(p.id)

    print("\nTodos os processos foram iniciados.")

    for p in processos:

        gerenciador.esperarProcesso(p.id)

    print("\nTodos os processos terminaram.")


if __name__ == "__main__":
    main()