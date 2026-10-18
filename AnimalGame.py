# Author: David Haiman
# GitHub username: dhaiman1
# Date: 12/08/25
# Write a class named AnimalGame for playing an animal-themed abstract board game, described below.
# One side's pieces are colored tangerine and the other side's pieces are colored amethyst (you don't need to display any colors,
# but having names for the two sides will help us talk about them). You will need to keep track of which player's turn it is.
# The tangerine player moves first.
# The game takes place on a 7x7 grid. Locations on the board will be specified using "algebraic notation",
# with columns labeled a-g and rows labeled 1-7.

class Piece:
    '''Piece class represents each of the pieces in the game. There will be 14 instances that will be initialized
    by the AnimalGame __init__ method. All of the Piece instances will be sub-classes of Piece that will inherit
    all of the methods of the Piece class. It will communicate with the AnimalGame Class in that an instance of AnimalGame
    will instantiate 14 Pieces. The data members of class Piece will be owner(either Tangerine or Amethyst), distance,
    direction, and locomotion. These data members will be determined depending on what sub-class is being instantiated.
    The Piece class is the parent class of Wombat, Okapi, Kinkajou, and Cuttlefish'''

    def __init__(self, owner, distance, direction, locomotion):
        '''The Piece class init method shows what data members will be apart of each Piece instance'''
        self._owner = owner  # T or A
        self._distance = distance
        self._direction = direction
        self._locomotion = locomotion

    def is_valid_move(self, board, x1, y1, x2, y2):
        '''Determines if the move is valid, this is a method that is designed to be called by AnimalGame make_move() method, returns True
         if the move is a valid move and False if the move is not a valid move. Takes three arguments, two of which will
         be the arguments passed to make_move(), the other will be the current board of the AnimalGame instance, which
         will be a data member of AnimalGame. This use the two positions(arguments for make_move), the current board along
         with the data members of the instance of Piece (which will be determined when the sub-classes are instantiated)
         This method interacts with every class of the program'''
        # check if p_moved_to has a friendly piece
        if board[x2][y2] is not None and board[x2][y2].get_owner() == self._owner:
            return False

        x_delta = x2 - x1
        y_delta = y2 - y1

        if abs(x_delta) == abs(y_delta):
            direction = 'diagonal'
            move_distance = abs(x_delta)

        elif x_delta == 0:
            direction = 'orthogonal'
            move_distance = abs(y_delta)

        elif y_delta == 0:
            direction = 'orthogonal'
            move_distance = abs(x_delta)

        else:
            return False

        # check primary movement
        if self._direction == direction:
            if self._locomotion == 'jumping' and self._distance == move_distance:
                return True
            elif self._locomotion == 'sliding' and self._distance >= move_distance:
                # check if move is blocked
                if self.is_blocked(board, x1, y1, x2, y2, x_delta, y_delta):
                    print('blocked')
                    return False

                return True


        # check secondary movement
        elif self._direction != direction:
            if move_distance == 1:
                return True

        return False

    def is_blocked(self, board, x1, y1, x2, y2, x_delta, y_delta):
        '''takes a board and coordinates and returns True if there is a piece between the starting point and
        the end point of the moves'''

        # compute the necessary steps depending on the sign of the x_delta and y_delta
        if x_delta > 0:
            x1 += 1
        elif x_delta < 0:
            x1 -= 1
        if y_delta > 0:
            y1 += 1
        elif y_delta < 0:
            y1 -= 1

        # if we make it to the final position, there is nothing blocking the move
        if x1 == x2 and y1 == y2:
            return False
        # if there is a piece at the next space, it is blocked
        elif board[x1][y1] is not None:
            return True

        return self.is_blocked(board, x1, y1, x2, y2, x_delta, y_delta)



    def get_owner(self):
        '''Returns who the piece belongs to. This method is designed to be called by AnimalGame method make_move()
        to determine if is_valid_move should be called. If make_move is called and it determines that the Piece
        belongs to the player who's turn it is not, make_move can immediately return False and is_valid_move will
        not be called'''
        return self._owner


class Wombat(Piece):
    '''Represents the sub-class Wombat Piece, inherits all methods from class Piece.'''

    def __init__(self, owner):
        super().__init__(owner, 1, "orthogonal", "jumping")


class Okapi(Piece):
    '''Represents the sub-class Okapi Piece, inherits all methods from class Piece.'''

    def __init__(self, owner):
        super().__init__(owner, 4, "orthogonal", "sliding")


class Kinkajou(Piece):
    '''Represents the sub-class Kinkajou Piece, inherits all methods from class Piece'''

    def __init__(self, owner):
        super().__init__(owner, 3, "diagonal", "jumping")


class Cuttlefish(Piece):
    '''Represents the sub-class Okapi Piece, inherits all methods from class Piece'''

    def __init__(self, owner):
        super().__init__(owner, 2, "diagonal", "sliding")

    '''When is_valid_move is called on any sub-class piece it will behave slightly 
    differently due to its data members being unique to it'''


