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
                
                # vamos substituir as transições que escrevem _ no meio da fita e atrapalham nossa MT
                # nossa solução vai ser substituir os "_" na parte interna da fita por "v"
                    # nas transições que escrevem e as que dependem dessas os '_' seram trocados por 'v'
                    # nas restantes será apenas adicionada a opção de usar o 'v'
                if new_state == 'halt-accept':
                    pass
                elif int(new_state) > 900 : # MT principal
                    if current_symbol == '_' and new_symbol == '_' and direction == 'l' :
                        # caso de varredura para '_' na fita, foi adicionado a opção de varrer 'v'
                        self.transitions[(current_state, 'v')] = ('v', direction, new_state)
                    elif current_symbol == '_' and new_symbol == '_' and direction == 'r' :
                        # esse é o caso que seria testado o fim da fita a esquerda, foi trocado pelo simbolo especial
                        current_symbol = '#'
                        new_symbol = '#'
                    elif (current_symbol == '1' or current_symbol == '0') and new_symbol == '_':
                        # troca escrita de '_' interno por 'v'
                        new_symbol = 'v'
                    elif current_symbol == '_' and (new_symbol == '0' or new_symbol == '1'):
                        # caso dependente do anterior
                        self.transitions[(current_state, 'v')] = (new_symbol, direction, new_state)
                    elif current_symbol == '_' and new_symbol == 'B':
                        # também depende do caso de escrita de 'v'
                        current_symbol = 'v'
                    # faz as substituições que os outros ifs não pegaram
                    elif current_symbol == '_' :
                        current_symbol = 'v'
                    elif new_symbol == '_' :
                        new_symbol = 'v'
                
                # MT1
                # vamos inserir um simbolo especial no começo da fita. Veja figura 1.
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
                
                # estados da figura 2# X é todos os estados do programa original
                # x    # # r 100 
                # 100  0 0 r 100 
                # 100  1 1 r 100
                # 100  v v r 100
                # 100  _ _ l 101
                # 101  1 $ r 111
                # 101  0 $ r 110
                # 111  _ 1 * 101w
                # 110  _ 0 * 101w
                # 101w 0 0 l 101w
                # 101w 1 1 l 101w
                # 101w $ $ l 200
                # 200  0 $ r 210
                # 200  1 $ r 211
                # 200  v $ r 21v
                # 210  $ 0 * 200w
                # 211  $ 1 * 200w
                # 21v  $ v * 200w
                # 200w 0 0 l 200w
                # 200w 1 1 l 200w
                # 200w v v l 200w
                # 200w $ $ l 200
                # 200  # # r 201
                # 201  $ v * x
                
                # fig 2
                # self.transitions[('100', 'x')] = ('0', 'r', '100')
                # self.transitions[('100', '0')] = ('0', 'r', '100')
                # self.transitions[('100', '1')] = ('1', 'r', '100')
                # self.transitions[('100', 'v')] = ('v', 'r', '100')
                # self.transitions[('100', '_')] = ('_', 'l', '101')
                # self.transitions[('101', '1')] = ('v', 'r', '111')
                # self.transitions[('101', '0')] = ('v', 'r', '110')
                # self.transitions[('111', '_')] = ('1', '*', '101w')
                # self.transitions[('110', '_')] = ('0', '*', '101w')
                # self.transitions[('101w', '0')] = ('0', 'l', '101w')
                # self.transitions[('101w', '1')] = ('1', 'l', '101w')
                # self.transitions[('101w', 'v')] = ('v', 'l', '200')
                # self.transitions[('200', '0')] = ('v', 'r', '210')
                # self.transitions[('200', '1')] = ('v', 'r', '211')
                # self.transitions[('200', 'v')] = ('v', 'r', '21v')
                # self.transitions[('210', 'v')] = ('0', '*', '200w')
                # self.transitions[('211', 'v')] = ('1', '*', '200w')
                # self.transitions[('21v', 'v')] = ('v', '*', '200w')
                # self.transitions[('200w', '0')] = ('0', 'l', '200w')
                # self.transitions[('200w', '1')] = ('1', 'l', '200w')
                # self.transitions[('200w', 'v')] = ('v', 'l', '200w')
                # self.transitions[('200w', 'v')] = ('v', 'l', '200')
                # self.transitions[('200', '#')] = ('#', 'r', '201')
                # self.transitions[('1001', '#')] = ('#', 'r', '1001')
                # self.transitions[('1001', '#')] = ('#', 'r', '100')
                # self.transitions[('201', 'v')] = ('v', '*', '1001')
                
                

                
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
MT1 = TuringMachine('sameamount10.in')
MT1.save("sameamount10.out")

