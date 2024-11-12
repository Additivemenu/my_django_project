import pytest
from .calculator import add, divide, get_user_status

"""
just a dummy test file to show some examples of pytest features (no django specific testing features)
These examples demonstrate key pytest features:

1. Basic Assertions: Simple test using assert
2. Fixtures: Reusable test data/setup
3. Setup/Teardown: Using yield in fixtures
4. Parametrization: Running same test with different inputs
5. Exception Testing: Using pytest.raises
6. Markers: @pytest.mark.slow, skip, xfail
7. Test Organization: Using classes
8. Fixture Scopes: scope="module"
9. Nested Tests: Class hierarchy
10. Conditional Tests: Using skipif
"""

# 1. Basic Test
def test_add():
    assert add(1, 2) == 3

# 2. Fixture Example
@pytest.fixture
def sample_numbers():
    return [1, 2, 3, 4, 5]

# ! you see the input to a test function is the fixture name -> this test function is using the fixture to create mock data or behavior
def test_using_fixture(sample_numbers):
    assert len(sample_numbers) == 5
    assert sum(sample_numbers) == 15

# 3. Fixture with Setup and Teardown
@pytest.fixture
def database():
    print("\nConnecting to test database...")  # Setup
    db = {"connected": True}
    yield db  # ! This is what the test will use
    print("\nDisconnecting test database...")  # Teardown

def test_database(database):
    assert database["connected"] is True

# 4. Parametrize Example
@pytest.mark.parametrize("a, b, expected", [
    (3, 5, 8),
    (-1, 1, 0),
    (0, 0, 0),
    (10, -5, 5),
])
def test_add_params(a, b, expected):
    assert add(a, b) == expected

# 5. FIXME: Testing Exceptions ??????????
def test_divide_by_zero():
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)
    assert str(exc_info.value) == "Cannot divide by zero"

# ! 6. Mark Examples
@pytest.mark.slow
def test_slow_operation():
    import time
    time.sleep(1)
    assert True

@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    pass

@pytest.mark.xfail(reason="Known bug #123")
def test_known_bug():
    assert 1 == 2  # This will fail but won't affect test suite results

# ! 7. Test Class Organization
class TestUserStatus:
    def test_minor(self):
        assert get_user_status(15) == "minor"
    
    def test_adult(self):
        assert get_user_status(30) == "adult"
    
    def test_senior(self):
        assert get_user_status(70) == "senior"
    
    def test_invalid_age(self):
        """
        Here's what the with statement is doing:
            pytest.raises(ValueError) is a context manager provided by pytest.
            The context manager expects a ValueError exception to be raised within the with block.
            If get_user_status(-5) raises a ValueError, the test passes.
            If no exception or a different exception is raised, the test fails.
        """
        with pytest.raises(ValueError): # what is 'with' - context manager
            get_user_status(-5)

# 8. Fixture Scope Example
@pytest.fixture(scope="module")
def expensive_operation():
    print("\nDoing expensive setup...")
    data = {"result": 42}
    yield data
    print("\nCleaning up expensive operation...")

def test_first_use(expensive_operation):
    assert expensive_operation["result"] == 42

def test_second_use(expensive_operation):
    assert expensive_operation["result"] == 42

# 9. Nested Test Classes with Fixtures
class TestMathOperations:
    @pytest.fixture
    def base_number(self):
        return 10
    
    class TestAddition:
        def test_positive(self, base_number):
            assert add(base_number, 5) == 15
        
        def test_negative(self, base_number):
            assert add(base_number, -5) == 5
    
    class TestDivision:
        def test_valid(self, base_number):
            assert divide(base_number, 2) == 5

# 10. Conditional Skip
@pytest.mark.skipif(
    not hasattr(list, "some_future_method"),
    reason="Python version doesn't support this feature"
)
def test_future_list_feature():
    pass