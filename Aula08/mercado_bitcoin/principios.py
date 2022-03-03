import datetime
import math
from typing import List


class Pessoa:
    def __init__(self, nome:str, sobrenome:str, data_nascimento:datetime.date):
        self.nome = nome
        self.sobrenome = sobrenome
        self.data_nascimento = data_nascimento

    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_nascimento).days / 365.2425)
    
    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome} tem {self.idade} anos"

class Curriculo:
    def __init__(self, pessoa: Pessoa, experiencias: List[str]):
        self.experiencias = experiencias
        self.pessoa = pessoa

    @property
    def qtd_exp(self) -> int:
        return len(self.experiencias)

    @property
    def emp_atual(self) -> str:
        return self.experiencias[-1]

    def adiciona_exp(self, experiencia:str) -> None:
        self.experiencias.append(experiencia)

    def __str__(self) -> str:
        return f"{self.pessoa.nome} {self.pessoa.sobrenome} tem {self.pessoa.idade} anos e já" \
               f"trabalhou em {self.qtd_exp} empresas e atualmente trabalha em {self.emp_atual}"
        

andre = Pessoa(nome='Andre', sobrenome='Sionek', data_nascimento = datetime.date(1991,1,9))
print(andre)


curriculo_andre = Curriculo(pessoa=andre, experiencias=['HSBC','Polyteck','Grupo Boticário','Olist', 'Emcasa', 'Gousto'])

print(curriculo_andre)

curriculo_andre.adiciona_exp("How Education")

print(curriculo_andre)



#Classe Herdada
class Vivente:
    def __init__(self, nome: str, data_nascimento: datetime.date) -> None:
        self.nome = nome
        self.data_nascimento = data_nascimento

    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_nascimento).days / 365.2425)

    def emite_ruido(self, ruido:str):
        print(f"{self.nome} fez ruido: {ruido}")

#Classe Herdada 1.0
class PessoaHeranca(Vivente):
    def __str__(self) -> str:
        return f"{self.nome} tem {self.idade} anos"

    def fala(self,frase):
        return self.emite_ruido(frase)


#Classe herdada 2.0
class Cachorro(Vivente):
    def __init__(self, nome:str, data_nascimento: datetime.date, raca:str):
        super().__init__(nome, data_nascimento)
        self.raca = raca

    def __str__(self):
        return f"{self.nome} é da raça {self.raca} e tem {self.idade} anos"

    def late(self):
        return self.emite_ruido("Au! Au!")

andre2 = PessoaHeranca(nome='Andre', data_nascimento=datetime.date(1991, 1, 9))
print(andre2)


cachorro = Cachorro(nome='Belisco', data_nascimento=datetime.date(2019, 4 , 15), raca='Lhasa Apso')

print(cachorro)

cachorro.late()
andre2.fala("Cala a boca Belisco!")
