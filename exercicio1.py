import random
from simanneal import Annealer

# --------------------------------------------------------------------------
# 1. DEFINIÇÃO DO PROBLEMA (Dados do Exercício 1)
# --------------------------------------------------------------------------

# Dados extraídos da tabela na página 29 do PDF [cite: 704]
shows = [
    {"nome": "Taylor Swift", "preco": 1200, "gosto": 9.5},
    {"nome": "Beyoncé", "preco": 1100, "gosto": 9.5},
    {"nome": "Tardezinha c/ Thiaguinho", "preco": 300, "gosto": 7.0},
    {"nome": "Jorge & Mateus", "preco": 250, "gosto": 6.0},
    {"nome": "Anitta", "preco": 350, "gosto": 6.0},
    {"nome": "Luísa Sonza", "preco": 280, "gosto": 6.5},
    {"nome": "Billie Eilish", "preco": 700, "gosto": 7.5},
    {"nome": "Avenged Sevenfold", "preco": 1000, "gosto": 6.5},
    {"nome": "Nando Reis", "preco": 200, "gosto": 7.5},
    {"nome": "Gilberto Gil", "preco": 220, "gosto": 7.5},
    {"nome": "Zeca Pagodinho", "preco": 240, "gosto": 7.0},
    {"nome": "Joelma", "preco": 180, "gosto": 5.5},
    {"nome": "Numanice (Ludmila)", "preco": 200, "gosto": 5.0},
    {"nome": "Adele", "preco": 800, "gosto": 8.0},
    {"nome": "Paramore", "preco": 800, "gosto": 8.5},
    {"nome": "The Weeknd", "preco": 950, "gosto": 8.5},
]

# Orçamento máximo de Maria [cite: 708]
BUDGET_MAX = 3000.0

# --------------------------------------------------------------------------
# 2. CLASSE DA METAHEURÍSTICA (RECOZIMENTO SIMULADO)
# --------------------------------------------------------------------------

class ShowAnnealer(Annealer):
    """
    Implementação do Recozimento Simulado para o problema dos shows.
    O "estado" (self.state) é uma lista de índices dos shows que Maria irá.
    """
    def __init__(self, state):
        super(ShowAnnealer, self).__init__(state) # Inicia o Annealer com o estado

    def move(self):
        """
        Gera uma solução "vizinha" modificando levemente a atual.
        Tenta adicionar, remover ou trocar um show aleatoriamente.
        """
        # Escolhe uma ação: 0=remover, 1=adicionar, 2=trocar
        acao = random.randint(0, 2)
        
        # Ação 0: Tenta remover um show (se a lista não estiver vazia)
        if acao == 0 and len(self.state) > 0:
            idx_remover = random.choice(self.state)
            self.state.remove(idx_remover)
            
        # Ação 1: Tenta adicionar um show
        elif acao == 1:
            # Lista de shows que *não* estão no estado atual
            shows_disponiveis = [i for i in range(len(shows)) if i not in self.state]
            if shows_disponiveis:
                idx_adicionar = random.choice(shows_disponiveis)
                self.state.append(idx_adicionar)
                
        # Ação 2: Tenta trocar um show (remove um, adiciona outro)
        else:
            # Tenta remover
            if len(self.state) > 0:
                idx_remover = random.choice(self.state)
                self.state.remove(idx_remover)
            # Tenta adicionar
            shows_disponiveis = [i for i in range(len(shows)) if i not in self.state]
            if shows_disponiveis:
                idx_adicionar = random.choice(shows_disponiveis)
                self.state.append(idx_adicionar)

    def energy(self):
        """
        Calcula a "energia" (custo) da solução.
        Queremos MAXIMIZAR o "gosto", mas o SA MINIMIZA a energia.
        Portanto, nossa energia será o 'gosto total negativo'.
        """
        total_preco = 0
        total_gosto = 0
        
        for idx in self.state:
            total_preco += shows[idx]["preco"]
            total_gosto += shows[idx]["gosto"]
            
        # Penalidade: Se estourar o orçamento, a solução é inválida
        # Damos uma "energia" (custo) muito alta para que o SA a descarte.
        if total_preco > BUDGET_MAX:
            # Retorna 1.0 (muito alto, já que queremos valores negativos)
            return 1.0 
        
        # Se for válida, retorna o negativo do gosto total
        # (pois o SA minimiza, e queremos maximizar o gosto)
        return -total_gosto