class AnimalGame:
    '''AnimalGame class that defines the rules of the game and determines who wins
    AnimalGame will need to communicate with the sub-classes of class Piece as it will instantiate 14 Pieces
    as part of it's init method. It will also need to communicate with each Piece as part of the make_move method
    to determine who the Piece belongs to'''

    def __init__(self):
        '''AnimalGame init method that will have data members game_state, board, and turn. The game_state will be either
        "UNFINISHED", "TANGERINE_WON", OR "AMETHYST_WON". The data member
        turn will be set to "Tangerine" to start. The board will be a 7x7 2D list (matrix) with every value starting
        with a value of None. After the board is initialized the 14 Pieces will be instantiated and set to the first and last
        rows.'''
        # any data members that are required for the game when it starts
        # game_state = either "UNFINISHED", "TANGERINE_WON", OR "AMETHYST_WON"
        self._board = [[None for i in range(7)] for j in range(7)]
        self._turn = 'T'
        self._game_state = "UNFINISHED"
        # create pieces and assign them to positions on the board
        starting_order = [Okapi, Wombat, Kinkajou, Cuttlefish, Kinkajou, Wombat, Okapi]
        for col, piece in enumerate(starting_order):
            self._board[0][col] = piece('T')
            self._board[6][col] = piece('A')

    def make_move(self, moved_from, moved_to):
        '''Takes two string arguments and converts the strings in order to index the board matrix to move a piece from
            one position to another position. The first argument will be where the piece is being moved from, the second
            argument will be where the piece is moving to.
            If the square being moved from does not contain a piece belonging
            to the player whose turn it is, or if the piece cannot legally move to the indicated target square,
            or if the game has already been won, then it should just return False
            If the square being moved from does contain a piece belonging to the
            player whose turn it is, we will call is_valid_move on that piece and pass in the board, move_from, and move_to.
            If is_valid_move returns True, it should make indicated move(update board), update whose turn it is, and return True.
                '''
        self.display_game()
        if moved_to.lower() == moved_from.lower():
            return False
        if self._game_state != 'UNFINISHED':
            return False

        parse_dict_col = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6}

        if moved_from[0] not in parse_dict_col or moved_to[0] not in parse_dict_col:
            print(f'{moved_from} or {moved_to} is not a space on the board')
            return False

        try:
            row_from, col_from = int(moved_from[1]) - 1, parse_dict_col[moved_from[0].lower()]
            row_to, col_to = int(moved_to[1]) - 1, parse_dict_col[moved_to[0].lower()]
            self._board[row_from][col_from]
            self._board[row_to][col_to]
        except IndexError:
            print(f'{moved_from} or {moved_to} is not a space on the board')
            return False

        # If the square being moved from does not contain a piece belonging to the player whose turn it is
        if self._board[row_from][col_from] is None or self._board[row_from][col_from].get_owner() != self._turn:
            print('not their turn')
            return False

        if self._board[row_from][col_from].is_valid_move(self._board, row_from, col_from, row_to, col_to):
            # update game_state if necessary, if a cuttlefish was taken
            if isinstance(self._board[row_to][col_to], Cuttlefish):
                if self._turn == 'T':
                    self._game_state = 'TANGERINE_WON'
                else:
                    self._game_state = 'AMETHYST_WON'


            # update board, switch values of board[x2][y2] with the value board[x1][y1]
            self._board[row_to][col_to] = self._board[row_from][col_from]
            self._board[row_from][col_from] = None

            if self._turn == 'T':
                self._turn = 'A'
            else:
                self._turn = 'T'

            self.display_game()
            return True

        return False

    def get_game_state(self):
        '''method that returns the current game state, will either return "UNFINISHED", "TANGERINE_WON", OR "AMETHYST_WON"
        This way we can check what the current state of the game is'''
        return self._game_state

    def display_game(self):
        '''displays current board, useful for debugging purposes and to show what moves have been made and where the pieces
        are on the board. Does not return anything'''
        piece_dict = {'Okapi': 'O', 'Wombat': 'W', 'Kinkajou': 'K', 'Cuttlefish': 'C', None: '[    ]'}
        columns = '   |  A  |  B  |  C  |  D  |  E  |  F  |  G |'
        print(columns)
        for index, row in enumerate(self._board):
            print(f'{index + 1}  ', end='')
            for space in row:

                if space is not None:
                    print(f' {piece_dict[type(space).__name__]}({space.get_owner()}) ', end='')
                else:
                    print(piece_dict[space], end='')
            print(f'  {index + 1}')

        print(columns)
        if self._game_state == 'UNFINISHED':
            print(f'It is {self._turn}\'s turn')
        else:
            print(f'Game Over {self._game_state}')


# a1 = AnimalGame()
# # for row in a1._board:
# #     for piece in row:
# #         print(type(piece).__name__, end='')
# #     print()
# # print(type(3))
# print(a1.make_move('d1', 'f3'))
# print(a1.make_move('g7','g4'))
# print(a1.make_move('g1', 'g4'))
# print(a1.make_move('a7', 'b6'))
# print(a1.make_move('b1', 'c2'))
# print(a1.make_move('b6', 'b4'))
# print(a1.make_move('g4', 'd4'))
# print(a1.make_move('b4', 'd4'))
# print(a1.make_move('a1', 'a3'))
# print(a1.make_move('b7', 'b6'))