class Jogador:
    def __init__(self, id, nome, overall):
        self.id = id
        self.nome = nome
        self.overall = overall

    def getId(self) -> str:
        return self.id

    def getNome(self) -> str:
        return self.nome

    def getOver(self) -> str:
        return self.overall