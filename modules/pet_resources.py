# Pet resources (images, personalities, responses)

# Pet GIFs and images by type and mood
PET_IMAGES = {
    "cat": {
        "happy": [
            "https://media.giphy.com/media/BzyTuYCmvSORqs1ABM/giphy.gif",  # Happy cat purring
            "https://media.giphy.com/media/ICOgUNjpvO0PC/giphy.gif",       # Cat playing
            "https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif",       # Cat vibing
        ],
        "content": [
            "https://media.giphy.com/media/mlvseq9yvZhba/giphy.gif",       # Content cat
            "https://media.giphy.com/media/xJLNafkD7RGsE/giphy.gif",       # Cat grooming
        ],
        "unhappy": [
            "https://media.giphy.com/media/VbnUQpnihPSIgIXuZv/giphy.gif",  # Sad cat
            "https://media.giphy.com/media/3oriO0OEd9QIDdllqo/giphy.gif",  # Annoyed cat
        ],
        "hungry": [
            "https://media.giphy.com/media/8JrkAsk9CeJHi/giphy.gif",       # Hungry looking cat
            "https://media.giphy.com/media/GwpCDe8SPEeYM/giphy.gif",       # Cat asking for food
        ],
        "playing": [
            "https://media.giphy.com/media/q1MeAPDDMb43K/giphy.gif",       # Cat playing
            "https://media.giphy.com/media/aC45M5Q4D07Pq/giphy.gif",       # Cat attacking toy
        ],
        "sleeping": [
            "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",  # Sleeping cat
            "https://media.giphy.com/media/fLv2F5rMY2YWk/giphy.gif",       # Cat napping
        ],
        "eating": [
            "https://media.giphy.com/media/MLhIi4DoxeUjC/giphy.gif",       # Cat eating
            "https://media.giphy.com/media/nR4L10XlJcSeQ/giphy.gif",       # Cat munching
        ],
    },
    "dog": {
        "happy": [
            "https://media.giphy.com/media/4Zo41lhzKt6iZ8xff9/giphy.gif",  # Happy dog
            "https://media.giphy.com/media/hVYVYZZBgF50k/giphy.gif",       # Excited dog
        ],
        "content": [
            "https://media.giphy.com/media/mCRJDo24UvJMA/giphy.gif",       # Content dog
            "https://media.giphy.com/media/51Uiuy5QBZNkoF3b2Z/giphy.gif",  # Relaxed dog
        ],
        "unhappy": [
            "https://media.giphy.com/media/kHoOIOkLnHGp2/giphy.gif",       # Sad doggo
            "https://media.giphy.com/media/l0HlUH6eDIyq3ASwo/giphy.gif",   # Disappointed dog
        ],
        "hungry": [
            "https://media.giphy.com/media/eYilisUwipOEM/giphy.gif",       # Hungry dog
            "https://media.giphy.com/media/ZgqJGwh2tLj5C/giphy.gif",       # Begging dog
        ],
        "playing": [
            "https://media.giphy.com/media/3orif1K0QRfJ2QIr1m/giphy.gif",  # Dog playing with ball
            "https://media.giphy.com/media/l41m0CPz6UCnaUmxG/giphy.gif",   # Playful dog
        ],
        "sleeping": [
            "https://media.giphy.com/media/wW95fEq09hOI8/giphy.gif",       # Sleeping dog
            "https://media.giphy.com/media/ND6xkVPaj8tHO/giphy.gif",       # Dog napping
        ],
        "eating": [
            "https://media.giphy.com/media/pOZhmE42D1WrCWATLK/giphy.gif",  # Dog eating
            "https://media.giphy.com/media/19ijzMia1BaMg/giphy.gif",       # Dog munching
        ],
    },
    "dragon": {
        "happy": [
            "https://media.giphy.com/media/L4DnOdeDrBQhamvvLQ/giphy.gif",  # Happy dragon (Toothless)
            "https://media.giphy.com/media/aQYR1p8saOQla/giphy.gif",       # Flying dragon
        ],
        "content": [
            "https://media.giphy.com/media/xIJLgO6rizUJi/giphy.gif",       # Content dragon 
            "https://media.giphy.com/media/dILrAu24mU729pxPMN/giphy.gif",  # Relaxed dragon
        ],
        "unhappy": [
            "https://media.giphy.com/media/X3VrxPijowGIcIHbry/giphy.gif",  # Sad dragon
            "https://media.giphy.com/media/11JTxkrmq4bGE0/giphy.gif",      # Disappointed dragon
        ],
        "hungry": [
            "https://media.giphy.com/media/NipFetnQOuKhW/giphy.gif",       # Hungry dragon
            "https://media.giphy.com/media/WKJpCXfvBHyla/giphy.gif",       # Dragon roaring for food
        ],
        "playing": [
            "https://media.giphy.com/media/Z9WQLSrsQKH3uBbiXq/giphy.gif",  # Dragon playing
            "https://media.giphy.com/media/l3978y5HqiEtqupiM/giphy.gif",   # Dragon flying playfully
        ],
        "sleeping": [
            "https://media.giphy.com/media/iDJQRjTCenF7A4BRyU/giphy.gif",  # Sleeping dragon
            "https://media.giphy.com/media/W0VuY0dTxH9L6vLUJ4/giphy.gif",  # Dragon napping
        ],
        "eating": [
            "https://media.giphy.com/media/3o7btQsLqXMJAPu6Na/giphy.gif",  # Dragon eating
            "https://media.giphy.com/media/b53xiN2B9VbKE/giphy.gif",       # Dragon roasting food
        ],
    }
}

