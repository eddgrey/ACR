import random
import sys
from io import StringIO
from typing import Tuple


class Buscaminas:
    """ Version simple del juego Buscaminas """

    def __init__(self, tam, num_minas):

        self.tam = tam
        self.casillas_para_ganar = (self.tam * self.tam) - num_minas
        self.estado = 'Jugando'
        self.nombre_col = list(' ABCDEFGHIJKLMNOPQRSTUVWXYZ')[:tam+1]
        self.columnas = dict(zip(self.nombre_col[1:], range(tam)))

        self.tablero = [[{'valor': 0, 'is_mina': False, 'visible': False}
                         for j in range(tam)] for i in range(tam)]

        for mina in range(num_minas):
            self.crear_mina_aleatoria()

        self.asignar_valor_casillas()

    def imprimir_tablero(self):

        stdout_original = sys.stdout

        new_stdout = StringIO()

        sys.stdout = new_stdout

        for col in self.nombre_col:
            print(col, end='   ')
        print('\n')

        filas = range(self.tam)
        i = 0

        for row in self.tablero:
            print(filas[i], end='   ')

            for casilla in row:
                if casilla['visible']:
                    print(casilla['valor'], end='   ')
                else:
                    print('_', end='   ')
            i += 1

            print('\n')

        sys.stdout = stdout_original
        return new_stdout.getvalue()

    def seleccionar_casilla(self, casilla):

        col = self.columnas[casilla[0].upper()]
        row = int(casilla[1])

        try:
            casilla = self.tablero[row][col]

            if casilla['is_mina']:
                self.lose_game()
            else:
                self.casillas_para_ganar -= 1  # Revisar esta linea
                if self.casillas_para_ganar == 0:
                    self.win_game()
                else:
                    casilla['visible'] = True

            return True
        except:
            return False

    def crear_mina_aleatoria(self):

        row = random.randint(0, self.tam - 1)
        col = random.randint(0, self.tam - 1)

        self.tablero[row][col]['is_mina'] = True
        self.tablero[row][col]['valor'] = 'X'

    def asignar_valor_casillas(self):
        for row in range(self.tam):
            for col in range(self.tam):
                if not self.tablero[row][col]['is_mina']:
                    self.buscar_minas_adyacentes(row, col)

    def buscar_minas_adyacentes(self, row, col):
        movimientos = [-1, 1, 0]

        for dx in movimientos:
            for dy in movimientos:
                if (row + dx) > -1 and (row + dx) < self.tam and (col + dy) > -1 and (col + dy) < self.tam:
                    casilla_adyacente = self.tablero[row+dx][col+dy]
                    if casilla_adyacente['is_mina']:
                        self.tablero[row][col]['valor'] += 1

    def lose_game(self):
        self.estado = 'Lose'
        for row in range(self.tam):
            for col in range(self.tam):
                if self.tablero[row][col]['is_mina']:
                    self.tablero[row][col]['visible'] = True
        self.imprimir_tablero()

    def win_game(self):
        self.estado = 'Win'
        self.imprimir_tablero()


if __name__ == '__main__':
    tab = Buscaminas(5, 3)

    while tab.estado == 'Jugando':
        tablero = tab.imprimir_tablero()
        print(tablero)
        # casilla = list(input('Ingrese columna y fila (d4, e5, etc): '))
        # tab.seleccionar_casilla(casilla)
