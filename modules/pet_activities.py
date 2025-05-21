# Pet activities and interaction functions
import discord
import asyncio
import random
from datetime import datetime, timedelta
from modules.pet_data import load_pet_data, save_pet_data, get_user_pets
from modules.pet_resources import get_pet_gif, get_pet_response, EXPLORATION_MESSAGES
from config import PET_ACTIVITIES

# Get pet mood based on stats
def get_pet_mood(pet):
    happiness = pet.get("happiness", 50)
    hunger = pet.get("hunger", 50)
    energy = pet.get("energy", 50)
    
    # Calculate weighted mood score
    mood_score = (happiness * 0.4) + (hunger * 0.4) + (energy * 0.2)
    
    if mood_score < 20:
        return "miserable", "😭"
    elif mood_score < 40:
        return "unhappy", "😢"
    elif mood_score < 60:
        return "content", "😐"
    elif mood_score < 80:
        return "happy", "😊"
    else:
        return "ecstatic", "🤩"

# Update pet stats and handle experience/leveling
def update_pet_stats(user_id, pet_type, stat_updates, exp_gain=0):
    data = load_pet_data()
    str_user_id = str(user_id)
    now = datetime.now().isoformat()
    level_up = False
    
    if str_user_id in data and pet_type in data[str_user_id]:
        pet = data[str_user_id][pet_type]
        
        # Update stats
        for stat, value in stat_updates.items():
            if stat in pet:
                if isinstance(pet[stat], (int, float)):
                    pet[stat] = max(0, min(100, pet[stat] + value))
            else:
                # If the stat doesn't exist, add it with default value + update
                if stat == "happiness" or stat == "hunger" or stat == "energy":
                    pet[stat] = max(0, min(100, 50 + value))  # Default is 50
        
        # Ensure energy exists
        if "energy" not in pet:
            pet["energy"] = 50
            
        # Ensure level and exp exist
        if "level" not in pet:
            pet["level"] = 1
        if "exp" not in pet:
            pet["exp"] = 0
        
        # Update experience and check for level up
        if exp_gain > 0:
            pet["exp"] += exp_gain
            
            # Simple leveling formula: level * 100 exp needed for next level
            while pet["exp"] >= pet["level"] * 100:
                pet["exp"] -= pet["level"] * 100
                pet["level"] += 1
                level_up = True
            
            # Bonus stats on level up
            if level_up:
                pet["happiness"] = min(100, pet["happiness"] + 10)
                pet["energy"] = min(100, pet["energy"] + 10)
        
        # Update last interaction time
        pet["last_interaction"] = now
        save_pet_data(data)
        return data[str_user_id][pet_type], level_up if exp_gain > 0 else False
    
    return None, False

# Start pet on an activity
def start_pet_activity(user_id, pet_type, activity, duration_minutes=30):
    data = load_pet_data()
    str_user_id = str(user_id)
    
    if str_user_id in data and pet_type in data[str_user_id]:
        pet = data[str_user_id][pet_type]
        
        # Set pet activity
        pet["current_activity"] = activity
        
        # Set end time for activity
        end_time = datetime.now() + timedelta(minutes=duration_minutes)
        pet["activity_until"] = end_time.isoformat()
        
        # Apply immediate effects based on activity
        if activity == "sleeping":
            pet["energy"] = min(100, pet["energy"] + 20)
        elif activity == "playing":
            pet["happiness"] = min(100, pet["happiness"] + 10)
            pet["energy"] = max(0, pet["energy"] - 10)
        elif activity == "eating":
            pet["hunger"] = min(100, pet["hunger"] + 20)
        elif activity == "training":
            pet["exp"] = pet["exp"] + 10
            pet["energy"] = max(0, pet["energy"] - 15)
        elif activity == "exploring":
            pet["happiness"] = min(100, pet["happiness"] + 5)
            pet["hunger"] = max(0, pet["hunger"] - 5)
            pet["energy"] = max(0, pet["energy"] - 10)
        
        save_pet_data(data)
        return pet
    
    return None

