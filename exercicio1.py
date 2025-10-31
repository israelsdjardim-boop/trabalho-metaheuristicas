import random
from simanneal import Annealer

# --- Dados do Exercício (Baseado nas páginas 29-30 do PDF) ---
#
artistas = [
    "Taylor Swift", "Beyoncé", "Tardezinha c/ Thiaguinho", "Jorge & Mateus",
    "Anitta", "Luísa Sonza", "Billie Eilish", "Avenged Sevenfold",
    "Nando Reis", "Gilberto Gil", "Zeca Pagodinho", "Joelma",
    "Numanice (Ludmila)", "Adele", "Paramore", "The Weeknd"
]

# Preços (R$) - Baseado na tabela da pág. 29
precos = [
    1200, 1100, 300, 250, 350, 280, 800, 1000, # Nota: PDF tem dados inconsistentes. Usando tabela.
    200, 220, 240, 180, 200, 800, 800, 950 # Nota: PDF tem dados inconsistentes. Usando tabela.
]

# Gosto Pessoal (Vi) - Baseado na tabela da pág. 29
gostos = [
    9.5, 9.5, 7.0, 6.0, 6.0, 6.5, 7.5, 6.5, 
    7.5, 7.5, 7.0, 5.5, 5.0, 8.0, 8.5, 8.5
]

# IDs dos artistas para a restrição da alternativa (a)
ID_TAYLOR = 0
ID_BEYONCE = 1
ORCAMENTO_MAXIMO = 3000.0


class ShowProblem(Annealer):
    """
    Resolve o problema da Maria usando Recozimento Simulado.
    O 'estado' é uma tupla de IDs dos shows que ela decidiu ir.
    """
    
    def __init__(self, initial_state, must_have_show_id=None):
        self.must_have_show_id = must_have_show_id
        super(ShowProblem, self).__init__(initial_state)

    def move(self):
        """Gera um novo estado vizinho."""
        # Escolhe aleatoriamente um show para adicionar ou remover
        show_id = random.randint(0, len(artistas) - 1)
        
        # Faz cópia do estado para não modificar o original
        novo_estado = list(self.state)

        if show_id in novo_estado:
            # Se a restrição (a) estiver ativa, não permite remover o show obrigatório
            if show_id == self.must_have_show_id:
                return # Não faz nada
            novo_estado.remove(show_id)
        else:
            novo_estado.append(show_id)
            
        self.state = tuple(sorted(novo_estado)) # Estados devem ser "hashable" (imutáveis)

    def energy(self):
        """Calcula a "energia" do estado (o que queremos minimizar)."""
        total_custo = 0
        total_gosto = 0
        num_shows = len(self.state)

        # 1. Verificar restrição (a)
        if self.must_have_show_id is not None and self.must_have_show_id not in self.state:
            # Penalidade muito alta se o show obrigatório não estiver incluído
            return 1_000_000 

        # 2. Calcular custo e gosto
        for show_id in self.state:
            total_custo += precos[show_id]
            total_gosto += gostos[show_id]

        # 3. Verificar restrição de orçamento
        if total_custo > ORCAMENTO_MAXIMO:
            # Penalidade alta, proporcional ao quanto estourou o orçamento
            # Isso guia o algoritmo de volta para soluções válidas
            return (total_custo - ORCAMENTO_MAXIMO) * 1000

        # 4. Calcular o objetivo
        # Queremos MAXIMIZAR o número de shows e o gosto pessoal.
        # "ela quer ir no máximo de shows... considerando seu gosto"
        # Isso sugere que N° de Shows é prioridade.
        
        objetivo = (num_shows * 100) + total_gosto
        
        # Como o Annealer MINIMIZA, nós minimizamos o NEGATIVO do nosso objetivo.
        return -objetivo 


def print_solution(state, energy):
    """Função auxiliar para imprimir os resultados."""
    print(f"\nEnergia (Objetivo Negativo): {energy:.2f}")
    
    total_custo = sum(precos[i] for i in state)
    total_gosto = sum(gostos[i] for i in state)
    num_shows = len(state)
    
    print(f"Resultado: {num_shows} shows, Gosto total: {total_gosto:.1f}, Custo total: R$ {total_custo:.2f}")
    print("Shows selecionados:")
    for i in state:
        print(f"  - {artistas[i]} (Custo: R${precos[i]}, Gosto: {gostos[i]})")


# --- Solução Principal ---
print("="*40)
print("Solução Principal (Exercício 1)")
print("="*40)
# Estado inicial: nenhum show
initial_state = []
sa = ShowProblem(tuple(initial_state))
best_state, best_energy = sa.auto(minutes=0.1)
print_solution(best_state, best_energy)


# --- Solução Alternativa (a) ---
print("\n" + "="*40)
print("Solução (a): Obrigada a ir na Taylor Swift OU Beyoncé") 
print("="*40)

# Cenário 1: Obrigada a ir na Taylor Swift (ID 0)
print("--- Cenário A1: Com Taylor Swift ---")
initial_state_ts = [ID_TAYLOR]
sa_ts = ShowProblem(tuple(initial_state_ts), must_have_show_id=ID_TAYLOR)
best_state_ts, best_energy_ts = sa_ts.auto(minutes=0.1)
print_solution(best_state_ts, best_energy_ts)

# Cenário 2: Obrigada a ir na Beyoncé (ID 1)
print("\n--- Cenário A2: Com Beyoncé ---")
initial_state_b = [ID_BEYONCE]
sa_b = ShowProblem(tuple(initial_state_b), must_have_show_id=ID_BEYONCE)
best_state_b, best_energy_b = sa_b.auto(minutes=0.1)
print_solution(best_state_b, best_energy_b)

print("\n--- Conclusão (a) ---")
if best_energy_ts < best_energy_b:
    print("A melhor opção (maior objetivo) é forçar a ida ao show da Taylor Swift.")
else:
    print("A melhor opção (maior objetivo) é forçar a ida ao show da Beyoncé.")


# --- Solução Alternativa (b) ---
print("\n" + "="*40)
print("Solução (b): Mudando parâmetros do modelo") 
print("="*40)
print("Vamos rodar a solução principal novamente, mas com mais 'steps' (passos)")

initial_state = []
sa_b = ShowProblem(tuple(initial_state))

sa_b.Tmax = 25000.0  # Temperatura inicial mais alta
sa_b.Tmin = 1.0      # Temperatura final mais baixa
sa_b.steps = 500000  # Muito mais passos de exploração
sa_b.updates = 100

best_state_b2, best_energy_b2 = sa_b.run()
print_solution(best_state_b2, best_energy_b2)

print(f"\nComparação (b):")
print(f"  Energia com auto(): {best_energy:.2f}")
print(f"  Energia com +steps: {best_energy_b2:.2f}")
if best_energy_b2 < best_energy:
    print("Resultado: Mudar os parâmetros encontrou uma solução melhor!")
else:
print("Resultado: Mudar os parâmetros não melhorou a solução (ou achou a mesma).")