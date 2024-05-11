import sys

class TuringMachine:
    def __init__(self, file_path):
        self.transitions = {}
        self.current_state = 0
        self.fita = []
        self.head_position = 0
        self.load(file_path)
        self.alfabeto_fita = []

    def load(self, file_path):
        self.alfabeto_fita = []
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line == ";S":
                    self.tipo = "sipser"
                    raise ValueError("Erro: o arquivo fornecido já é Sipser.")
                elif line == ";I":
                    self.tipo = "duplamente infinita"
                    continue
                parts = line.split()
                # print(parts[0])
                # como o simulador sempre começa no estado 0,
                # adicionei 1000 ao número dos estados da MT de entrada.
                # Assim posso fazer computações antes de iniciar a MT principal.
                if str(parts[0]).isnumeric():
                    current_state = str(int(parts[0]) + 1000)
                else:
                    current_state = str(parts[0])
                current_symbol = str(parts[1])
                new_symbol = str(parts[2])
                direction = str(parts[3])
                
                new_state = str(parts[4]) if not parts[4].isnumeric() else str(int(parts[4]) + 1000)
                self.alfabeto_fita.append(current_symbol)
                self.alfabeto_fita.append(new_symbol)
                self.transitions[(current_state, current_symbol)] = (new_symbol, direction, new_state)
                
            temp = self.alfabeto_fita
            self.alfabeto_fita = list(set(temp))
            print(f"Alfabeto fita: {self.alfabeto_fita}")

            # MT01
            # Marca inicio e fim da fita
            self.transitions[('0', '0')] = ('0', 'r', '0')
            self.transitions[('0', '1')] = ('1', 'r', '0')
            self.transitions[('0', '_')] = (']', 'l', '1')
            self.transitions[('1', '0')] = ('#', 'r', '10')
            self.transitions[('1', '1')] = ('#', 'r', '11')
            self.transitions[('1', '#')] = ('[', 'r', '1000') # vai pro programa principal
            self.transitions[('10', '#')] = ('0', '*', '1w')
            self.transitions[('10', '_')] = ('0', '*', '1w')
            self.transitions[('11', '#')] = ('1', '*', '1w')
            self.transitions[('11', '_')] = ('1', '*', '1w')
            self.transitions[('1w', '0')] = ('0', 'l', '1w')
            self.transitions[('1w', '1')] = ('1', 'l', '1w')
            self.transitions[('1w', '#')] = ('#', 'l', '1')
            
            # MT02
            # Cuida da borda à esquerda
            estados = list(set(state for state, _ in self.transitions.keys()))
            # print(estados)
            # para que a MT02 "se lembre" de qual estado chamou ela,
            # vamos criar uma MT02 para cada estado chamador.
            for estado in estados:
                
                self.transitions[(estado, '[')] = ('[', 'r', f'{estado}_MT2_q0')
                self.transitions[(f'{estado}_MT2_q3', '[')] = ('[', 'r', estado)
                self.transitions[(f'{estado}_MT2_q0', ']')] = ('_', 'r', f'{estado}_MT2_q]')
                self.transitions[(f'{estado}_MT2_q]', '_')] = (']', 'l', f'{estado}_MT2_q1')
                self.transitions[(f'{estado}_MT2_q1', '_')] = ('#', 'l', f'{estado}_MT2_q1')
                for simbolo in self.alfabeto_fita:
                    self.transitions[(f'{estado}_MT2_q0', simbolo)] = (simbolo, 'r', f'{estado}_MT2_q0')
                    if simbolo != '_':
                        self.transitions[(f'{estado}_MT2_q1', simbolo)] = ('#', 'r', f'{estado}_MT2_q1{simbolo}')
                        self.transitions[(f'{estado}_MT2_q1{simbolo}', '#')] = (simbolo, 'l', f'{estado}_MT2_q1w')
                    if simbolo != ']':
                        self.transitions[(f'{estado}_MT2_q2', simbolo)] = (simbolo, 'r', f'{estado}_MT2_q2')
                    if simbolo != '[':
                        self.transitions[(f'{estado}_MT2_q3', simbolo)] = (simbolo, 'l', f'{estado}_MT2_q3')
                self.transitions[(f'{estado}_MT2_q1', '[')] = ('[', 'r', f'{estado}_MT2_q2')
                self.transitions[(f'{estado}_MT2_q1w', '#')] = ('#', 'l', f'{estado}_MT2_q1')
                self.transitions[(f'{estado}_MT2_q2', '_')] = ('_', 'r', f'{estado}_MT2_q2')
                self.transitions[(f'{estado}_MT2_q2', '#')] = ('_', 'r', f'{estado}_MT2_q2')
                self.transitions[(f'{estado}_MT2_q2', ']')] = (']', 'l', f'{estado}_MT2_q3')
            
            # MT03 
            # Cuida da borda à direita
            estados = list(set(state for state, _ in self.transitions.keys()))
            for estado in estados:
                if "MT2" not in str(estado):
                    self.transitions[(estado, ']')] = ('_', 'r', f'MT3_{estado}')
                    self.transitions[(f'MT3_{estado}', '_')] = (']', 'l', estado)
                                
    def save(self, file_path):
        with open(file_path, 'w') as file:
            if self.tipo == "sipser":
                file.write(";I\n")
            else:
                file.write(";S\n")
            for (current_state, current_symbol), (new_symbol, direction, new_state) in self.transitions.items():
                line = f"{current_state} {current_symbol} {new_symbol} {direction} {new_state}\n"
                file.write(line)


# O arquivo sameamount10.txt é de uma máquina com fita duplamente infinita 
# que aceita a linguagem das sequências binárias que possuem a mesma quantidade de 0s e de 1s.
if __name__ == '__main__':
    entrada = str(sys.argv[1]).split('.')[0]
    print(f"Convertendo {entrada} para Sipser...")
    MT1 = TuringMachine(f'{entrada}.in')
    MT1.save(f"{entrada}.out")


