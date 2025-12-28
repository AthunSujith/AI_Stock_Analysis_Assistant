from pathlib import Path

ROOT = Path(".")

# Corrected list with quotes and standardized naming
STRUCTURE = [
    "app/api",        # FastAPI/Flask endpoints
    "app/models",     # LSTM architecture definitions
    "app/core",       # Logic for training and inference
    "app/data",       # Data loading/preprocessing scripts
    "app/pipelines",  # Training/Deployment pipelines
    "app/config",     # Hyperparameters and .env settings
    "data_store/raw", # Unprocessed data
    "data_store/processed", # Scaled/Vectorized data
    "services"        # External service integrations
]

def main():
    print("🚀 Initializing poetry_rnn project structure...\n")

    for folder in STRUCTURE:
        path = ROOT / folder
        path.mkdir(parents=True, exist_ok=True)
        # Creating an __init__.py makes these folders actual Python packages
        (path / "__init__.py").touch(exist_ok=True)
        print(f"✅ Created: {path}")

    # Essential boilerplate files
    files = ["README.md", "requirements.txt", "main.py", ".env"]
    for file in files:
        (ROOT / file).touch(exist_ok=True)
        print(f"📝 Created file: {file}")

    print("\n✨ Project structure successfully created.")

if __name__ == "__main__":
    main()