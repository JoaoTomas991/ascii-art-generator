#!/bin/bash
# ASCII Art Generator - Start Script

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 not found!${NC}"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

# Get project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}     ASCII Art Generator - Start      ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Show options
echo "Select execution mode:"
echo ""
echo -e "  ${GREEN}[1]${NC} Menu Mode (interactive interface)"
echo -e "  ${GREEN}[2]${NC} Intelligent Mode (English natural commands)"
echo -e "  ${GREEN}[3]${NC} Direct Command"
echo -e "  ${GREEN}[4]${NC} Show Help"
echo ""

read -p "Option: " choice

case $choice in
    1)
        echo -e "\n${BLUE}Starting menu mode...${NC}\n"
        python run.py
        ;;
    2)
        echo -e "\n${BLUE}Starting intelligent mode...${NC}\n"
        python run.py --intelligent
        ;;
    3)
        read -p "Command (e.g., 'draw a heart'): " cmd
        if [ -n "$cmd" ]; then
            echo -e "\n${BLUE}Executing: $cmd${NC}\n"
            python run.py "$cmd"
        else
            echo -e "${YELLOW}No command provided${NC}"
        fi
        ;;
    4)
        echo -e "\n${BLUE}Help:${NC}\n"
        python run.py --help
        ;;
    *)
        echo -e "\n${YELLOW}Invalid option. Using default menu mode...${NC}\n"
        python run.py
        ;;
esac
