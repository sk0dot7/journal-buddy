#!/bin/bash

echo "     ██╗ ██████╗ ██╗   ██╗██████╗ ███╗   ██╗ █████╗ ██╗        "
echo "     ██║██╔═══██╗██║   ██║██╔══██╗████╗  ██║██╔══██╗██║        "
echo "     ██║██║   ██║██║   ██║██████╔╝██╔██╗ ██║███████║██║        "
echo "██   ██║██║   ██║██║   ██║██╔══██╗██║╚██╗██║██╔══██║██║        "
echo "╚█████╔╝╚██████╔╝╚██████╔╝██║  ██║██║ ╚████║██║  ██║███████╗   "
echo " ╚════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝   "
echo ""
echo "        ██████╗ ██╗   ██╗██████╗ ██████╗ ██╗   ██╗"
echo "        ██╔══██╗██║   ██║██╔══██╗██╔══██╗╚██╗ ██╔╝"
echo "        ██████╔╝██║   ██║██║  ██║██║  ██║ ╚████╔╝ "
echo "        ██╔══██╗██║   ██║██║  ██║██║  ██║  ╚██╔╝  "
echo "        ██████╔╝╚██████╔╝██████╔╝██████╔╝   ██║   "
echo "        ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝    ╚═╝   "
echo ""
echo "               Journal Buddy – Setup Script"
echo "==================================================================="
echo ""


# Check Python version
echo "Checking Python version..."
python3_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
required_version="3.10"

if (( $(echo "$python3_version < $required_version" | bc -l) )); then
    echo "❌ Error: Python 3.10+ required. You have Python $python3_version"
    exit 1
fi
echo "✅ Python $python3_version found"
echo ""


# Check if Ollama is installed

echo " ██████╗  ██╗     ██╗      █████╗ ███╗   ███╗ █████╗ "
echo "██╔═══██╗ ██║     ██║     ██╔══██╗████╗ ████║██╔══██╗"
echo "██║   ██║ ██║     ██║     ███████║██╔████╔██║███████║"
echo "██║   ██║ ██║     ██║     ██╔══██║██║╚██╔╝██║██╔══██║"
echo "╚██████╔╝ ███████╗███████╗██║  ██║██║ ╚═╝ ██║██║  ██║"
echo " ╚═════╝  ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝"
echo ""

echo "------------------------------------------------------------------------"
echo "Checking for Ollama..."

if command -v ollama &> /dev/null; then
    echo "✅ Ollama is installed"
else
    echo "❌ Ollama not found"
    echo ""
    echo "Would you like to install Ollama now? (y/n)"
    read -r install_ollama
    
    if [[ $install_ollama == "y" || $install_ollama == "Y" ]]; then
        echo "Installing Ollama..."
        curl -fsSL https://ollama.com/install.sh | sh
    else
        echo "Please install Ollama manually: https://ollama.com"
        exit 1
    fi
fi
echo ""

# Check if Ollama is running
echo "Checking if Ollama is running..."
if ollama list &> /dev/null; then
    echo "✅ Ollama is running"
else
    echo "⚠️  Ollama is not running"
    echo "Starting Ollama server..."
    ollama serve &
    sleep 3
fi
echo ""

echo ""
echo "────────────────────────────────────────────────────────"
echo "          🤖  OLLAMA MODEL SELECTION"
echo "────────────────────────────────────────────────────────"
echo ""
echo "Choose the AI model Journal Buddy will use."
echo "Smaller models = faster • Larger models = smarter"
echo ""

printf " %-3s %-14s %-10s %-10s %-12s %s\n" "No" "MODEL" "SIZE" "SPEED" "QUALITY" "BEST FOR"
printf " %-3s %-14s %-10s %-10s %-12s %s\n" "──" "─────" "────" "─────" "──────" "────────"
printf " %-3s %-14s %-10s %-10s %-12s %s\n" "1"  "llama3.1"      "~4.7 GB" "Medium"    "Excellent" "Best quality"
printf " %-3s %-14s %-10s %-10s %-12s %s\n" "2"  "gemma:2b"      "~1.4 GB" "Fast"      "Good"      "Recommended"
printf " %-3s %-14s %-10s %-10s %-12s %s\n" "3"  "phi3:mini"    "~2.3 GB" "Fast"      "Very Good" "Great balance"
printf " %-3s %-14s %-10s %-10s %-12s %s\n" "4"  "qwen2.5:1.5b"  "~1 GB"   "Very Fast" "Decent"    "Low RAM"
printf " %-3s %-14s %-10s %-10s %-12s %s\n" "5"  "tinyllama"    "~637 MB" "Ultra Fast" "Basic"     "Minimal"
echo ""

read -p "Enter the model number (1-5): " CHOICE
echo ""

