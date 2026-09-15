import queue  # Biblioteca padrão para tratamento de exceções de fila
from multiprocessing import Queue

class Comunicacao:
    def __init__(self):
        self.fila = Queue()

    def enviar(self, mensagem):
        self.fila.put(mensagem)

    def receber(self):
        try:
            # Tenta retirar da fila imediatamente. Se estiver vazia, gera erro controlado
            return self.fila.get_nowait()
        except queue.Empty:
            return None