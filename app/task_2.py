import unittest
from app.task_1 import get_score


class TestGetScore(unittest.TestCase):

    def test_exact_match(self):
        game_stamps = [
            {"offset": 0, "score": {"home": 0, "away": 0}},
            {"offset": 10, "score": {"home": 1, "away": 0}},
            {"offset": 20, "score": {"home": 1, "away": 1}},
            {"offset": 30, "score": {"home": 2, "away": 1}},
        ]
        self.assertEqual(get_score(game_stamps, 10), (1, 0))

    def test_before_first_stamp(self):
        game_stamps = [
            {"offset": 10, "score": {"home": 1, "away": 0}},
            {"offset": 20, "score": {"home": 1, "away": 1}},
            {"offset": 30, "score": {"home": 2, "away": 1}},
        ]
        self.assertEqual(get_score(game_stamps, 5), (0, 0))

    def test_between_stamps(self):
        game_stamps = [
            {"offset": 0, "score": {"home": 0, "away": 0}},
            {"offset": 10, "score": {"home": 1, "away": 0}},
            {"offset": 20, "score": {"home": 1, "away": 1}},
            {"offset": 30, "score": {"home": 2, "away": 1}},
        ]
        self.assertEqual(get_score(game_stamps, 15), (1, 0))

    def test_after_last_stamp(self):
        game_stamps = [
            {"offset": 0, "score": {"home": 0, "away": 0}},
            {"offset": 10, "score": {"home": 1, "away": 0}},
            {"offset": 20, "score": {"home": 1, "away": 1}},
            {"offset": 30, "score": {"home": 2, "away": 1}},
        ]
        self.assertEqual(get_score(game_stamps, 35), (2, 1))

    def test_empty_game_stamps(self):
        game_stamps = []
        self.assertEqual(get_score(game_stamps, 10), (0, 0))

    def test_negative_offset(self):
        game_stamps = [
            {"offset": 0, "score": {"home": 0, "away": 0}},
            {"offset": 10, "score": {"home": 1, "away": 0}},
            {"offset": 20, "score": {"home": 1, "away": 1}},
            {"offset": 30, "score": {"home": 2, "away": 1}},
        ]
        self.assertEqual(get_score(game_stamps, -5), (0, 0))