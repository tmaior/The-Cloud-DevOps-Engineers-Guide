import unittest
from unittest.mock import patch, MagicMock
import random
import pygame

# Importing the game logic functions from the file
from game_logic import main_game, questions

class TestRomanEmpireQuiz(unittest.TestCase):

    @patch('pygame.display.update')
    @patch('pygame.font.Font')
    @patch('game_logic.get_text_height')
    @patch('game_logic.draw_text')
    @patch('game_logic.draw_border')
    @patch('pygame.event.get')
    @patch('game_logic.congratulations_screen', return_value=False)
    @patch('game_logic.game_over_screen', return_value=False)
    def test_correct_answer(self, mock_game_over_screen, mock_congratulations_screen, mock_event_get, mock_draw_border, mock_draw_text, mock_get_text_height, mock_font, mock_display_update):
        # Set up mock event sequence for answering correctly
        mock_event_get.side_effect = [
            [MagicMock(type=pygame.KEYDOWN, key=pygame.K_1)],
            [MagicMock(type=pygame.KEYDOWN, key=pygame.K_1)]
        ]
        
        # Patch the random sample to control which questions are selected
        selected_questions = [
            questions[0],  # Question 1: "Who was the first Roman Emperor?"
            questions[1]   # Question 2: "Which emperor built a massive wall across Britain?"
        ]
        
        with patch('random.sample', return_value=selected_questions):
            main_game()
        
        # Assert that the congratulations screen was called
        mock_congratulations_screen.assert_called_once()

    @patch('pygame.display.update')
    @patch('pygame.font.Font')
    @patch('game_logic.get_text_height')
    @patch('game_logic.draw_text')
    @patch('game_logic.draw_border')
    @patch('pygame.event.get')
    @patch('game_logic.congratulations_screen', return_value=False)
    @patch('game_logic.game_over_screen', return_value=False)
    def test_incorrect_answer(self, mock_game_over_screen, mock_congratulations_screen, mock_event_get, mock_draw_border, mock_draw_text, mock_get_text_height, mock_font, mock_display_update):
        # Set up mock event sequence for answering incorrectly
        mock_event_get.side_effect = [
            [MagicMock(type=pygame.KEYDOWN, key=pygame.K_2)],  # Incorrect for the first question
            [MagicMock(type=pygame.KEYDOWN, key=pygame.K_2)]   # Incorrect for the second question
        ]
        
        # Patch the random sample to control which questions are selected
        selected_questions = [
            questions[0],  # Question 1: "Who was the first Roman Emperor?"
            questions[1]   # Question 2: "Which emperor built a massive wall across Britain?"
        ]
        
        with patch('random.sample', return_value=selected_questions):
            main_game()
        
        # Assert that the game over screen was called
        mock_game_over_screen.assert_called()

    @patch('pygame.display.update')
    @patch('pygame.font.Font')
    @patch('game_logic.get_text_height')
    @patch('game_logic.draw_text')
    @patch('game_logic.draw_border')
    @patch('pygame.event.get')
    @patch('game_logic.congratulations_screen', return_value=False)
    @patch('game_logic.game_over_screen', return_value=False)
    def test_mixed_answers(self, mock_game_over_screen, mock_congratulations_screen, mock_event_get, mock_draw_border, mock_draw_text, mock_get_text_height, mock_font, mock_display_update):
        # Set up mock event sequence for one correct and one incorrect answer
        mock_event_get.side_effect = [
            [MagicMock(type=pygame.KEYDOWN, key=pygame.K_1)],  # Correct for the first question
            [MagicMock(type=pygame.KEYDOWN, key=pygame.K_2)]   # Incorrect for the second question
        ]
        
        # Patch the random sample to control which questions are selected
        selected_questions = [
            questions[0],  # Question 1: "Who was the first Roman Emperor?"
            questions[1]   # Question 2: "Which emperor built a massive wall across Britain?"
        ]
        
        with patch('random.sample', return_value=selected_questions):
            main_game()
        
        # Assert that the game over screen was not called
        mock_game_over_screen.assert_not_called()
        # Assert that the congratulations screen was called
        mock_congratulations_screen.assert_called_once()

if __name__ == '__main__':
    unittest.main()