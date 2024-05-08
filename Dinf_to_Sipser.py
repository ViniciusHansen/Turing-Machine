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
            print(estados)
            # para que a MT02 "se lembre" de qual estado chamou ela,
            # vamos criar uma MT02 para cada estado chamador.
            for estado in estados:
                
                self.transitions[(estado, '[')] = ('[', 'r', f'{estado}_MT2_q0')
                self.transitions[(f'{estado}_MT2_q3', '[')] = ('[', 'r', estado)
                self.transitions[(f'{estado}_MT2_q0', ']')] = ('_', 'r', f'{estado}_MT2_q]')
                self.transitions[(f'{estado}_MT2_q]', '_')] = (']', 'l', f'{estado}_MT2_qa')
                self.transitions[(f'{estado}_MT2_qa', '_')] = ('#', 'l', f'{estado}_MT2_qa')
                self.transitions[(f'{estado}_MT2_q1', '_')] = ('_', 'l', f'{estado}_MT2_q1')
                for simbolo in self.alfabeto_fita:
                    self.transitions[(f'{estado}_MT2_q0', simbolo)] = (simbolo, 'r', f'{estado}_MT2_q0')
                    if simbolo != '_':
                        self.transitions[(f'{estado}_MT2_q1', simbolo)] = ('#', 'r', f'{estado}_MT2_q1{simbolo}')
                        self.transitions[(f'{estado}_MT2_q1{simbolo}', '#')] = (simbolo, 'l', f'{estado}_MT2_q1w')
                        self.transitions[(f'{estado}_MT2_qa', simbolo)] = ('#', 'r', f'{estado}_MT2_q1{simbolo}') # qa tem as msm transições de q1
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

print(f"Simulando a maquina finita na infinita...")#
MT1 = TuringMachine('sameamount10.in')
MT1.save("sameamount10.out")


print(f"Simulando a maquina finita na infinita...")#
MT1 = TuringMachine('teste.in')
MT1.save("teste.out")