# Time decay of pet stats
async def decay_stats_over_time(bot):
    await bot.wait_until_ready()
    while not bot.is_closed():
        data = load_pet_data()
        current_time = datetime.now()
        
        for user_id, pets in data.items():
            for pet_type, pet in pets.items():
                # Check activity status
                if pet.get("activity_until"):
                    try:
                        activity_end = datetime.fromisoformat(pet["activity_until"])
                        if current_time > activity_end:
                            # Activity finished
                            pet["current_activity"] = "relaxing"
                            pet["activity_until"] = None
                    except (ValueError, TypeError):
                        # Invalid datetime format, reset it
                        pet["current_activity"] = "relaxing"
                        pet["activity_until"] = None
                
                # Decay stats based on time
                last_interaction = pet.get("last_interaction")
                if last_interaction:
                    try:
                        last_time = datetime.fromisoformat(last_interaction)
                        hours_passed = (current_time - last_time).total_seconds() / 3600
                        
                        # Decay stats based on time passed
                        if hours_passed > 0.5:  # 30 minutes
                            decay_amount = min(int(hours_passed * 2), 10)  # Cap at 10 points per check
                            pet["hunger"] = max(0, pet["hunger"] - decay_amount)
                            pet["happiness"] = max(0, pet["happiness"] - decay_amount)
                            pet["energy"] = max(0, pet.get("energy", 50) - decay_amount)
                    except (ValueError, TypeError):
                        # Invalid datetime format, reset it
                        pet["last_interaction"] = current_time.isoformat()
        
        save_pet_data(data)
        await asyncio.sleep(1800)  # Check every 30 minutes

