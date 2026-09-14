## Querido professor e colegas de ofício trabalhístico de SO II, atenção ao seguinte detalhe:
## Em python, não usaremos diretamente as operações clássicas de gerencia de processor, como
## fork(), create(), wait() etc...
## isso pq a biblioteca MULTIPROCESSING já traz essas funções indiretamente

from multiprocessing import Process


class GerenciadorProcessos:
    def __init__(self):
        self.processos = {}

    def criarProcesso(self, processo, funcao, args_extra=()):
        ## process é uma instancia DIRETAMENTE gerenciada pelo SO, com espaço de memória,
        ## recursos e interpretador próprios

        p = Process(
            target=funcao, ## target é a função que o processo vai executar. 
            args=(processo, *args_extra) ## argumentos a ser passados para a "função"
        )

        self.processos[processo.id] = p
        return p

    def iniciarProcesso(self, pid):
        processo = self.processos[pid]
        processo.start()

    def finalizarProcesso(self, pid):
        processo = self.processos[pid]
        processo.terminate()

    def esperarProcesso(self, pid):
        processo = self.processos[pid]
        processo.join()