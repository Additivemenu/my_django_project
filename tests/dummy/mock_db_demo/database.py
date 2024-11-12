# database.py
class DatabaseConnection:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.is_connected = False
    
    def connect(self):
        # In real implementation, this would establish a DB connection
        self.is_connected = True
    
    def disconnect(self):
        self.is_connected = False
    
    def execute_query(self, query, params=None):
        if not self.is_connected:
            raise ConnectionError("Not connected to database")
        # Simulate query execution
        if query.startswith("SELECT") and "users" in query:
            return [{"id": 1, "name": "John Doe", "email": "john@example.com"}]
        return []