# Pet Interaction View with buttons
class PetInteractionView(discord.ui.View):
    def __init__(self, user_id, pet_type):
        super().__init__(timeout=120)  # 2 minute timeout
        self.user_id = user_id
        self.pet_type = pet_type
    
    # Only allow the pet owner to interact with buttons
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your pet! Use !pet <type> to summon your own pet.", ephemeral=True)
            return False
        return True
    
    @discord.ui.button(label="Pet", style=discord.ButtonStyle.primary, emoji="✋", custom_id="pet")
    async def pet_action(self, interaction: discord.Interaction, button: discord.ui.Button):
        pet_data, _ = update_pet_stats(self.user_id, self.pet_type, {"happiness": 10}, exp_gain=2)
        mood, emoji = get_pet_mood(pet_data)
        
        response_text = get_pet_response(self.pet_type, "pet_phrases", pet_data["name"])
        
        # Create a new embed for the response
        embed = discord.Embed(
            title=f"{pet_data['name']} enjoys the attention!",
            description=response_text,
            color=discord.Color.blue()
        )
        
        embed.set_image(url=get_pet_gif(self.pet_type, pet_data))
        embed.add_field(name="Status", value=f"Mood: {mood} {emoji}\nHappiness: {pet_data['happiness']}/100\nHunger: {pet_data['hunger']}/100\nEnergy: {pet_data['energy']}/100")
        
        await interaction.response.send_message(embed=embed, ephemeral=False)
    
    @discord.ui.button(label="Feed", style=discord.ButtonStyle.success, emoji="🍖", custom_id="feed")
    async def feed_action(self, interaction: discord.Interaction, button: discord.ui.Button):
        pet_data, _ = update_pet_stats(self.user_id, self.pet_type, {"hunger": 15, "happiness": 5}, exp_gain=2)
        mood, emoji = get_pet_mood(pet_data)
        
        # Start eating activity
        pet_data = start_pet_activity(self.user_id, self.pet_type, "eating", 10)
        
        response_text = get_pet_response(self.pet_type, "feed_phrases", pet_data["name"])
        
        embed = discord.Embed(
            title=f"{pet_data['name']} enjoys their meal!",
            description=response_text,
            color=discord.Color.green()
        )
        
        embed.set_image(url=get_pet_gif(self.pet_type, pet_data))
        embed.add_field(name="Status", value=f"Mood: {mood} {emoji}\nHappiness: {pet_data['happiness']}/100\nHunger: {pet_data['hunger']}/100\nEnergy: {pet_data['energy']}/100")
        embed.set_footer(text=f"{pet_data['name']} will be eating for the next 10 minutes")
        
        await interaction.response.send_message(embed=embed, ephemeral=False)
    
    @discord.ui.button(label="Play", style=discord.ButtonStyle.danger, emoji="🎮", custom_id="play")
    async def play_action(self, interaction: discord.Interaction, button: discord.ui.Button):
        pet_data, _ = update_pet_stats(self.user_id, self.pet_type, {"happiness": 15, "hunger": -5, "energy": -10}, exp_gain=5)
        mood, emoji = get_pet_mood(pet_data)
        
        # Start playing activity
        pet_data = start_pet_activity(self.user_id, self.pet_type, "playing", 15)
        
        response_text = get_pet_response(self.pet_type, "play_phrases", pet_data["name"])
        
        embed = discord.Embed(
            title=f"{pet_data['name']} is having a blast playing!",
            description=response_text,
            color=discord.Color.red()
        )
        
        embed.set_image(url=get_pet_gif(self.pet_type, pet_data))
        embed.add_field(name="Status", value=f"Mood: {mood} {emoji}\nHappiness: {pet_data['happiness']}/100\nHunger: {pet_data['hunger']}/100\nEnergy: {pet_data['energy']}/100")
        embed.add_field(name="Toys", value=", ".join(pet_data.get("toys", ["basic toy"])))
        embed.set_footer(text=f"{pet_data['name']} will be playing for the next 15 minutes")
        
        await interaction.response.send_message(embed=embed, ephemeral=False)
    
    @discord.ui.button(label="Sleep", style=discord.ButtonStyle.secondary, emoji="😴", custom_id="sleep")
    async def sleep_action(self, interaction: discord.Interaction, button: discord.ui.Button):
        pet_data, _ = update_pet_stats(self.user_id, self.pet_type, {"energy": 20}, exp_gain=1)
        mood, emoji = get_pet_mood(pet_data)
        
        # Start sleeping activity
        pet_data = start_pet_activity(self.user_id, self.pet_type, "sleeping", 20)
        
        embed = discord.Embed(
            title=f"{pet_data['name']} is taking a nap",
            description=f"{pet_data['name']} curls up and falls asleep. So peaceful... 💤",
            color=discord.Color.light_gray()
        )
        
        embed.set_image(url=get_pet_gif(self.pet_type, pet_data))
        embed.add_field(name="Status", value=f"Mood: {mood} {emoji}\nHappiness: {pet_data['happiness']}/100\nHunger: {pet_data['hunger']}/100\nEnergy: {pet_data['energy']}/100")
        embed.set_image(url=get_pet_gif(self.pet_type, pet_data))
        embed.add_field(name="Status", value=f"Mood: {mood} {emoji}\nHappiness: {pet_data['happiness']}/100\nHunger: {pet_data['hunger']}/100\nEnergy: {pet_data['energy']}/100")
        embed.set_footer(text=f"{pet_data['name']} will be sleeping for the next 20 minutes")
        
        await interaction.response.send_message(embed=embed, ephemeral=False)
    
    @discord.ui.button(label="Stats", style=discord.ButtonStyle.secondary, emoji="📊", custom_id="stats")
    async def stats_action(self, interaction: discord.Interaction, button: discord.ui.Button):
        pet_data = get_user_pets(self.user_id)[self.pet_type]
        mood, emoji = get_pet_mood(pet_data)
        
        embed = discord.Embed(
            title=f"{pet_data['name']}'s Stats",
            description=f"Here's how your {self.pet_type} is doing:",
            color=discord.Color.blue()
        )
        
        embed.set_thumbnail(url=get_pet_gif(self.pet_type, pet_data))
        
        # Basic stats
        embed.add_field(name="Basic Stats", value=f"Level: {pet_data['level']}\nXP: {pet_data['exp']}/{pet_data['level']*100}\nMood: {mood} {emoji}", inline=False)
        
        # Care stats
        embed.add_field(name="Care Stats", value=f"Happiness: {pet_data['happiness']}/100\nHunger: {pet_data['hunger']}/100\nEnergy: {pet_data['energy']}/100", inline=False)
        
        # Tricks and toys
        embed.add_field(name="Tricks Known", value=", ".join(pet_data.get("tricks", ["None"])), inline=True)
        embed.add_field(name="Favorite Toys", value=", ".join(pet_data.get("toys", ["None"])), inline=True)
        
        # Activity
        current_activity = pet_data.get("current_activity", "relaxing")
        activity_until = pet_data.get("activity_until")
        
        if activity_until and current_activity != "relaxing":
            try:
                end_time = datetime.fromisoformat(activity_until)
                now = datetime.now()
                
                if end_time > now:
                    minutes_left = int((end_time - now).total_seconds() / 60)
                    embed.add_field(name="Current Activity", value=f"Currently {current_activity} for {minutes_left} more minutes", inline=False)
                else:
                    embed.add_field(name="Current Activity", value=f"Relaxing", inline=False)
            except:
                embed.add_field(name="Current Activity", value=f"Relaxing", inline=False)
        else:
            embed.add_field(name="Current Activity", value=f"Relaxing", inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Train", style=discord.ButtonStyle.primary, emoji="🎓", custom_id="train")
    async def train_action(self, interaction: discord.Interaction, button: discord.ui.Button):
        pet_data, _ = update_pet_stats(self.user_id, self.pet_type, {"happiness": 5, "energy": -15}, exp_gain=10)
        mood, emoji = get_pet_mood(pet_data)
        
        # Start training activity
        pet_data = start_pet_activity(self.user_id, self.pet_type, "training", 15)
        
        # Training messages by pet type
        training_messages = {
            "cat": [
                "sits perfectly still for a treat!",
                "learns to high-five with their paw!",
                "figures out how to open a door by jumping on the handle!",
                "jumps through a tiny hoop with perfect form!"
            ],
            "dog": [
                "masters the 'stay' command even with distractions!",
                "learns to fetch specific items by name!",
                "practices an impressive rollover trick!",
                "balances a treat on their nose until given permission to eat it!"
            ],
            "dragon": [
                "practices controlling the size of their flame bursts!",
                "learns to hover steadily in place!",
                "masters a perfectly executed aerial roll!",
                "trains to sort colored objects with their tail!"
            ]
        }
        
        training_result = random.choice(training_messages.get(self.pet_type, ["learns a new trick!"]))
        
        embed = discord.Embed(
            title=f"Training {pet_data['name']}",
            description=f"{pet_data['name']} {training_result} 🎓",
            color=discord.Color.purple()
        )
        
        embed.set_image(url=get_pet_gif(self.pet_type, pet_data))
        embed.add_field(name="Status", value=f"Level: {pet_data.get('level', 1)} | XP: {pet_data.get('exp', 0)}/{pet_data.get('level', 1)*100}\nMood: {mood} {emoji}\nHappiness: {pet_data.get('happiness', 50)}/100\nEnergy: {pet_data.get('energy', 50)}/100")
        embed.set_footer(text=f"{pet_data['name']} will be training for the next 15 minutes")
        
        await interaction.response.send_message(embed=embed, ephemeral=False)

# Pet selection view for main hub
class PetSelectionView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=60)
        self.user_id = user_id
    
    # Only allow the pet owner to interact with buttons
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("These aren't your pets! Use !pets to summon your own pets.", ephemeral=True)
            return False
        return True
    
    @discord.ui.button(label="Cat", style=discord.ButtonStyle.primary, emoji="🐱", custom_id="select_cat")
    async def select_cat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await show_pet(interaction, "cat", self.user_id)
    
    @discord.ui.button(label="Dog", style=discord.ButtonStyle.success, emoji="🐶", custom_id="select_dog")
    async def select_dog(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await show_pet(interaction, "dog", self.user_id)
    
    @discord.ui.button(label="Dragon", style=discord.ButtonStyle.danger, emoji="🐉", custom_id="select_dragon")
    async def select_dragon(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await show_pet(interaction, "dragon", self.user_id)

# Displays a specific pet with interactive buttons
async def show_pet(interaction, pet_type, user_id):
    pet_data = get_user_pets(user_id)[pet_type]
    mood, emoji = get_pet_mood(pet_data)
    
    # Get the appropriate pet response based on mood and activity
    if pet_data.get("current_activity") == "sleeping":
        response = f"{pet_data['name']} is sleeping peacefully... 💤"
    elif pet_data.get("current_activity") == "playing":
        response = f"{pet_data['name']} is having a great time playing! 🎮"
    elif pet_data.get("current_activity") == "eating":
        response = f"{pet_data['name']} is enjoying a delicious meal! 🍽"
    elif pet_data.get("current_activity") == "training":
        response = f"{pet_data['name']} is focused on learning new tricks! 🎓"
    elif pet_data.get("current_activity") == "exploring":
        response = f"{pet_data['name']} is on an adventure! 🧭"
    elif mood == "ecstatic":
        response = f"{pet_data['name']} jumps with excitement when they see you! 🤩"
    elif mood == "happy":
        response = f"{pet_data['name']} greets you cheerfully! 😊"
    elif mood == "content":
        response = f"{pet_data['name']} looks up at you calmly. 😐"
    elif mood == "unhappy":
        response = f"{pet_data['name']} seems a bit sad. Maybe they need attention? 😢"
    else:  # miserable
        response = f"{pet_data['name']} looks extremely unhappy. They need immediate care! 😭"
    
    embed = discord.Embed(
        title=f"{pet_data['name']} the {pet_type.capitalize()}",
        description=response,
        color=discord.Color.random()
    )
    
    # Add pet image based on mood and activity
    embed.set_image(url=get_pet_gif(pet_type, pet_data))
    
    # Add pet stats
    embed.add_field(
        name="Status",
        value=f"Level: {pet_data.get('level', 1)} | XP: {pet_data.get('exp', 0)}/{pet_data.get('level', 1)*100}\nMood: {mood} {emoji}",
        inline=False
    )
    
    embed.add_field(
        name="Care Stats",
        value=f"Happiness: {pet_data.get('happiness', 50)}/100\nHunger: {pet_data.get('hunger', 50)}/100\nEnergy: {pet_data.get('energy', 50)}/100",
        inline=False
    )
    
    # Show current activity
    current_activity = pet_data.get("current_activity", "relaxing")
    activity_until = pet_data.get("activity_until")
    
    if activity_until and current_activity != "relaxing":
        try:
            end_time = datetime.fromisoformat(activity_until)
            now = datetime.now()
            
            if end_time > now:
                minutes_left = int((end_time - now).total_seconds() / 60)
                embed.add_field(name="Current Activity", value=f"Currently {current_activity} for {minutes_left} more minutes", inline=False)
            else:
                embed.add_field(name="Current Activity", value=f"Relaxing", inline=False)
        except:
            embed.add_field(name="Current Activity", value=f"Relaxing", inline=False)
    else:
        embed.add_field(name="Current Activity", value=f"Relaxing", inline=False)
    
    # Create interaction buttons for this specific pet
    view = PetInteractionView(user_id, pet_type)
    
    if interaction.response.is_done():
        await interaction.followup.send(embed=embed, view=view)
    else:
        await interaction.response.send_message(embed=embed, view=view)