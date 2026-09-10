from multiprocessing import Queue
## Queue traz a implementação das filas entre processos

class Comunicacao:

    def __init__(self):
        self.fila = Queue()

    def enviar(self, mensagem):
        self.fila.put(mensagem)

    def receber(self):
        if not self.fila.empty():
            return self.fila.get()

        return None