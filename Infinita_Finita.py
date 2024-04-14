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
                current_state = str(int(parts[0]) + 1000)
                current_symbol = str(parts[1])
                new_symbol = str(parts[2])
                direction = str(parts[3])
                new_state = str(parts[4]) if parts[4] == "halt-accept" else str(int(parts[4]) + 1000)
                # <current state> <current symbol> <new symbol> <direction> <new state>
                # 0  0 0 r 0
                # 0  1 1 r 0
                # 0  _ _ l 1
                # 1  1 # r 11
                # 1  0 # r 10
                # 11 _ 1 * 1w
                # 10 _ 0 * 1w
                # 1w 0 0 l 1w
                # 1w 1 1 l 1w
                # 1w # # l 2
                # 2  0 # r 20
                # 2  1 # r 21
                # 20 # 0 * 2w
                # 21 # 1 * 2w
                # 2w 0 0 l 2w
                # 2w 1 1 l 2w
                # 2w # # l 2
                # 2  # # r 1000
                # agora vamos adicionar os novos estados
                self.transitions[('0', '0')] = ('0', 'r', '0')
                self.transitions[('0', '1')] = ('1', 'r', '0')
                self.transitions[('0', '_')] = ('_', 'l', '1')
                self.transitions[('1', '1')] = ('#', 'r', '11')
                self.transitions[('1', '0')] = ('#', 'r', '10')
                self.transitions[('11', '_')] = ('1', '*', '1w')
                self.transitions[('10', '_')] = ('0', '*', '1w')
                self.transitions[('1w', '0')] = ('0', 'l', '1w')
                self.transitions[('1w', '1')] = ('1', 'l', '1w')
                self.transitions[('1w', '#')] = ('#', 'l', '2')
                self.transitions[('2', '0')] = ('#', 'r', '20')
                self.transitions[('2', '1')] = ('#', 'r', '21')
                self.transitions[('20', '#')] = ('0', '*', '2w')
                self.transitions[('21', '#')] = ('1', '*', '2w')
                self.transitions[('2w', '0')] = ('0', 'l', '2w')
                self.transitions[('2w', '1')] = ('1', 'l', '2w')
                self.transitions[('2w', '#')] = ('#', 'l', '2')
                self.transitions[('2', '#')] = ('#', 'r', '1000')
                self.transitions[(current_state, current_symbol)] = (new_symbol, direction, new_state)
                
                # criamos o simbolo especial no começo da fita.
                # agora precisamos implementar o seu comportamento
                # toda vez que o simbolo especial '#' for alcançado:
                    # mover a fita pra direita novamente e inserir o simbolo em branco
                    # exemplo: #1010  --->  #_1010


            
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
MT1 = TuringMachine('sameamount10.in')
MT1.save("sameamount10.out")

