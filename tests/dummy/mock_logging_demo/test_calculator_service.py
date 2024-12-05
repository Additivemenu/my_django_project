# test_calculator_service.py
import pytest
from unittest.mock import patch
from calculator_service import CalculatorService

class TestCalculatorService:
    @pytest.fixture
    def calculator(self):
        return CalculatorService()
    
    @patch('logging.info')
    def test_add_numbers_success(self, mock_log, calculator):
        # Arrange is handled by fixture
        
        # Act
        result = calculator.add_numbers_with_logging(2, 3)
        
        # Assert
        assert result == 5
        
        # Verify logging was called twice
        assert mock_log.call_count == 2
        # You can also check the specific log messages
        mock_log.assert_any_call("Adding numbers 2 and 3")  # Note: datetime will vary
        mock_log.assert_any_call("Result is 5")

    @patch('logging.info')
    @patch('logging.error')
    def test_add_numbers_with_exception(self, mock_log_error, mock_log_info, calculator):
        # Arrange
        invalid_input_a = "not"
        invalid_input_b = "numbers"
        
        # Act & Assert
        with pytest.raises(TypeError) as exc_info:
            calculator.add_numbers_with_logging(invalid_input_a, invalid_input_b)
        
        # Verify the exception message
        assert "must be numbers" in str(exc_info.value) or "unsupported operand" in str(exc_info.value)
        
        # Verify logging calls
        mock_log_info.assert_not_called()  # Should not log info for invalid inputs
        mock_log_error.assert_called_once()
        
        # Verify error message
        error_msg = mock_log_error.call_args[0][0]
        assert "Error during calculation" in error_msg

    # You can also add more test cases easily
    @patch('logging.info')
    def test_add_negative_numbers(self, mock_log, calculator):
        # Act
        result = calculator.add_numbers_with_logging(-2, -3)
        
        # Assert
        assert result == -5
        assert mock_log.call_count == 2
        mock_log.assert_any_call("Adding numbers -2 and -3")
        mock_log.assert_any_call("Result is -5")

    @pytest.mark.parametrize("a, b, expected", [
        (1, 1, 2),
        (0, 0, 0),
        (-1, 1, 0),
        (100, -100, 0),
    ])
    @patch('logging.info')
    def test_add_numbers_parametrized(self, mock_log, calculator, a, b, expected):
        # Act
        result = calculator.add_numbers_with_logging(a, b)
        
        # Assert
        assert result == expected
        assert mock_log.call_count == 2