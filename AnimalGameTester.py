# Author: David Haiman
# GitHub username: dhaiman1
# Date: 12/3/25
# Unit Tests for AnimalGame.py
# Pieces only move valid distances (sliding pieces can move less than their full range, jumping pieces cannot)
# Pieces only move valid directions (diagonal pieces can also move one square orthogonally and orthogonal pieces can also move one square diagonally)
# Sliding pieces are blocked by intervening pieces, jumping pieces are not
# Captures are handled correctly, including that players cannot capture their own pieces
# Turn order is handled correctly
# The get_game_state() method correctly reports the game state
import unittest
from halfway_progress_report import Piece, Wombat, Okapi, Kinkajou, Cuttlefish, AnimalGame



class AnimalGameTester(unittest.TestCase):
    '''Contains unit tests for Piece and Piece sub-classes and AnimalGame classes'''

    def test_distance_moves(self):
        '''Tests pieces for proper movement as it relates to distance. Jumping pieces cannot move less than their distance,
         sliding pieces can.'''
        animal_1 = AnimalGame()
        self.assertEqual(animal_1.make_move('a1', 'a3'), True)  # Okapi(sliding) can move less than 4 spaces
        self.assertEqual(animal_1.make_move('c7', 'e5'), False) # KinKajou(jumping) cannot move less than 3 spaces
        self.assertEqual(animal_1.make_move('c7', 'f4'), True)  # Kinkajou can move 3 spaces (it's distance)
        self.assertEqual(animal_1.make_move('d1', 'g4'), False)  # Cuttlefish cannot move 3 spaces
        self.assertEqual(animal_1.make_move('d1', 'f3'), True)  # Cuttlefish can move 2 spaces

    def test_direction_moves(self):
        '''Tests pieces for proper movement as it relates to direction, Orthogonal pieces can move orthogonally and exactly
         one space diagonally. Diagonal pieces can move diagonally and exactly one space orthogonally'''
        animal_1 = AnimalGame()
        self.assertEqual(animal_1.make_move('a1', 'c3'), False)  # Okapi cannot move diagonally more than once space
        self.assertEqual(animal_1.make_move('a1', 'b2'), True)  # Okapi can move once space diagonally
        self.assertEqual(animal_1.make_move('c7', 'c6'), True)  # Kinkajou can move once space orthogonally
        self.assertEqual(animal_1.make_move('d1', 'd3'), False)  # Cuttlefish cannot move two spaces orthogonally
        self.assertEqual(animal_1.make_move('d1', 'd2'), True)  # Cuttlefish can move one space orthogonally

    def test_blocked_moves(self):
        '''Tests that sliding pieces are properly blocked if there is a piece in it's way. Also tests that jumping pieces
        are not blocked if there is a piece in its way'''
        animal_1 = AnimalGame()
        self.assertEqual(animal_1.make_move('a1', 'a5'), True)  # Tangerine Okapi moves 4 spaces down
        self.assertEqual(animal_1.make_move('a7', 'a4'), False)  # Amethyst Okapi is blocked by Tangerine Okapi
        self.assertEqual(animal_1.make_move('g7', 'g4'), True)
        self.assertEqual(animal_1.make_move('a5', 'e5'), True)  # Tangerine Okapi moves 4 spaces to the right
        self.assertEqual(animal_1.make_move('c7', 'f4'), True)  # Amethyst Kinkajou can jump 3 spaces over Tangerine Okapi

    def test_captured_pieces(self):
        '''Tests pieces are properly captured when the opposing side moves a piece to it's piece's place. Also
        tests that a piece cannot take one of it's own side'''
        animal_1 = AnimalGame()
        self.assertEqual(animal_1.make_move('a1', 'a5'), True)  # Tangerine Okapi moves 4 spaces down
        self.assertEqual(animal_1.make_move('a7', 'a5'), True)  # Amethyst Okapi moves 2 spaces up and captures Tangerine Okapi
        self.assertEqual(animal_1._board[4][0].get_owner(), 'A') # getting the value at board[4][0] which is the same as 'a5' will equal 'A' for Amethyst showing that Amethyst has taken the tangerine Okapi
        self.assertEqual(animal_1.make_move('b1', 'c1'), False) # Tangerine Wombat tries to move one space to the right which would capture it's own Kinkajou, returns false

    def test_turn_order(self):
        '''Tests proper turn order. Game should start with Tangerine having the move, and should switch to Amethyst
        after the first move. After the second move it should switch back to Tangerine'''
        animal_1 = AnimalGame()
        self.assertEqual(animal_1._turn, 'T') # Game starts with Tangerine having the first move
        animal_1.make_move('a1', 'a5')  # Tangerine Okapi moves 4 spaces down
        self.assertEqual(animal_1._turn, 'A')  # Turn is now Amethyst's after Tangerine has moved
        animal_1.make_move('c7', 'c6')  # Amethyst moves
        self.assertEqual(animal_1._turn, 'T')  # Turn is now Tangerine after Amethyst has moved

    def test_game_state(self):
        '''tests get_game_state() functions properly before and after a Cuttlefish is captured'''
        animal_1 = AnimalGame()
        self.assertEqual(animal_1.get_game_state(), 'UNFINISHED')
        animal_1.make_move('d1', 'f3')  # Tangerine Cuttlefish moves 2 spaces down-right
        animal_1.make_move('c7', 'c6')  # Amethyst Kinkajou moves up one space
        animal_1.make_move('a1', 'a2')  # Tangerine moves
        animal_1.make_move('c6', 'f3')  # Amethyst Kinkajou takes Tangerine Cuttlefish
        self.assertEqual(animal_1.get_game_state(), "AMETHYST_WON")
