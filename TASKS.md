# QA Automation Engineer Assessment

## Overview

Welcome to the QA Automation Engineer assessment! This repository contains a pytest framework for API testing using the RESTful Booker API. Your task is to review and improve the existing tests and implement comprehensive tests for a new endpoint.

We are automating APIs from the RESTful Booker service. The API documentation can be found at: https://restful-booker.herokuapp.com/apidoc/index.html

**Tech Stack:**
- pytest framework
- loguru for logging
- requests library (via custom API client)
- uv for dependency management

## Assessment Criteria

You will be evaluated on:
- **Test Design**: Quality of test scenarios and pytest feature usage (parameterization, fixtures, markers)
- **Code Quality**: Clean, maintainable, production-ready code following Python standards
- **Problem Solving**: Ability to identify issues and implement solutions independently
- **API Testing**: Understanding of REST API testing principles (status codes, response validation, error handling)

---

## Part 1: Review and Improve Existing Tests (Mandatory)

Review the existing test files and identify areas for improvement. Analyze the code, run the tests, and apply pytest best practices to improve quality, maintainability, and coverage.

**Files to review:**

1. **`tests/conftest.py`** - Fixture configuration
   - Review fixture scopes (function, module, session)
   - Check for exposed credentials or hardcoded values
   - Evaluate exception handling
   - Consider data immutability and isolation

2. **`tests/unit/`** - Unit test files
   - Review assertion depth and test coverage
   - Look for opportunities to use parameterization
   - Ensure tests validate response structure, not just status codes
   - Check test isolation and data handling

3. **`tests/integration/`** - Integration test files
   - Review test data setup/teardown
   - Check for proper cleanup to avoid test pollution
   - Evaluate full lifecycle testing

**What we're looking for:**
- Appropriate fixture scopes and reusable fixtures
- Parameterized tests to reduce duplication
- Comprehensive assertions (response structure, data types, validation)
- Secure credential management (config files, not hardcoded)
- Proper test data creation and cleanup
- Test isolation (tests don't affect each other)
- Type hints, docstrings, and PEP 8 compliance

---

## Part 2: Implement Comprehensive Tests for a New Endpoint (Mandatory)

**Scenario:** We are planning to implement comprehensive testing for a new endpoint from the RestfulBookerClient. Your task is to select an endpoint from the `RestfulBookerClient` class (located in `tools/api_client.py`) and create a complete test suite for it.

**Your Task:**

1. **Select an endpoint** from the RestfulBookerClient that you believe needs more comprehensive testing coverage. Review existing test files to identify which endpoints may be under-tested.

2. **Create a new test file** in the `tests/integration/` directory for your chosen endpoint.

3. **Implement comprehensive test coverage** including positive test cases, negative test cases, error handling scenarios, performance considerations, and edge cases. Ensure your tests validate response structure and data integrity, not just HTTP status codes.

4. **Fixture Management:** Reuse existing fixtures from `tests/conftest.py` where appropriate, but feel free to modify or create new fixtures as needed for your test scenarios. Ensure proper fixture scoping and test data setup/cleanup.

5. **Test Organization:** Use pytest parameterization where appropriate, group related tests logically, use descriptive test names, and add docstrings to explain test scenarios.

**What we're looking for:**
- Comprehensive test coverage across all test categories
- Proper use of existing fixtures with modifications or new fixtures as needed
- Clean, maintainable test code following pytest best practices
- Well-structured assertions that validate response structure, not just status codes
- Proper test isolation and data cleanup

---

## Deliverables

1. **Improved existing tests** - Part 1 reviews and fixes completed with best practices applied
2. **Comprehensive endpoint test suite** - Part 2 complete test file with positive, negative, performance, edge cases, and error handling tests
3. **Code quality** - PEP 8, type hints, docstrings on test functions
4. **Documentation** - README updated with setup, execution, and configuration instructions
5. **Test results** - All tests passing successfully

---

## Success Metrics

Your work will be evaluated based on:
- **Code Quality**: Production-ready code following Python standards
- **Test Design**: Well-structured tests using pytest best practices
- **Coverage**: Comprehensive assertions validating response structure
- **Problem Solving**: Ability to identify and resolve issues independently
- **Maintainability**: Clean organization, reusable code, clear documentation

Good luck! Demonstrate your expertise in QA automation and testing best practices. 🚀
