# Pet data handling functions
import json
import os
from config import PET_DATA_FILE

# Check if pet data file exists, create it if not
if not os.path.exists(PET_DATA_FILE):
    with open(PET_DATA_FILE, "w") as f:
        json.dump({}, f)

# Load pet data from file
def load_pet_data():
    try:
        with open(PET_DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# Save pet data to file
def save_pet_data(data):
    with open(PET_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Get pet data for a user, create new if doesn't exist, or update existing with new fields
def get_user_pets(user_id):
    data = load_pet_data()
    str_user_id = str(user_id)
    
    # Default pet template
    default_pets = {
        "cat": {
            "name": "Whiskers", 
            "happiness": 50, 
            "hunger": 50, 
            "energy": 50,
            "level": 1,
            "exp": 0,
            "last_interaction": None,
            "current_activity": "relaxing",
            "activity_until": None,
            "toys": ["yarn ball", "mouse toy"],
            "tricks": ["paw", "sit"]
        },
        "dog": {
            "name": "Buddy", 
            "happiness": 50, 
            "hunger": 50, 
            "energy": 50,
            "level": 1,
            "exp": 0,
            "last_interaction": None,
            "current_activity": "relaxing",
            "activity_until": None,
            "toys": ["tennis ball", "rope"],
            "tricks": ["sit", "roll over"]
        },
        "dragon": {
            "name": "Ember", 
            "happiness": 50, 
            "hunger": 50, 
            "energy": 50,
            "level": 1,
            "exp": 0,
            "last_interaction": None,
            "current_activity": "relaxing",
            "activity_until": None,
            "toys": ["magical orb", "treasure chest"],
            "tricks": ["flame breath", "fly"]
        },
    }
    
    # Check if the user exists in the data
    if str_user_id not in data:
        # Initialize new user with default pets
        data[str_user_id] = default_pets
        save_pet_data(data)
    else:
        # User exists, but check if pets have all the necessary fields
        need_save = False
        
        for pet_type in ["cat", "dog", "dragon"]:
            # If user doesn't have this pet type, add it
            if pet_type not in data[str_user_id]:
                data[str_user_id][pet_type] = default_pets[pet_type]
                need_save = True
            else:
                # For existing pets, ensure they have all the necessary fields
                for field, value in default_pets[pet_type].items():
                    if field not in data[str_user_id][pet_type]:
                        data[str_user_id][pet_type][field] = value
                        need_save = True
        
        # Save if any updates were made
        if need_save:
            save_pet_data(data)
    
    return data[str_user_id]