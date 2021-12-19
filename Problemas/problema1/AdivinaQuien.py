from io import StringIO
from data import personajes
import sys
import random


class AdivinaQuien():
    def __init__(self, character=None):
        self.estado = 'Jugando'
        self.animals = personajes
        self.character = character if character else self.choose_random_character()
        self.descartados = []
        self.update_board()

    def update_board(self):

        stdout_original = sys.stdout

        new_stdout = StringIO()
        sys.stdout = new_stdout

        if len(self.descartados) == 9 and self.character['nombre'] not in self.descartados:
            self.estado = "You Win"

        for index, animal in enumerate(self.animals):
            if animal['nombre'] not in self.descartados:
                print(f"{index+1}. {animal['nombre']}", end='')
            else:
                print(f"X. {animal['nombre']}", end='')

            print()

        sys.stdout = stdout_original
        self.board_str = new_stdout.getvalue()

    def choose_random_character(self):
        index = random.randint(0, 9)
        return self.animals[index]

    def get_clue(self):
        pistas = self.character['pistas']
        num_pistas = len(pistas)

        if num_pistas == 0:
            return 'No hay mas pistas'

        index = random.randint(0, num_pistas - 1)

        return pistas.pop(index)

    def answer_question(self, question):
        caracteristicas = self.character['caracteristicas']

        for caract in caracteristicas:
            if caract.lower() in question.lower():
                return 'Si'

        return 'No'

    def discard_animals(self, animals):

        for index in animals.split(','):
            self.descartados.append(self.animals[int(index)-1]["nombre"])

        self.update_board()
