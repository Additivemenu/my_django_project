import json
from pathlib import Path

class UserStorage:
    def __init__(self, file_path: str = "users.json"):
        self.file_path = file_path

    def save_user(self, name: str, age: int) -> dict:
        """Save user data to a JSON file"""
        user_data = {"name": name, "age": age}
        
        try:
            # Check if file exists and read existing data
            if Path(self.file_path).exists():
                with open(self.file_path, 'r') as f:
                    users = json.load(f)
            else:
                users = []
            
            # Add new user
            users.append(user_data)
            
            # Save updated data
            with open(self.file_path, 'w') as f:
                json.dump(users, f)
            
            return user_data
            
        except Exception as e:
            print(f"Error saving user: {e}")
            raise
