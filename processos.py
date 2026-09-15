class processo:

    def __init__(self, pid, nome, inicio, tarefas):
        self.id = pid
        self.nome = nome
        self.posicao = inicio
        self.tarefas = tarefas
        self.tarefasConcluidas = 0
        self.estado = "Novo"
        self.ativo = True

    def executarTarefas(self, labirinto):
        linha, coluna = self.posicao
        conteudo = labirinto.obter_conteudo(linha, coluna)

        # Define quais caracteres representam tarefas
        letras_tarefa = ['K', 'A', 'D']

        if conteudo in letras_tarefa:
            if self.tarefasConcluidas < len(self.tarefas):
                self.tarefasConcluidas += 1
                tarefa_atual = self.tarefas[self.tarefasConcluidas - 1]
                print(f"[{self.nome}] Executou a tarefa '{tarefa_atual}' na letra '{conteudo}' ({linha}, {coluna})")
            else:
                print(f"[{self.nome}] Encontrou a letra '{conteudo}', mas todas as tarefas já foram concluídas.")
        else:
            print(f"[{self.nome}] Posição ({linha}, {coluna}) contém '{conteudo}'. Nenhuma tarefa para executar aqui.")

    def todasTarefasConcluidas(self):
        return self.tarefasConcluidas == len(self.tarefas)

    def mudarEstado(self, estado):
        self.estado = estado