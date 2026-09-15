from multiprocessing import Queue

class Comunicacao:
    def __init__(self):
        self.fila = Queue()

    def enviar(self, mensagem):
        self.fila.put(mensagem)

    def receber(self):
        if not self.fila.empty():
            return self.fila.get()
        return None