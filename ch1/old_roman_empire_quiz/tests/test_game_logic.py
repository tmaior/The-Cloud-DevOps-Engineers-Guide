import unittest
from unittest.mock import patch, MagicMock
import pygame
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
        # Set up mock event sequence for answering all questions correctly
        mock_event_get.side_effect = [
            [MagicMock(type=pygame.KEYDOWN, key=pygame.K_1)] for _ in range(10)
        ]
        
        # Mock `pygame.font.Font` to return a mock object with a `get_height` method
        mock_font_instance = MagicMock()
        mock_font_instance.get_height.return_value = 30
        mock_font.return_value = mock_font_instance

        # Mock `get_text_height` to return an integer value
        mock_get_text_height.return_value = 30

        # Patch the random sample to control which questions are selected
        selected_questions = [
            questions[0],  # Question 1
            questions[1],  # Question 2
            questions[2],  # Question 3
            questions[3],  # Question 4
            questions[4],  # Question 5
            questions[5],  # Question 6
            questions[6],  # Question 7
            questions[7],  # Question 8
            questions[8],  # Question 9
            questions[9]   # Question 10
        ]

        with patch('random.sample', return_value=selected_questions):
            main_game()

        # Assert that the congratulations screen was called
        mock_congratulations_screen.assert_called_once()
        mock_game_over_screen.assert_not_called()

    @patch('pygame.display.update')
    @patch('pygame.font.Font')
    @patch('game_logic.get_text_height')
    @patch('game_logic.draw_text')
    @patch('game_logic.draw_border')
    @patch('pygame.event.get')
    @patch('game_logic.congratulations_screen', return_value=False)
    @patch('game_logic.game_over_screen', return_value=False)
    def test_incorrect_answer(self, mock_game_over_screen, mock_congratulations_screen, mock_event_get, mock_draw_border, mock_draw_text, mock_get_text_height, mock_font, mock_display_update):
        # Set up mock event sequence for answering all questions incorrectly
        mock_event_get.side_effect = [
            [MagicMock(type=pygame.KEYDOWN, key=pygame.K_2)] for _ in range(10)
        ]
        
        # Mock `pygame.font.Font` to return a mock object with a `get_height` method
        mock_font_instance = MagicMock()
        mock_font_instance.get_height.return_value = 30
        mock_font.return_value = mock_font_instance

        # Mock `get_text_height` to return an integer value
        mock_get_text_height.return_value = 30

        # Patch the random sample to control which questions are selected
        selected_questions = [
            questions[0],  # Question 1
            questions[1],  # Question 2
            questions[2],  # Question 3
            questions[3],  # Question 4
            questions[4],  # Question 5
            questions[5],  # Question 6
            questions[6],  # Question 7
            questions[7],  # Question 8
            questions[8],  # Question 9
            questions[9]   # Question 10
        ]

        with patch('random.sample', return_value=selected_questions):
            main_game()

        # Assert that the game over screen was called
        mock_game_over_screen.assert_called_once()
        mock_congratulations_screen.assert_not_called()

    @patch('pygame.display.update')
    @patch('pygame.font.Font')
    @patch('game_logic.get_text_height')
    @patch('game_logic.draw_text')
    @patch('game_logic.draw_border')
    @patch('pygame.event.get')
    @patch('game_logic.congratulations_screen', return_value=False)
    @patch('game_logic.game_over_screen', return_value=False)
    def test_mixed_answers(self, mock_game_over_screen, mock_congratulations_screen, mock_event_get, mock_draw_border, mock_draw_text, mock_get_text_height, mock_font, mock_display_update):
        # Set up mock event sequence for mixed answers
        mock_event_get.side_effect = [
            [MagicMock(type=pygame.KEYDOWN, key=pygame.K_1)],
            [MagicMock(type=pygame.KEYDOWN, key=pygame.K_2)],
            [MagicMock(type=pygame.KEYDOWN, key=pygame.K_1)],
            [MagicMock(type=pygame.KEYDOWN, key=pygame.K_1)],
            [MagicMock(type=pygame.KEYDOWN, key=pygame.K_1)],
            [MagicMock(type=pygame.KEYDOWN, key=pygame.K_2)],
            [MagicMock(type=pygame.KEYDOWN, key=pygame.K_1)],
            [MagicMock(type=pygame.KEYDOWN, key=pygame.K_2)],
            [MagicMock(type=pygame.KEYDOWN, key=pygame.K_1)],
            [MagicMock(type=pygame.KEYDOWN, key=pygame.K_1)]
        ]
        
        # Mock `pygame.font.Font` to return a mock object with a `get_height` method
        mock_font_instance = MagicMock()
        mock_font_instance.get_height.return_value = 30
        mock_font.return_value = mock_font_instance

        # Mock `get_text_height` to return an integer value
        mock_get_text_height.return_value = 30

        # Patch the random sample to control which questions are selected
        selected_questions = [
            questions[0],  # Question 1
            questions[1],  # Question 2
            questions[2],  # Question 3
            questions[3],  # Question 4
            questions[4],  # Question 5
            questions[5],  # Question 6
            questions[6],  # Question 7
            questions[7],  # Question 8
            questions[8],  # Question 9
            questions[9]   # Question 10
        ]

        with patch('random.sample', return_value=selected_questions):
            main_game()

        # Assert that the congratulations screen was called
        mock_congratulations_screen.assert_called_once()
        mock_game_over_screen.assert_not_called()

if __name__ == '__main__':
    unittest.main()