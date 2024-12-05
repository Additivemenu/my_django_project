# test_user_storage.py
import pytest
import unittest
from unittest.mock import patch, mock_open
from user_storage import UserStorage

class TestUserStorage:
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.storage = UserStorage("test_users.json")

    @patch('pathlib.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_first_user(self, mock_file, mock_exists):
        # Arrange
        mock_exists.return_value = False  # File doesn't exist yet
        
        # Act
        result = self.storage.save_user("John", 30)
        
        # Assert
        assert result == {"name": "John", "age": 30}
        
        # Verify file operations
        mock_file.assert_called_once_with("test_users.json", "w")
        mock_file().write.assert_called_once_with('[{"name": "John", "age": 30}]')

    @patch('pathlib.Path.exists')
    @patch('builtins.open')
    def test_save_additional_user(self, mock_file, mock_exists):
        # Arrange
        mock_exists.return_value = True  # File exists
        mock_file.side_effect = [
            mock_open(read_data='[{"name": "Alice", "age": 25}]').return_value,
            mock_open().return_value
        ]
        
        # Act
        result = self.storage.save_user("Bob", 35)
        
        # Assert
        assert result == {"name": "Bob", "age": 35}
        
        # Verify file operations
        assert mock_file.call_count == 2  # Once for read, once for write
        mock_file().write.assert_called_once_with(
            '[{"name": "Alice", "age": 25}, {"name": "Bob", "age": 35}]'
        )

    @patch('pathlib.Path.exists')
    @patch('builtins.open')
    def test_save_user_with_file_error(self, mock_file, mock_exists):
        # Arrange
        mock_exists.return_value = True
        mock_file.side_effect = IOError("Permission denied")
        
        # Act & Assert
        with unittest.TestCase().assertRaises(IOError):
            self.storage.save_user("John", 30)