# ASCII Generator - Makefile
# Easier execution and development for the ASCII Generator project

# Interpreter used by every target. Linux/macOS generally only ship "python3";
# override on platforms where the binary has another name, e.g.:
#   make run PYTHON=python
PYTHON ?= python3

.PHONY: help run intelligent command test install clean

# Colors for output
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m

help: ## Show this help
	@echo "ASCII Generator - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

run: ## Start the project in menu mode
	@echo "$(BLUE)Starting ASCII Generator (menu mode)...$(NC)"
	$(PYTHON) run.py

intelligent: ## Start in intelligent mode
	@echo "$(BLUE)Starting ASCII Generator (intelligent mode)...$(NC)"
	$(PYTHON) run.py --intelligent

# Command shortcuts
command-draw: ## Draw a rectangle
	@$(PYTHON) run.py "draw a rectangle 10x5"

command-circle: ## Draw a circle
	@$(PYTHON) run.py "make a circle with radius 8"

command-heart: ## Draw a heart
	@$(PYTHON) run.py "draw a heart"

command-tree: ## Draw a tree
	@$(PYTHON) run.py "create a tree with height 10"

command-banner: ## Create a banner
	@$(PYTHON) run.py "make a banner with text ASCII ART"

command-text: ## Convert text to ASCII
	@$(PYTHON) run.py "write HELLO with font banner"

# Test commands
test: ## Run basic tests
	@echo "$(BLUE)Running tests...$(NC)"
	@$(PYTHON) -c "from ascii_art_generator.ascii_art import draw_rectangle, draw_circle, draw_heart, draw_diamond, text_to_ascii; print('Import tests: OK')"
	@$(PYTHON) -c "from ascii_art_generator.cli import ENCommandParser; p = ENCommandParser(); print('Parser tests: OK')"
	@echo "$(GREEN)All tests passed!$(NC)"

test-shape: ## Test shape generation
	@echo "$(BLUE)Testing shapes...$(NC)"
	@$(PYTHON) run.py "draw a rectangle 5x3"
	@echo ""
	@$(PYTHON) run.py "make a circle with radius 5"

-test-text: ## Test text conversion
	@echo "$(BLUE)Testing text...$(NC)"
	@$(PYTHON) run.py "write TEST with font small"

# Installation
install: ## Install dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	$(PYTHON) -m pip install -r requirements.txt 2>/dev/null || echo "$(YELLOW)No requirements.txt found$(NC)"
	@echo "$(GREEN)Installation complete!$(NC)"

# Clean
clean: ## Remove temporary files and cache
	@echo "$(BLUE)Cleaning temporary files...$(NC)"
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf .pytest_cache
	rm -rf *.pyc
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)Cleanup complete!$(NC)"

# Development commands
dev: run ## Start in development mode (alias for run)

# Show version
version: ## Show version
	@echo "$(BLUE)ASCII Generator v1.0.0$(NC)"
	@$(PYTHON) -c "import sys; print(f'Python: {sys.version}')"