case $CHOICE in
  1) MODEL="llama3.1" ;;
  2) MODEL="gemma:2b" ;;
  3) MODEL="phi3:mini" ;;
  4) MODEL="qwen2.5:1.5b" ;;
  5) MODEL="tinyllama" ;;
  *)
    echo "❌ Invalid selection. Please run setup again."
    exit 1
    ;;
esac

echo "You selected: $MODEL"
echo ""

echo "Checking for $MODEL..."
if ollama list | grep -q "$MODEL"; then
    echo "✅ $MODEL is already installed"
else
    echo "📥 Downloading $MODEL (this may take a few minutes)..."
    ollama pull "$MODEL"
fi

echo ""
echo "✔ Model ready: $MODEL"
echo ""


# Install Python dependencies
echo "██╗███╗   ██╗███████╗████████╗ █████╗ ██╗     ██╗     ██╗███╗   ██╗ ██████╗ "
echo "██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║     ██║     ██║████╗  ██║██╔════╝ "
echo "██║██╔██╗ ██║███████╗   ██║   ███████║██║     ██║     ██║██╔██╗ ██║██║  ███╗"
echo "██║██║╚██╗██║     ██║   ██║   ██╔══██║██║     ██║     ██║██║╚██╗██║██║   ██║"
echo "██║██║ ╚████║███████║   ██║   ██║  ██║███████╗███████╗██║██║ ╚████║╚██████╔╝"
echo "╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ "
echo ""
echo "██████╗ ██╗   ██╗████████╗██╗  ██╗ ██████╗ ███╗   ██╗"
echo "██╔══██╗██║   ██║╚══██╔══╝██║  ██║██╔═══██╗████╗  ██║"
echo "██████╔╝████████║   ██║   ███████║██║   ██║██╔██╗ ██║"
echo "██╔═══╝    ██║      ██║   ██╔══██║██║   ██║██║╚██╗██║"
echo "██║        ██║      ██║   ██║  ██║╚██████╔╝██║ ╚████║"
echo "╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝"
echo ""
echo "██████╗ ███████╗██████╗ ███████╗███╗   ██╗██████╗ ███████╗███╗   ██╗ ██████╗ ██╗███████╗███████╗"
echo "██╔══██╗██╔════╝██╔══██╗██╔════╝████╗  ██║██╔══██╗██╔════╝████╗  ██║██╔════╝ ██║██╔════╝██╔════╝"
echo "██║  ██║█████╗  ██████╔╝█████╗  ██╔██╗ ██║██║  ██║█████╗  ██╔██╗ ██║██║      ██║█████╗  ███████╗"
echo "██║  ██║██╔══╝  ██╔═══╝ ██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██║╚██╗██║██║      ██║██╔══╝  ╚════██║"
echo "██████╔╝███████╗██║     ███████╗██║ ╚████║██████╔╝███████╗██║ ╚████║╚██████╗ ██║███████╗███████║"
echo "╚═════╝ ╚══════╝╚═╝     ╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚══════╝╚══════╝"
echo ""

pip3 install -r requirements.txt --break-system-packages
echo ""

# Make main.py executable
chmod +x main.py
echo "███████╗███████╗████████╗██╗   ██╗██████╗ "
echo "██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔══██╗"
echo "███████╗█████╗     ██║   ██║   ██║██████╔╝"
echo "╚════██║██╔══╝     ██║   ██║   ██║██╔═══╝ "
echo "███████║███████╗   ██║   ╚██████╔╝██║     "
echo "╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝     "
echo ""
echo " ██████╗ ██████╗ ███╗   ███╗██████╗ ██╗     ███████╗████████╗███████╗██████╗ "
echo "██╔════╝██╔═══██╗████╗ ████║██╔══██╗██║     ██╔════╝╚══██╔══╝██╔════╝██╔══██╗"
echo "██║     ██║   ██║██╔████╔██║██████╔╝██║     █████╗     ██║   █████╗  ██║  ██║"
echo "██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝     ██║   ██╔══╝  ██║  ██║"
echo "╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ███████╗███████╗   ██║   ███████╗██████╔╝"
echo " ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝   ╚═╝   ╚══════╝╚═════╝ "
echo ""
echoecho "──────────────────────────────────────────────────────────"
echo "   Ready to use  •  Journal Buddy"
echo "──────────────────────────────────────────────────────────────"
echo ""
echo "  ▶ Start the app:"
echo "     python3 main.py"
echo ""
echo "  ▶ Or make it executable:"
echo "     ./main.py"
echo ""
echo "  📝 Runs in the system tray"
echo "     Double-click the tray icon to journal"
echo ""
echo "──────────────────────────────────────────────────────────────"
echo ""
