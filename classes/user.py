import json
import sys
sys.path.insert(1, '/path/to/application/app/folder')
import db.mongo as mongo


class User():
    def __init__(self, dict):

        """ Instancia um novo objeto User com os seguintes atributos:
        self.id
        self.name
        self.balance
        self.apelido
        self.bank
        """

        for key in dict:
            setattr(self, key, dict[key])

    def work(self, colecao, value):
        self.balance += value
        mongo.atualizar_um_na_colecao(nome_colecao=colecao, usuario={"id": self.id}, novos_dados={"$set": {"balance": self.balance}})

    def saldo(self):
        string_formatada = (
            f':dollar: : {self.balance}\n'
            f':bank: : {self.bank}'
        )
        return string_formatada

    def deposito(self, colecao, value):
        self.balance -= value
        self.bank += value
        mongo.atualizar_um_na_colecao(nome_colecao=colecao, usuario={"id": self.id}, novos_dados={"$set": {"balance": self.balance, "bank": self.bank}})

    def saque(self, colecao, value):
        self.balance += value
        self.bank -= value
        mongo.atualizar_um_na_colecao(nome_colecao=colecao, usuario={"id": self.id}, novos_dados={"$set": {"balance": self.balance, "bank": self.bank}})

    def getsaldo(self):
        return self.balance

    def getpoup(self):
        return self.bank
    
    def getId(self):
        return self.id