# Pet personalities by type
PET_PERSONALITIES = {
    "cat": {
        "pet_phrases": [
            "{name} purrs contentedly and nudges your hand for more pets! 🐾",
            "{name} stretches and rolls over, exposing their fluffy belly! 🐱",
            "{name} starts kneading on your lap while purring loudly! 😺",
            "{name}'s eyes narrow with contentment as you scratch behind their ears! 😻",
            "{name} nuzzles against your hand and makes little chirping sounds! 🐈",
        ],
        "feed_phrases": [
            "{name} sniffs the food cautiously, then devours it enthusiastically! 🍣",
            "{name} does a little dance of joy before eating the delicious treats! 🍤",
            "{name} meows thankfully and gobbles up the food! 🥣",
            "{name} purrs loudly while munching on the tasty meal! 😋",
            "{name} eats delicately, then licks their paws clean! 👅",
        ],
        "play_phrases": [
            "{name} pounces on the toy with lightning speed! 🎯",
            "{name} chases the laser pointer dot with intense focus! 🔴",
            "{name} bats at the string toy and does a backflip! 🧶",
            "{name} crouches low, wiggles their butt, and then leaps at the toy! 🐆",
            "{name} zooms around the room in a sudden burst of energy! 💨",
        ],
    },
    "dog": {
        "pet_phrases": [
            "{name} wags their tail so hard their whole body wiggles! 🐕",
            "{name} rolls over for belly rubs, tongue lolling happily! 🐶",
            "{name} leans against your leg and looks up adoringly! ❤",
            "{name} gives your hand a gentle lick of appreciation! 👅",
            "{name}'s tail thumps rhythmically against the floor in happiness! 💓",
        ],
        "feed_phrases": [
            "{name} woofs excitedly and gulps down the food in seconds! 🍖",
            "{name} does a little spin before diving into the meal! 🍗",
            "{name} drools a little as you prepare their food, then munches happily! 🤤",
            "{name} crunches loudly and enthusiastically on their delicious dinner! 😋",
            "{name} polishes off their meal and looks hopeful for seconds! 👀",
        ],
        "play_phrases": [
            "{name} catches the frisbee mid-air with an impressive leap! 🥏",
            "{name} brings back the ball and drops it at your feet, ready for more! ⚾",
            "{name} races around the yard with pure joy! 🏃",
            "{name} tugs on the rope toy with surprising strength! 💪",
            "{name} does a perfect roll-over trick for a treat! 🍪",
        ],
    },
    "dragon": {
        "pet_phrases": [
            "{name} puffs small happy smoke rings from their nostrils! 💨",
            "{name} nuzzles against you, their scales warm and smooth! 🔥",
            "{name} stretches their wings contentedly and makes a rumbling purr! 🐉",
            "{name} gently rests their head on your shoulder, eyes half-closed in bliss! 😌",
            "{name} lets out a small flame of joy that sparkles with different colors! ✨",
        ],
        "feed_phrases": [
            "{name} breathes a small flame to perfectly cook the meal before eating! 🔥",
            "{name} devours the whole feast with gusto, then licks their chops! 🍖",
            "{name} roasts the food with a precise flame, then eats with refined manners! 👑",
            "{name} snaps up the meal in one bite, then looks satisfied! 😋",
            "{name} shares a tiny portion of their food with you (after carefully cooking it)! 🍽",
        ],
        "play_phrases": [
            "{name} soars through the sky, performing incredible aerial acrobatics! ✈",
            "{name} playfully shoots small fireballs for you to dodge! 🔥",
            "{name} plays a game of hide-and-seek, using their wings to hide! 🌳",
            "{name} carefully carries you on their back for a short flight! 🏞",
            "{name} challenges you to a race and pretends to let you win! 🏁",
        ],
    },
}

# Exploration messages by pet type
EXPLORATION_MESSAGES = {
    "cat": [
        "ventures into the neighbor's garden, stalking bugs and climbing trees!",
        "investigates a mysterious sound in the attic, finding a forgotten toy!",
        "sneaks into the kitchen and discovers where the treats are hidden!",
        "prowls through the basement, hunting imaginary mice and exploring dark corners!"
    ],
    "dog": [
        "runs through the park, making friends with every person and dog they meet!",
        "follows an interesting scent trail that leads to a friendly squirrel!",
        "digs in the backyard and unearths a long-lost tennis ball!",
        "explores the neighborhood, wagging their tail at everyone they see!"
    ],
    "dragon": [
        "soars above the clouds, discovering a flock of friendly birds!",
        "ventures into a cave and finds a small collection of shiny treasures!",
        "explores a mountain peak, enjoying the view from the highest point!",
        "investigates a mysterious forest, startling a group of deer with a tiny flame!"
    ]
}

# Get a random response phrase for pet actions
def get_pet_response(pet_type, action, name):
    if action in PET_PERSONALITIES[pet_type]:
        import random
        return random.choice(PET_PERSONALITIES[pet_type][action]).format(name=name)
    return f"{name} seems to enjoy that!"

# Get appropriate GIF for pet based on state
def get_pet_gif(pet_type, pet):
    from modules.pet_activities import get_pet_mood
    import random
    
    mood, _ = get_pet_mood(pet)
    activity = pet.get("current_activity", "relaxing")
    
    # Map activities to mood categories for GIF selection
    activity_mood_map = {
        "sleeping": "sleeping",
        "playing": "playing",
        "eating": "eating",
        "training": "playing",
        "exploring": "playing",
        "relaxing": mood,
    }
    
    gif_category = activity_mood_map.get(activity, mood)
    
    # If we don't have a specific category, fall back to mood
    if gif_category not in PET_IMAGES[pet_type]:
        gif_category = mood
        
    # If we still don't have it, use "content" as fallback
    if gif_category not in PET_IMAGES[pet_type]:
        gif_category = "content"
    
    return random.choice(PET_IMAGES[pet_type][gif_category])