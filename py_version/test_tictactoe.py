import unittest
from unittest.mock import patch
import minimax

class TestTicTacToe(unittest.TestCase):
# ce en test spremeni board, drug dobi spremenjenega
    def setUp(self):
        minimax.board[:] = [ 
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ]

    # HAPPY PATH
    # ali se veljavna poteza pravilno izvede
    def test_valid_move(self):
        result = minimax.set_move(0,0,minimax.HUMAN) # cloveski igralec v kodi -1
        self.assertTrue(result) 
        self.assertEqual(minimax.board[0][0], minimax.HUMAN) # da se vrednost na plošči spremenila
 
    # ali wins pravilno zazna zmago v vrstici
    def test_wins_row(self):
        board = [ 
            [minimax.COMP, minimax.COMP, minimax.COMP],
            [0,0,0],
            [0,0,0]
        ]
        self.assertTrue(minimax.wins(board, minimax.COMP)) # ali je igralec zmagal

    def test_evaluate_comp_win(self):
        board = [
            [minimax.COMP, minimax.COMP, minimax.COMP],
            [0,0,0],
            [0,0,0]
        ]
        self.assertEqual(minimax.evaluate(board), 1) 

    # INVALID INPUT
    # ali igra zavrne potezo na že zasedeno polje
    def test_invalid_move_on_taken_cell(self):
        minimax.set_move(0,0,minimax.HUMAN) 
        result = minimax.set_move(0,0,minimax.COMP) 

        self.assertFalse(result) 

# ali igra pravilno zavrne koordinate, ki niso na plošči
    def test_invalid_coordinates(self):
        invalid_moves = [
            (-1,0),
            (3,3),
            (5,1)
        ]

        for x,y in invalid_moves:
            with self.subTest(x=x,y=y): # vsak obravnava kot podtest
                self.assertFalse(minimax.valid_move(x,y)) # preveri ali je poteza dovoljena

    @patch("builtins.input", side_effect=["abc","10","1"])
    @patch("minimax.clean")
    @patch("minimax.render")
    def test_invalid_human_input(self, mock_render, mock_clean, mock_input):

        minimax.human_turn("O","X") # klice rac potezo
        self.assertEqual(minimax.board[0][0], minimax.HUMAN)

    # EDGE CASE
    # da funkcija pravilno vrne prazen seznam ko je plošča polna
    def test_full_board_empty_cells(self):

        full_board = [
            [1,-1,1],
            [-1,1,-1],
            [-1,1,-1]
        ]

        cells = minimax.empty_cells(full_board)

        self.assertEqual(cells, [])

    def test_last_move(self):

        minimax.board[:] = [
            [1,-1,1],
            [-1,1,-1],
            [-1,1,0]
        ]

        minimax.set_move(2,2,minimax.COMP)

        self.assertEqual(len(minimax.empty_cells(minimax.board)),0) # preveri da ni vec praznih celic

    # MOCK TEST
    @patch("minimax.choice", side_effect=[1,2])
    @patch("minimax.clean")
    @patch("minimax.render")
    @patch("minimax.time.sleep")
    def test_ai_first_move_random(self, mock_sleep, mock_render, mock_clean, mock_choice):

        minimax.ai_turn("O","X")

        self.assertEqual(minimax.board[1][2], minimax.COMP)


if __name__ == "__main__":
    unittest.main()