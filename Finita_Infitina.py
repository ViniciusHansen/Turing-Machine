class TuringMachine:
    def __init__(self, file_path):
        self.transitions = {}
        self.current_state = 0
        self.fita = []
        self.head_position = 0
        self.load(file_path)

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
                # vamos criar 2 transições no inicio do programa para inserir um 'x' na frente da fita
                # (nos aproveitando dos fato da fita também ser infinita à esquerda)
                # já que o estado 0 é sempre o inicial no simulador
                # vamos aumentar em 2 o numero de todos os estados
                current_state = str(int(parts[0]) + 2)
                current_symbol = str(parts[1])
                new_symbol = str(parts[2])
                direction = str(parts[3])
                new_state = str(parts[4]) if parts[4] == "halt-accept" else str(int(parts[4]) + 2)
                # agora vamos adicionar os novos estados
                # 0 * * l 1
                # 1 _ x r i
                # * x x r *
                self.transitions[('0', '*')] = ('*', 'l', '1')
                self.transitions[('1', '_')] = ('x', 'r', '2')
                self.transitions[('*', 'x')] = ('x', 'r', '*')
                self.transitions[(current_state, current_symbol)] = (new_symbol, direction, new_state)

            
    def save(self, file_path):
        with open(file_path, 'w') as file:
            if self.tipo == "sipser":
                file.write(";I\n")
            else:
                file.write(";S\n")
            for (current_state, current_symbol), (new_symbol, direction, new_state) in self.transitions.items():
                line = f"{current_state} {current_symbol} {new_symbol} {direction} {new_state}\n"
                file.write(line)


# O arquivo odd.txt é de uma máquina com fita limitada à esquerda (modelo de Sipser) 
# que aceita a linguagem das sequências binárias de comprimento ímpar.

print(f"Simulando a maquina finita na infinita...")
MT1 = TuringMachine('odd.in')
MT1.save("odd.out")

