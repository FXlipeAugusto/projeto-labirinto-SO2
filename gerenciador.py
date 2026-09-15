from multiprocessing import Process

class GerenciadorProcessos:
    def __init__(self):
        self.processos = {}

    def criarProcesso(self, processo_obj, funcao, comunicacao, mapa):
        p = Process(
            target=funcao,
            args=(processo_obj, comunicacao, mapa)
        )
        self.processos[processo_obj.id] = p
        return p

    def iniciarProcesso(self, pid):
        if pid in self.processos and not self.processos[pid].is_alive():
            self.processos[pid].start()

    def finalizarProcesso(self, pid):
        if pid in self.processos:
            self.processos[pid].terminate()

    def esperarProcesso(self, pid):
        if pid in self.processos:
            self.processos[pid].join()