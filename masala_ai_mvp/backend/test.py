from dotenv import load_dotenv
import os
from pathlib import Path

# Ensure .env is loaded from the correct location
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# Print the environment variables to verify
print("ACCESS KEY:", os.getenv("AWS_ACCESS_KEY_ID"))
print("SECRET KEY:", os.getenv("AWS_SECRET_ACCESS_KEY"))
print("REGION:", os.getenv("AWS_REGION"))
