import random
import sys
from io import StringIO


class Buscaminas:
    """ Version simple del juego Buscaminas """

    def __init__(self, tam, num_minas):

        self.tam = tam
        self.casillas_para_ganar = (self.tam * self.tam) - num_minas
        self.estado = 'Jugando'
        self.nombre_col = list(' ABCDEFGHIJKLMNOPQRSTUVWXYZ')[:tam+1]
        self.columnas = dict(zip(self.nombre_col[1:], range(tam)))
        self.board = [[{'valor': 0, 'is_mina': False, 'visible': False}for j in range(tam)] for i in range(tam)]
        self.board_str = ''
        self.update_board()
        n = 0
        while n < num_minas:
            n += self.crear_mina_aleatoria()

        self.asignar_valor_casillas()

    def update_board(self):

        stdout_original = sys.stdout

        new_stdout = StringIO()
        sys.stdout = new_stdout

        for col in self.nombre_col:
            print(col, end='   ')
        print('\n')

        filas = range(self.tam)
        i = 0

        for row in self.board:
            print(filas[i], end='   ')

            for casilla in row:
                if casilla['visible']:
                    print(casilla['valor'], end='   ')
                else:
                    print('_', end='   ')
            i += 1

            print('\n')

        sys.stdout = stdout_original
        self.board_str = new_stdout.getvalue()

    def seleccionar_casilla(self, casilla):

        col = self.columnas[casilla[0].upper()]
        row = int(casilla[1])

        try:
            casilla = self.board[row][col]

            if casilla['is_mina']:
                self.lose_game()
            else:
                self.casillas_para_ganar -= 1
                if self.casillas_para_ganar == 0:
                    self.win_game()
                else:
                    casilla['visible'] = True

            self.update_board()
        except Exception as e:
            print(e)

    def crear_mina_aleatoria(self):

        row = random.randint(0, self.tam - 1)
        col = random.randint(0, self.tam - 1)

        if self.board[row][col]['is_mina']:
            return 0
        else:
            self.board[row][col]['is_mina'] = True
            self.board[row][col]['valor'] = 'X'
            return 1

    def asignar_valor_casillas(self):
        for row in range(self.tam):
            for col in range(self.tam):
                if not self.board[row][col]['is_mina']:
                    self.buscar_minas_adyacentes(row, col)

    def buscar_minas_adyacentes(self, row, col):
        movimientos = [-1, 1, 0]

        for dx in movimientos:
            for dy in movimientos:
                if (row + dx) > -1 and (row + dx) < self.tam and (col + dy) > -1 and (col + dy) < self.tam:
                    casilla_adyacente = self.board[row+dx][col+dy]
                    if casilla_adyacente['is_mina']:
                        self.board[row][col]['valor'] += 1

    def lose_game(self):
        for row in range(self.tam):
            for col in range(self.tam):
                if self.board[row][col]['is_mina']:
                    self.board[row][col]['visible'] = True
        self.update_board()
        self.estado = 'Lose'

    def win_game(self):
        self.estado = 'Win'
        self.update_board()
