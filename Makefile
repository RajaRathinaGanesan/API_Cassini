.PHONY: help install test test-unit test-integration clean

# Default target
help:
	@echo "QA Automation Assessment Framework"
	@echo "================================"
	@echo ""
	@echo "Available targets:"
	@echo "  install              Install dependencies with uv"
	@echo "  test                 Run all tests"
	@echo "  test-unit            Run unit tests only"
	@echo "  test-integration     Run integration tests only"
	@echo "  clean                Clean up generated files"
	@echo ""

# Install dependencies with uv
install:
	uv sync

# Run all tests
test:
	uv run pytest

# Run unit tests only
test-unit:
	uv run pytest tests/unit/ -v

# Run integration tests only
test-integration:
	uv run pytest tests/integration/ -v

# Clean up generated files
clean:
	rm -rf .pytest_cache/
	rm -rf logs/
	rm -rf temp/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
