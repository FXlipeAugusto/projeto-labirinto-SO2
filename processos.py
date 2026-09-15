class processo:
    def __init__(self, pid, nome, inicio, tarefas):
        self.id = pid
        self.nome = nome
        self.posicao = inicio  # tuple (linha, coluna)
        self.tarefas = tarefas
        self.tarefasConcluidas = 0
        self.estado = "Novo"
        self.ativo = True
        self.iniciado = False  # Flag para evitar múltiplos disparos por proximidade

    def executarTarefas(self):
        if self.tarefasConcluidas < len(self.tarefas):
            self.tarefasConcluidas += 1

    def todasTarefasConcluidas(self):
        return self.tarefasConcluidas == len(self.tarefas)

    def mudarEstado(self, estado):
        self.estado = estado