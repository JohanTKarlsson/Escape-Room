import os

import pygame as pg
import unittest
from game import Game
from keypad import Keypad
from table_riddle import TableRiddle
from poster import Poster

class Test(unittest.TestCase):
    def setUp(self):
        # setting up the test environment to avoid errors
        pg.init()
        self.screen = pg.display.set_mode((1, 1))
        self.game = Game(self.screen, None)
        self.keypad = Keypad((0, 0))
        self.table_riddle = TableRiddle((0, 0))
        self.poster = Poster((0, 0))


    def test_score_calculation(self):
        # Test score calculation based on elapsed time and hints used
        self.game.elapsed_time = 200000  # 3 minutes 20 seconds
        self.game.hints_used = 0
        self.game.scoring()
        self.assertEqual(self.game.score, "10/10")

        self.game.elapsed_time = 400000  # 6 minutes 40 seconds
        self.game.hints_used = 1
        self.game.scoring()
        self.assertEqual(self.game.score, "8/10")

        self.game.elapsed_time = 600000  # 10 minutes
        self.game.hints_used = 2
        self.game.scoring()
        self.assertEqual(self.game.score, "5/10")

        self.game.elapsed_time = 1200000  # 20 minutes
        self.game.hints_used = 3
        self.game.scoring()
        self.assertEqual(self.game.score, "2/10")

    def test_end_of_game_attributes(self):
        # Test if end_of_game attribute is set to True and other attributes are set to None
        self.game.game_over()
        self.assertTrue(self.game.end_of_game)
        self.assertIsNone(self.game.poster)
        self.assertIsNone(self.game.table)
        self.assertIsNone(self.game.book)
        self.assertIsNone(self.game.table_riddle)
        self.assertIsNone(self.game.door)

    def test_check_code_keypad(self):

        result = self.keypad.check_code("3249")
        wrong_code = self.keypad.check_code("3232")

        self.assertTrue(result)
        self.assertFalse(wrong_code)
    
    def test_check_code_table_riddle(self):

        result = self.table_riddle.check_code("134")
        wrong_code = self.table_riddle.check_code("460")

        self.assertTrue(result)
        self.assertFalse(wrong_code)

    def test_check_code_poster(self):

        result = self.poster.check_code("SOLUTION")
        wrong_code = self.poster.check_code("MACKEREL")

        self.assertTrue(result)
        self.assertFalse(wrong_code)

if __name__ == "__main__":
    unittest.main()
