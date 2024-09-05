from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class ContaBancaria:
    def __init__(self, numero_conta, cliente):
        self._saldo = 0.0
        self._numero_conta = numero_conta
        self._numero_agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @property #propriedades para acessar os atributos privados
    def saldo(self):
        return self._saldo
    
    @property
    def numero_conta(self):
        return self._numero_conta
    
    @property    
    def numero_agencia(self):
        return self._numero_agencia

    @property    
    def cliente(self):
        return self._cliente

    @property    
    def historico(self):
        return self._historico
    
    @classmethod #retorna uma instância de ContaBancaria
    def nova_conta(cls, numero_conta, cliente):
        return cls(numero_conta,cliente)
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f'\n\033[0;30;42mDepósito Realizado com Sucesso!\033[m')
        else:
            print(f'\n\033[0;30;41mOperação de depósito falhou!\033[m')
            return False
        return True

    def sacar(self, valor):
        saldo = self.saldo
        if valor > saldo:
            print(f'\n\033[0;30;41mValor insuficiente para saque!\033[m')
            return False
        elif valor > 500:
            print(f'\n\033[0;30;41mNão é possível sacar mais de R$ 500!\033[m')
            return False
        else:
            print(f'\n\033[0;30;41mSaque Realizado com Sucesso!\033[m')
            return True

class ContaCorrente(ContaBancaria): 
    def __init__(self, numero_conta, cliente, limite = 500.0, limite_saques = 3):
        super().__init__(numero_conta, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        if valor > self._limite:
            print("Operação de saque falhou. Limite excedido!")
        elif numero_saques >= self._limite_saques:
            print("Operação de saque falhou. Número de saques permitido já excedido.")
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"""
            Agência:\t{self.numero_agencia}
            Conta Corrente:\t{self.numero_conta}
            Titular:\t{self.cliente.nome}        
        """

class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacao.append({
            "Tipo": transacao.__class__.__name__,
            "Valor": transacao.valor,
            "Data":datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
        })

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)