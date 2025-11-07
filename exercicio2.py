import random
import math
from simanneal import Annealer

# --------------------------------------------------------------------------
# 1. DEFINIÇÃO DO PROBLEMA (Dados do Exercício 2 - PDF Pág. 33)
# --------------------------------------------------------------------------

# Lista de estádios [cite: 784]
stadiums = [
    "Mineirão (Belo Horizonte)",    # 0 [cite: 785]
    "Maracanã (Rio de Janeiro)",    # 1 [cite: 786]
    "Morumbi (São Paulo)",          # 2 [cite: 787]
    "Mané Garrincha (Brasília)",    # 3 [cite: 788]
    "Beira-Rio (Porto Alegre)",     # 4 [cite: 789]
    "Arena da Baixada (Curitiba)",  # 5 [cite: 790]
    "Arena Fonte Nova (Salvador)",  # 6 [cite: 791]
    "Castelão (Fortaleza)",         # 7 [cite: 792]
    "Arena Pernambuco (Recife)",    # 8 [cite: 793]
    "Mangueirão (Belém)",           # 9 [cite: 794]
    "Arena Pantanal (Cuiabá)",      # 10 [cite: 795]
    "Serra Dourada (Goiânia)"       # 11 [cite: 796]
]

# Matriz de distâncias (km) [cite: 797]
dist_km = [
    [0, 434, 629, 770, 1686, 1032, 1202, 2351, 2039, 2640, 1714, 822],    # 0 [cite: 799]
    [434, 0, 456, 1165, 1406, 844, 1515, 2730, 2340, 3074, 1971, 1166],   # 1 [cite: 799]
    [629, 456, 0, 1098, 1059, 412, 1830, 2962, 2666, 3098, 1658, 1014],   # 2 [cite: 799]
    [770, 1165, 1098, 0, 2030, 1355, 1324, 2101, 2056, 2004, 1100, 219],  # 3 [cite: 799]
    [1686, 1406, 1059, 2030, 0, 685, 2885, 4014, 3720, 4004, 2105, 1875], # 4 [cite: 799]
    [1032, 844, 412, 1355, 685, 0, 2234, 3332, 3070, 3348, 1632, 1216],  # 5 [cite: 800]
    [1202, 1515, 1830, 1324, 2885, 2234, 0, 1275, 836, 2115, 2400, 1531], # 6 [cite: 800]
    [2351, 2730, 2962, 2101, 4014, 3332, 1275, 0, 762, 1419, 2911, 2312], # 7 [cite: 800]
    [2039, 2340, 2666, 2056, 3720, 3070, 836, 762, 0, 2078, 3056, 2274], # 8 [cite: 800]
    [2640, 3074, 3098, 2004, 4004, 3348, 2115, 1419, 2078, 0, 2240, 2132], # 9 [cite: 801]
    [1714, 1971, 1658, 1100, 2105, 1632, 2400, 2911, 3056, 2240, 0, 932],  # 10 [cite: 802]
    [822, 1166, 1014, 219, 1875, 1216, 1531, 2312, 2274, 2132, 932, 0],   # 11 [cite: 803]
]

# Ponto de partida e retorno [cite: 779, 780]
start_idx = 0 # Mineirão [cite: 804]

# --------------------------------------------------------------------------
# 2. CLASSE DA METAHEURÍSTICA (RECOZIMENTO SIMULADO PARA TSP)
# --------------------------------------------------------------------------

class TSPAnnealer(Annealer):
    """
    Implementação do Recozimento Simulado para o Problema do Caixeiro Viajante.
    O "estado" (self.state) é uma lista da ORDEM de visita dos estádios 
    (sem incluir o Mineirão, que é fixo no início e fim).
    """

    def __init__(self, state):
        # state é a lista de cidades (índices 1 a 11) em ordem aleatória
        super(TSPAnnealer, self).__init__(state)

    def move(self):
        """
        Gera uma solução "vizinha" fazendo uma troca "2-opt".
        Isso inverte uma seção aleatória da rota, o que é um
        movimento clássico e eficiente para o TSP.
        """
        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        
        # Garante que a < b
        if a > b:
            a, b = b, a
        elif a == b:
            # Se forem iguais, não faz nada (ou tenta de novo, mas assim é mais simples)
            return

        # Inverte a sub-lista (o "pedaço" da rota)
        self.state[a:b] = self.state[a:b][::-1]

    def energy(self):
        """
        Calcula a "energia" (custo) da solução.
        No TSP, a energia é simplesmente a distância total da rota.
        Queremos MINIMIZAR a distância.
        """
        distance = 0
        current_city = start_idx
        
        # 1. Distância do Início (Mineirão) até a primeira cidade da rota
        distance += dist_km[current_city][self.state[0]]
        
        # 2. Distância entre as cidades da rota
        for i in range(len(self.state) - 1):
            city1 = self.state[i]
            city2 = self.state[i+1]
            distance += dist_km[city1][city2]
            
        # 3. Distância da última cidade da rota de volta ao Início (Mineirão)
        distance += dist_km[self.state[-1]][current_city]
        
        return distance

# --------------------------------------------------------------------------
# 3. FUNÇÃO AUXILIAR PARA IMPRIMIR A ROTA
# --------------------------------------------------------------------------

def print_solution(route_state, distance, title=""):
    """Imprime a rota e a distância total de forma legível."""
    print(f"\n--- {title} ---")
    
    print("Ordem da Rota:")
    # Imprime o ponto de partida
    print(f"  1. {stadiums[start_idx]} (Início/Fim)")
    
    # Imprime a rota encontrada
    count = 2
    for idx in route_state:
        print(f"  {count}. {stadiums[idx]}")
        count += 1
        
    print(f"\nDistância Total: {distance:,.0f} km")

# --------------------------------------------------------------------------
# 4. EXECUTANDO AS SIMULAÇÕES
# --------------------------------------------------------------------------

if __name__ == "__main__":
    
    # --- Exercício 2.A: Rota Principal ---
    # "Dê a lista na ordem e a distancia total" [cite: 781]
    
    # Cria o estado inicial: uma lista de todas as cidades (exceto a inicial)
    # em ordem aleatória.
    initial_state = list(range(1, len(stadiums))) # Índices 1 a 11
    random.shuffle(initial_state)
    
    annealer = TSPAnnealer(initial_state)
    
    # Executa o Recozimento Simulado
    # Tmax/Tmin/steps podem precisar de ajuste para TSP. 
    # Começamos com valores "altos" para dar uma boa busca.
    best_route, min_distance = annealer.anneal(Tmax=1000000, Tmin=0.1, steps=100000)
    
    print_solution(best_route, min_distance, "Exercício 2.A: Melhor Rota Encontrada")

    # --- Exercício 2.B: Mudando Parâmetros ---
    # "Mude parâmetros no modelo escolhido e verifique se há mudanças" [cite: 782]
    #
    # Vamos rodar com MUITO menos 'steps' (passos).
    # Isso dará ao algoritmo menos tempo para "esfriar", e ele
    # provavelmente ficará "preso" em uma solução pior (um mínimo local).
    
    # Embaralha o estado inicial de novo para o teste B
    random.shuffle(initial_state)
    annealer_b = TSPAnnealer(initial_state)

    # Rodando com apenas 5000 passos (busca de baixa qualidade)
    route_b, dist_b = annealer_b.anneal(Tmax=1000000, Tmin=0.1, steps=5000)
    
    print_solution(route_b, dist_b, "Exercício 2.B: Rota com Parâmetros Alterados (steps=5000)")