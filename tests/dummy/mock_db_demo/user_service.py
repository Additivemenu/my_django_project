class UserService:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_user_by_id(self, user_id):
        query = "SELECT * FROM users WHERE id = %s"
        results = self.db.execute_query(query, [user_id])
        if not results:
            raise ValueError(f"User with id {user_id} not found")
        return results[0]
    
    def get_user_email(self, user_id):
        user = self.get_user_by_id(user_id)
        return user["email"]