import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

# Discord bot token
TOKEN = os.getenv("DISCORD_TOKEN")

# Command prefix
COMMAND_PREFIX = "!"

# Data storage file
PET_DATA_FILE = "pet_data.json"

# Pet activities
PET_ACTIVITIES = ["sleeping", "playing", "eating", "exploring", "relaxing", "training"]
