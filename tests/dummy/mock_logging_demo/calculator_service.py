# calculator_service.py
import logging
from datetime import datetime

class CalculatorService:
    def add_numbers_with_logging(self, a: int, b: int) -> int:
        """Add two numbers and log the operation"""
        try:
            if not isinstance(a, int) or not isinstance(b, int):
                raise TypeError("Both inputs must be numbers")
            
            # Log the operation
            logging.info(f"Adding numbers {a} and {b}")
            
            # Perform calculation
            result = a + b
            
            # Log the result
            logging.info(f"Result is {result}")
            
            return result
            
        except Exception as e:
            logging.error(f"Error during calculation: {str(e)}")
            raise

calculator_service = CalculatorService()
result = calculator_service.add_numbers_with_logging(2, 3)
print(result)  # Output: 5

invalid_input_a = "not"
invalid_input_b = "numbers"
res = calculator_service.add_numbers_with_logging(invalid_input_a, invalid_input_b)
print(res)  # Output: TypeError: unsupported operand type(s) for +: 'str' and 'str'