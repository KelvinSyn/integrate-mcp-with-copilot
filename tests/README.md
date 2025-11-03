# Tests Documentation

This directory contains unit and integration tests for the High School Management System API.

## Test Structure

- **`conftest.py`** - Pytest configuration and shared fixtures
- **`test_api_endpoints.py`** - Unit tests for individual API endpoints
- **`test_integration.py`** - Integration tests for complete workflows

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Tests with Verbose Output
```bash
pytest -v
```

### Run Tests with Coverage Report
```bash
pytest --cov=src --cov-report=term-missing
```

### Run Specific Test File
```bash
pytest tests/test_api_endpoints.py
```

### Run Specific Test Class
```bash
pytest tests/test_api_endpoints.py::TestSignupEndpoint
```

### Run Specific Test Function
```bash
pytest tests/test_api_endpoints.py::TestSignupEndpoint::test_signup_for_valid_activity_returns_200
```

## Test Coverage

Current test coverage: **100%** of application code

### Coverage Areas

#### Unit Tests (`test_api_endpoints.py`)
- **Root Endpoint** (`/`)
  - Redirect functionality
  
- **Get Activities Endpoint** (`GET /activities`)
  - Returns 200 OK status
  - Returns dictionary of activities
  - Contains all expected activities
  - Correct data structure validation
  - Participants list validation

- **Signup Endpoint** (`POST /activities/{activity_name}/signup`)
  - Valid signup returns 200 OK
  - Student is added to activity
  - Success message format
  - Non-existent activity returns 404
  - Duplicate signup returns 400
  - Error message validation
  - URL encoding handling
  - Multiple students can signup

- **Unregister Endpoint** (`DELETE /activities/{activity_name}/unregister`)
  - Valid unregister returns 200 OK
  - Student is removed from activity
  - Success message format
  - Non-existent activity returns 404
  - Not signed up returns 400
  - Error message validation
  - URL encoding handling

- **Parameter Validation**
  - Required email parameter validation

#### Integration Tests (`test_integration.py`)
- **Student Signup Workflows**
  - Complete signup workflow (view → signup → verify)
  - Signup and unregister workflow
  
- **Multiple Activity Management**
  - Student joining multiple activities
  - Leaving one activity while staying in others
  
- **Activity Capacity Management**
  - Multiple students filling up an activity
  
- **Concurrent Operations**
  - Multiple signups and unregisters in sequence
  
- **Error Recovery**
  - Failed operations don't corrupt state
  - State consistency after errors
  
- **Data Consistency**
  - Data persistence across requests
  - Structure validation for all activities
  
- **Edge Cases**
  - Signup → Unregister → Signup again
  - Operations on all activities

## Test Fixtures

### `client`
Provides a FastAPI TestClient instance for making HTTP requests to the API.
- **Scope**: Function (new instance per test)
- **Usage**: Passed as parameter to test functions

### `reset_activities`
Automatically resets activity data to initial state before and after each test.
- **Scope**: Function
- **Auto-use**: Yes (runs automatically for all tests)
- **Purpose**: Ensures test isolation

## Dependencies

- `pytest` - Testing framework
- `httpx` - Async HTTP client for FastAPI testing
- `pytest-cov` - Coverage reporting
- `fastapi` - Web framework
- `fastapi.testclient` - Test client for FastAPI applications

## Writing New Tests

When adding new tests:

1. **Unit tests**: Add to `test_api_endpoints.py` in appropriate test class
2. **Integration tests**: Add to `test_integration.py` in appropriate test class
3. **New fixtures**: Add to `conftest.py`
4. **Follow naming conventions**: 
   - Test files: `test_*.py`
   - Test classes: `Test*`
   - Test functions: `test_*`

## CI/CD Integration

These tests are designed to be easily integrated into CI/CD pipelines:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests with coverage
pytest --cov=src --cov-report=xml --cov-report=term

# Check coverage threshold (optional)
coverage report --fail-under=80
```
