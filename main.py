import random
import json
from collections import defaultdict, deque

# Configuração diretamente no script
configuracao = {
    "memoria_principal": 1024,
    "num_conjuntos": 8,
    "tamanho_conjunto": 4
}

class MemoriaCache:
    def __init__(self, num_conjuntos, tamanho_conjunto):
        self.num_conjuntos = num_conjuntos
        self.tamanho_conjunto = tamanho_conjunto
        self.cache = [deque(maxlen=tamanho_conjunto) for _ in range(num_conjuntos)]
        self.frequencia = [defaultdict(int) for _ in range(num_conjuntos)]
        self.substituicoes = 0  # Contador de substituições devido ao LFU
    
    def acessar(self, endereco, dado):
        indice_conjunto = endereco % self.num_conjuntos
        conjunto_atual = self.cache[indice_conjunto]
        if endereco in conjunto_atual:
            self.frequencia[indice_conjunto][endereco] += 1
            print(f"Acerto no conjunto {indice_conjunto}, endereço {endereco}")
        else:
            if len(conjunto_atual) >= self.tamanho_conjunto:
                self.substituir(indice_conjunto, endereco)
            conjunto_atual.append(endereco)
            self.frequencia[indice_conjunto][endereco] = 1
            print(f"Falha no conjunto {indice_conjunto}, endereço {endereco}, adicionando à cache")
    
    def substituir(self, indice_conjunto, endereco):
        menor_freq = float('inf')
        endereco_lfu = None
        for addr in self.cache[indice_conjunto]:
            if self.frequencia[indice_conjunto][addr] < menor_freq:
                menor_freq = self.frequencia[indice_conjunto][addr]
                endereco_lfu = addr
        self.cache[indice_conjunto].remove(endereco_lfu)
        del self.frequencia[indice_conjunto][endereco_lfu]
        self.substituicoes += 1
        print(f"Substituindo endereço {endereco_lfu} no conjunto {indice_conjunto} pelo endereço {endereco}")

    def exibir(self):
        for i, conjunto_cache in enumerate(self.cache):
            print(f"Conjunto {i}: {list(conjunto_cache)}")

def main():
    memoria_principal = []
    cache = MemoriaCache(configuracao['num_conjuntos'], configuracao['tamanho_conjunto'])
    memoria_principal = [random.randint(0, 1000) for _ in range(configuracao['memoria_principal'])]

    while True:
        print("\nMenu:")
        print("1. Acessar endereço de memória principal")
        print("2. Ler arquivo de sequência de endereços")
        print("3. Sair")
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            endereco = int(input("Informe o endereço da memória principal: "))
            if 0 <= endereco < len(memoria_principal):
                dado = memoria_principal[endereco]
                cache.acessar(endereco, dado)
                cache.exibir()
            else:
                print("Endereço inválido.")
        
        elif escolha == '2':
            arquivo_sequencia = input("Nome do arquivo de sequência de endereços: ")
            try:
                with open(arquivo_sequencia, 'r') as arquivo:
                    enderecos = [int(linha.strip()) for linha in arquivo]
                for endereco in enderecos:
                    if 0 <= endereco < len(memoria_principal):
                        dado = memoria_principal[endereco]
                        cache.acessar(endereco, dado)
                    else:
                        print(f"Endereço {endereco} inválido, ignorando.")
                cache.exibir()
            except FileNotFoundError:
                print(f"Erro: Arquivo '{arquivo_sequencia}' não encontrado.")
        
        elif escolha == '3':
            print(f"Cache final: ")
            cache.exibir()
            print(f"Substituições devido ao LFU: {cache.substituicoes}")
            print("Saindo do programa.")
            break
        
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
