import random
from simanneal import Annealer

# --------------------------------------------------------------------------
# 1. DEFINIÇÃO DO PROBLEMA (Dados do Exercício 3 - PDF Pág. 34-35)
# --------------------------------------------------------------------------

# Dados extraídos da tabela [cite: 807, 821]
animes_data = [
    {"nome": "Fullmetal Alchemist: Brotherhood", "duracao": 25.07, "interesse": 9.6},
    {"nome": "Death Note", "duracao": 14.49, "interesse": 9.2},
    {"nome": "Cowboy Bebop", "duracao": 10.18, "interesse": 8.8},
    {"nome": "Neon Genesis Evangelion + End of Evangelion", "duracao": 11.68, "interesse": 9.0},
    {"nome": "Steins;Gate (+ OVA)", "duracao": 9.80, "interesse": 9.3},
    {"nome": "Code Geass (R1+R2)", "duracao": 19.58, "interesse": 9.1},
    {"nome": "Hunter x Hunter (2011)", "duracao": 57.97, "interesse": 9.4},
    {"nome": "Monster", "duracao": 28.98, "interesse": 9.0},
    {"nome": "Samurai Champloo", "duracao": 10.18, "interesse": 8.7},
    {"nome": "Gurren Lagann", "duracao": 10.57, "interesse": 8.9},
    {"nome": "Parasyte: The Maxim", "duracao": 9.40, "interesse": 8.5},
    {"nome": "Erased (Boku dake ga Inai Machi)", "duracao": 4.70, "interesse": 8.4},
    {"nome": "Your Lie in April", "duracao": 8.62, "interesse": 8.6},
    {"nome": "Toradora!", "duracao": 9.79, "interesse": 8.3},
    {"nome": "Violet Evergarden (+ filme)", "duracao": 7.82, "interesse": 8.8},
    {"nome": "Baccano! (+ 3 OVAs)", "duracao": 6.27, "interesse": 8.2},
    {"nome": "Black Lagoon (+ Roberta's Blood Trail)", "duracao": 11.36, "interesse": 8.1},
    {"nome": "Fate/Zero", "duracao": 9.79, "interesse": 8.7},
    {"nome": "Fate/stay night: Unlimited Blade Works", "duracao": 10.18, "interesse": 8.4},
    {"nome": "Clannad + After Story", "duracao": 17.23, "interesse": 8.8},
    {"nome": "FLCL (original)", "duracao": 2.35, "interesse": 7.9},
    {"nome": "Ping Pong the Animation", "duracao": 4.31, "interesse": 8.5},
    {"nome": "Devilman Crybaby", "duracao": 3.92, "interesse": 8.0},
    {"nome": "Mob Psycho 100 (S1-S3)", "duracao": 14.49, "interesse": 9.0},
    {"nome": "Naruto (sem Shippuden)", "duracao": 86.17, "interesse": 8.0},
    {"nome": "Attack on Titan (série completa)", "duracao": 36.82, "interesse": 9.3},
    {"nome": "Psycho-Pass (S1)", "duracao": 8.62, "interesse": 8.4},
]

# Capacidade total de tempo (30 dias * 10 h/dia) [cite: 822]
CAPACIDADE_HORAS = 300.0

# --------------------------------------------------------------------------
# 2. CLASSE DA METAHEURÍSTICA (RECOZIMENTO SIMULADO)
# --------------------------------------------------------------------------

class AnimeAnnealer(Annealer):
    """
    Implementação do Recozimento Simulado para o problema dos Animes.
    O "estado" (self.state) é uma lista de índices dos animes que Miguel irá assistir.
    """
    def __init__(self, state):
        super(AnimeAnnealer, self).__init__(state) # Inicia o Annealer com o estado

    def move(self):
        """
        Gera uma solução "vizinha" modificando levemente a atual.
        Tenta adicionar, remover ou trocar um anime aleatoriamente.
        """
        # Escolhe uma ação: 0=remover, 1=adicionar, 2=trocar
        acao = random.randint(0, 2)
        
        # Ação 0: Tenta remover um anime (se a lista não estiver vazia)
        if acao == 0 and len(self.state) > 0:
            idx_remover = random.choice(self.state)
            self.state.remove(idx_remover)
            
        # Ação 1: Tenta adicionar um anime
        elif acao == 1:
            # Lista de animes que *não* estão no estado atual
            animes_disponiveis = [i for i in range(len(animes_data)) if i not in self.state]
            if animes_disponiveis:
                idx_adicionar = random.choice(animes_disponiveis)
                self.state.append(idx_adicionar)
                
        # Ação 2: Tenta trocar um anime (remove um, adiciona outro)
        else:
            # Tenta remover
            if len(self.state) > 0:
                idx_remover = random.choice(self.state)
                self.state.remove(idx_remover)
            # Tenta adicionar
            animes_disponiveis = [i for i in range(len(animes_data)) if i not in self.state]
            if animes_disponiveis:
                idx_adicionar = random.choice(animes_disponiveis)
                self.state.append(idx_adicionar)

    def energy(self):
        """
        Calcula a "energia" (custo) da solução.
        Queremos MAXIMIZAR o "interesse", mas o SA MINIMIZA a energia.
        Portanto, nossa energia será o 'interesse total negativo'.
        """
        total_duracao = 0
        total_interesse = 0
        
        for idx in self.state:
            total_duracao += animes_data[idx]["duracao"]
            total_interesse += animes_data[idx]["interesse"]
            
        # Penalidade: Se estourar o tempo, a solução é inválida
        if total_duracao > CAPACIDADE_HORAS:
            # Retorna 1.0 (muito alto, já que queremos valores negativos)
            return 1.0 
        
        # Se for válida, retorna o negativo do interesse total
        # (pois o SA minimiza, e queremos maximizar o interesse)
        return -total_interesse

# --------------------------------------------------------------------------
# 3. FUNÇÃO AUXILIAR PARA IMPRIMIR A SOLUÇÃO
# --------------------------------------------------------------------------

def print_solution(solution_state, title=""):
    """Imprime os resultados de forma legível."""
    print(f"\n--- {title} ---")
    
    total_interesse = 0
    total_duracao = 0
    animes_selecionados = []
    
    for idx in solution_state:
        anime = animes_data[idx]
        animes_selecionados.append(anime["nome"])
        total_interesse += anime["interesse"]
        total_duracao += anime["duracao"]
        
    print(f"Animes selecionados ({len(animes_selecionados)}):")
    for nome in sorted(animes_selecionados):
        print(f"  - {nome}")
        
    print(f"\nTotal Interesse: {total_interesse:.2f}")
    print(f"Total Duração: {total_duracao:.2f} horas (Capacidade: {CAPACIDADE_HORAS:.2f} horas)")

# --------------------------------------------------------------------------
# 4. EXECUTANDO A SIMULAÇÃO
# --------------------------------------------------------------------------

if __name__ == "__main__":
    
    # --- Exercício 3 (Principal) ---
    # "Otimize o máximo de animes que ele pode assistir" [cite: 814]
    # (A metaheurística vai otimizar o interesse total)
    
    # Começa com uma solução vazia
    initial_state = []
    annealer = AnimeAnnealer(initial_state)
    
    # Executa o Recozimento Simulado
    best_state, best_energy = annealer.anneal(Tmax=25000, Tmin=2.5, steps=50000)
    
    print_solution(best_state, "Exercício 3: Otimização de Animes (Max Interesse)")