# --------------------------------------------------------------------------
# 3. FUNÇÃO AUXILIAR PARA IMPRIMIR A SOLUÇÃO
# --------------------------------------------------------------------------

def print_solution(solution_state, title=""):
    """Imprime os resultados de forma legível."""
    print(f"\n--- {title} ---")
    
    total_gosto = 0
    total_preco = 0
    shows_selecionados = []
    
    for idx in solution_state:
        show = shows[idx]
        shows_selecionados.append(show["nome"])
        total_gosto += show["gosto"]
        total_preco += show["preco"]
        
    print(f"Shows selecionados ({len(shows_selecionados)}):")
    for nome in sorted(shows_selecionados):
        print(f"  - {nome}")
        
    print(f"\nTotal Gosto: {total_gosto:.2f}")
    print(f"Total Preço: R$ {total_preco:.2f} (Orçamento: R$ {BUDGET_MAX:.2f})")

# --------------------------------------------------------------------------
# 4. EXECUTANDO AS SIMULAÇÕES
# --------------------------------------------------------------------------

if __name__ == "__main__":
    
    # --- Exercício 1 (Principal) ---
    # "Quais shows ela deve ir considerando seu gosto pessoal e que ela quer ir 
    #  no máximo de shows que for possível?" [cite: 710, 712]
    # (Nossa função de energia já balanceia isso ao maximizar o gosto)
    
    # Começa com uma solução vazia
    initial_state = []
    annealer = ShowAnnealer(initial_state)
    
    # Executa o Recozimento Simulado
    # Tmax = Temperatura inicial (alta, aceita piores soluções) [cite: 543]
    # Tmin = Temperatura final (baixa, "congela" na melhor solução)
    # steps = Número de iterações
    best_state, best_energy = annealer.anneal(Tmax=25000, Tmin=2.5, steps=50000)
    
    print_solution(best_state, "Exercício 1: Solução Principal (Max Gosto)")

    # --- Exercício 1.a (Com Restrição) ---
    # "Qual o resultado se Maria não abrisse mão de ir ao menos 
    #  no show da Taylor Swift ou Beyonce?" 
    
    # Criamos uma nova classe que HERDA da original e modifica a energia
    class ShowAnnealerConstrained(ShowAnnealer):
        def energy(self):
            # ID da Taylor Swift é 0, Beyoncé é 1
            taylor_presente = (0 in self.state)
            beyonce_presente = (1 in self.state)
            
            # Se NENHUMA das duas estiver, aplica a penalidade máxima
            if not taylor_presente and not beyonce_presente:
                return 1.0 # Solução inválida
            
            # Se ao menos uma estiver, calcula a energia normalmente
            return super().energy()

    initial_state_a = [] # Começa do zero
    annealer_a = ShowAnnealerConstrained(initial_state_a)
    best_state_a, best_energy_a = annealer_a.anneal(Tmax=25000, Tmin=2.5, steps=50000)
    
    print_solution(best_state_a, "Exercício 1.a: Com Restrição (Taylor ou Beyoncé)")

    # --- Exercício 1.b (Mudando Parâmetros) ---
    # "Mude alguns parametros do modelo escolhido e verifique se há mudanças" 
    # Vamos rodar com MUITO menos 'steps' (passos), simulando uma busca de baixa qualidade.
    
    initial_state_b = []
    annealer_b = ShowAnnealer(initial_state_b) # Usando a classe original
    
    # Rodando com apenas 1000 passos (pode não achar a solução ótima)
    best_state_b, best_energy_b = annealer_b.anneal(Tmax=25000, Tmin=2.5, steps=1000)
    
    print_solution(best_state_b, "Exercício 1.b: Parâmetros Alterados (steps=1000)")