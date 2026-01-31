#!/usr/bin/env python3
"""
Test script to verify Journal Buddy components
"""

print("Testing Journal Buddy components...")
print("-" * 50)

# Test 1: Import checks
print("\n1. Testing imports...")
try:
    from pathlib import Path
    print("   ✓ pathlib.Path")
    from PyQt6.QtWidgets import QApplication
    print("   ✓ PyQt6")
    import ollama
    print("   ✓ ollama")
    from utils.config import Config
    print("   ✓ utils.config")
    from gui.settings import SettingsDialog
    print("   ✓ gui.settings")
    print("   All imports successful!")
except ImportError as e:
    print(f"   ✗ Import failed: {e}")
    exit(1)

# Test 2: Config creation
print("\n2. Testing config...")
try:
    config = Config()
    print(f"   ✓ Config created at: {config.config_file}")
    print(f"   ✓ Default model: {config.get('ollama_model')}")
except Exception as e:
    print(f"   ✗ Config failed: {e}")

# Test 3: Ollama connection
print("\n3. Testing Ollama...")
try:
    models = ollama.list()
    print(f"   ✓ Ollama is running")
    models_list = models.get('models', [])
    print(f"   ✓ Available models: {len(models_list)}")
    for model in models_list:
        model_name = model.get('name', model.get('model', 'unknown'))
        print(f"     - {model_name}")
    if len(models_list) == 0:
        print("   ⚠️  No models installed!")
        print("   → Run: ollama pull tinyllama")
except Exception as e:
    print(f"   ✗ Ollama error: {e}")
    print("   → Make sure Ollama is running: ollama serve")

# Test 4: Path validation
print("\n4. Testing Path handling...")
try:
    home = Path.home()
    print(f"   ✓ Home directory: {home}")
    test_path = Path("/tmp/test")
    print(f"   ✓ Path operations working")
except Exception as e:
    print(f"   ✗ Path failed: {e}")

print("\n" + "-" * 50)
print("All basic tests completed!")
print("\nTo run the app:")
print("  python3 main.py")
