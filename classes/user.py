class User():
    def __init__(self,userid,name,apelido):
        self.id = userid
        self.name = name
        self.balance = 0
        self.apelido = apelido
        self.bank = 0
        
    def work(self,value):
        self.balance += value
            
    def saldo(self):
        string_formatada =(
        f':dollar: : {self.balance}\n'
        f':bank: : {self.bank}'
        )
        return string_formatada 
    
    def deposito(self,value):
        self.balance-=value
        self.bank+=value
    
    def saque(self,value):
        self.balance+=value
        self.bank-=value

    def getsaldo(self):
        return self.balance
    
    def getpoup(self):
        return self.bank