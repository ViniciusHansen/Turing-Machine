# Simulador que reconhece tanto a MT sipser quanto a MT duplamente infinita

class TuringMachine:
    def __init__(self, file_path):
        self.transitions = {}
        self.current_state = 0
        self.fita = []
        self.head_position = 0
        self.load(file_path)
        # Duplamente infinita

    def load(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line == ";S":
                    print("Modelo Sipser infinito à direita")
                    self.tipo = "sipser"
                    continue
                elif line == ";I":
                    print("Modelo Sipser infinito aos dois lados")
                    self.tipo = "duplamente infinita"
                    continue
                parts = line.split()
                current_state = str(parts[0])
                current_symbol = str(parts[1])
                new_symbol = str(parts[2])
                direction = str(parts[3])
                new_state = str(parts[4])
                self.transitions[(current_state, current_symbol)] = (new_symbol, direction, new_state)
            
    
                    

    def __str__(self):
        transitions_str = "\n".join([f"{key[0]} {key[1]} -> {value[0]} {value[1]} {value[2]}" for key, value in self.transitions.items()])
        return f"Turing Machine Transitions:\n{transitions_str}"

    def run(self, input_string):
        self.fita = list(input_string) + ['_'] # adiciona um branco no final para representar os infintos brancos
        self.head_position = self.fita.index('*') if '*' in input_string else 0 # opcional: pega posição cabeçote
        print(self.fita)
        # converte para sipser
        if self.tipo == "sipser":
            # Cria transições de estados para o simbolo x
            # '<current state> <current symbol>   <new symbol> <direction> <new state>'.
            #   Estado Y               x                   x           r    Estado Y
            estados = list(set(state for state, _ in self.transitions.keys()))
            for estado in estados:
                self.transitions[(str(estado), '#')] = ('#', 'r', str(estado))
                
            nova_fita = list('#'+''.join(self.fita))
            self.fita = nova_fita
            self.head_position = 1
            print(f"fita sipser: {self.fita}")


        while True:
            # simula a fita infinita
            if self.head_position == len(self.fita) - 1:
                self.fita.append("_")
            symbol_under_head = self.fita[self.head_position] # lê simbolo no cabeçote
            transition_key = (str(self.current_state), symbol_under_head) # cria tupla do estado atual + simbolo lido
            # print()
            if transition_key not in self.transitions:
                print(f"Transição {transition_key}-> não definida --> Entrada rejeitada")
                print(self.transitions)
                break
            new_symbol, direction, new_state = self.transitions[transition_key] # pega dados da função programa
            self.fita[self.head_position] = new_symbol
            self.current_state = new_state
            if direction == 'r':
                self.head_position += 1
            elif direction == 'l':
                self.head_position -= 1
            elif direction == '*':
                pass
            else:
                print("Movimento inválido na fita --> entrada rejeitada") 

            if new_state == "halt-accept":
                print("Estado de aceitação alcançado --> Entrada Aceita!!!")
                break
            

# O arquivo odd.txt é de uma máquina com fita limitada à esquerda (modelo de Sipser) 
# que aceita a linguagem das sequências binárias de comprimento ímpar.
print(f"Simulando a maquina finita na infinita...")
MT1 = TuringMachine('odd.in')
MT1.run('0101010')


# O arquivo sameamount10.txt é de uma máquina com fita duplamente infinita 
# que aceita a linguagem das sequências binárias que possuem a mesma quantidade de 0s e de 1s.

MT2 = TuringMachine('sameamount10.in')
MT2.run('01010101')