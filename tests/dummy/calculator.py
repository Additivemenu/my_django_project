# calculator.py
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def get_user_status(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age < 18:
        return "minor"
    if age < 65:
        return "adult"
    return "senior"