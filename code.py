import random


class KnightsTour:
    def __init__(self):
        self.board = self.board_size = self.player = None
        self.moves = []

    def main(self):
        size = self.get_input('size')
        self.board = Board(*size)
        position = self.get_input('start')
        play = self.get_input('?')
        solution = self.solve(position)
        if play and solution:
            self.board = Board(*size)
            result = self.play_game(position)
            print(result)
        elif not solution:
            print('No solution exists!')
            quit()
        else:
            print("\nHere's the solution!")
            self.board.print()

    # Get input from user, validates input based on game event, and returns proper input
    def get_input(self, event, invalid=False):
        while True:
            if event == 'size':
                choice, error = input("Enter your board dimensions: ").split(), 0
            elif event == 'start':
                choice, error = input("Enter the knight's starting position: ").split(), 0
            elif event == 'next':
                error = 1
                if invalid:
                    choice = input("Invalid move! Try again: Enter your next move: ").split()
                else:
                    choice = input("Enter the next move: ").split()
            else:
                choice, error = input("Do you want to try the puzzle? (y/n): ").lower(), 2
                if choice in ['y', 'n']:
                    return True if choice == 'y' else False
            if len(choice) == 2 and choice[0].isdigit() and choice[1].isdigit():
                x, y = int(choice[0]), int(choice[1])
                if event == 'size' and x > 0 and y > 0:
                    return x, y
                elif event in ['start', 'next'] and 0 < x <= self.board.x and 0 < y <= self.board.y:
                    return x - 1, y - 1
            print(['Invalid dimensions!', 'Invalid positions!', 'Invalid input!'][error])

    # move piece to position is valid and
    def move(self, position, count=None):
        x, y = position
        if self.player == 'computer':
            self.board.field[y][x] = (self.board.cell - len(str(count))) * ' ' + str(count)
        else:
            self.moves.append(position)
            self.board.field[y][x] = (self.board.cell - 1) * ' ' + 'X'

    # creates a list of possible moves based on the position
    def possible_moves(self, position):
        x, y = position
        count, moves = 0, {}
        positions = [2, -1], [-2, 1], [-2, -1], [2, 1], [-1, 2], [1, -2], [-1, -2], [1, 2]
        for i, j in positions:
            if 0 <= x + i <= self.board.x - 1 and 0 <= y + j <= self.board.y - 1:
                if self.board.field[y + j][x + i] == self.board.cell * '_':
                    count += 1
                    if self.player == 'user':
                        self.board.field[y + j][x + i] = (self.board.cell - 1) * ' ' + str(count)
                    moves[(x + i, y + j)] = count
        return moves

    # game play loop
    def play_game(self, position):
        self.player = 'user'
        self.move(position)
        moves = self.possible_moves(position)
        while moves:
            self.board.print()
            position = self.get_input('next')
            while position not in moves:
                position = self.get_input('next', True)
            else:
                for row in self.board.field:
                    for i, j in enumerate(row):
                        if 'X' in j:
                            row[i] = (self.board.cell - 1) * ' ' + '*'
                        elif '*' not in j:
                            row[i] = self.board.cell * '_'
                self.move(position)
                moves = self.possible_moves(position)
        self.board.print()
        result = sum("*" in cell for row in self.board.field for cell in row) + 1
        if result == self.board.x * self.board.y:
            return 'What a great tour! Congratulations!'
        else:
            return f'No more possible moves!\nYour knight visited {result} squares!'

    # computer solves the puzzle
    def solve(self, position, count=1):
        self.player = 'computer'
        if count == self.board.x * self.board.y:
            self.move(position, count)
            return True
        for option in self.possible_moves(position):
            if self.possible_moves(option):
                self.move(position, count)
                if self.solve(option, count + 1):
                    return True
                self.move(option, self.board.cell * '_')
        return False


# create a board based on the user input
class Board:
    def __init__(self, x, y):
        self.x, self.y = int(x), int(y)
        self.cell = len(str(self.x * self.y))
        self.field = [[self.cell * '_' for _ in range(self.x)] for _ in range(self.y)]

    def print(self):
        size = len(self.field)
        align = self.x * (self.cell + 1) + 3
        for i in range(size + 3):
            if i in [0, size + 1]:
                print(((self.cell - 1) * ' ') + ('-' * align))
            elif i == size + 2:
                print(''.join((self.cell - len(str(i)) + 1) * ' ' + str(i) for i in range(1, self.x + 1)).rjust(
                    align - 1), '\n')
            else:
                row = str(abs(size + 1) - i)
                print((len(str(size)) - len(row)) * ' ' + row + '|', *self.field[-i], '|')


if __name__ == '__main__':
    game = KnightsTour()
    game.main()
