import discord
from discord.ext import commands
import asyncio
import os
from modules.pet_data import load_pet_data, get_user_pets
from modules.pet_activities import (
    PetInteractionView, 
    PetSelectionView, 
    show_pet, 
    decay_stats_over_time,
    start_pet_activity,
    update_pet_stats
)
from config import TOKEN, COMMAND_PREFIX

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Initialize bot
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    print(f"Bot is in {len(bot.guilds)} servers")
    
    # Set custom status
    await bot.change_presence(activity=discord.Game(name="with virtual pets | !pets"))
    
    # Start the background task for stat decay
    bot.loop.create_task(decay_stats_over_time(bot))

@bot.command(name="pets")
async def pets_command(ctx):
    """Shows your virtual pet collection"""
    user_pets = get_user_pets(ctx.author.id)
    
    # Create a rich embed with pet summary
    embed = discord.Embed(
        title=f"{ctx.author.name}'s Virtual Pets",
        description="Choose a pet to interact with:",
        color=discord.Color.purple()
    )
    
    # Add a cute header image
    embed.set_thumbnail(url="https://media.giphy.com/media/Y4pAQv58ETJgRwoLxj/giphy.gif")
    
    # Add fields for each pet with a brief status
    for pet_type, pet in user_pets.items():
        mood, emoji = get_pet_mood(pet)
        
        # Get pet activity status
        activity = pet.get("current_activity", "relaxing")
        activity_emoji = {
            "relaxing": "💤",
            "playing": "🎮",
            "eating": "🍽",
            "sleeping": "😴",
            "training": "🎓",
            "exploring": "🧭"
        }.get(activity, "🏠")
        
        # Get level or default to 1
        level = pet.get("level", 1)
        
        embed.add_field(
            name=f"{pet['name']} ({pet_type.capitalize()})",
            value=f"Level: {level} | Mood: {mood} {emoji}\nActivity: {activity} {activity_emoji}",
            inline=True
        )
    
    # Add footer with tip
    embed.set_footer(text="Click a button below to select a pet to interact with!")
    
    # Send the embed with selection buttons
    view = PetSelectionView(ctx.author.id)
    await ctx.send(embed=embed, view=view)

@bot.command(name="pet")
async def pet_command(ctx, pet_type: str = None):
    """Interact with a specific pet"""
    if not pet_type:
        await ctx.send("Please specify which pet you want to interact with: !pet cat, !pet dog, or !pet dragon")
        return
    
    pet_type = pet_type.lower()
    if pet_type not in ["cat", "dog", "dragon"]:
        await ctx.send("I don't recognize that pet type! Choose from: cat, dog, or dragon")
        return
    
    user_pets = get_user_pets(ctx.author.id)
    if pet_type not in user_pets:
        await ctx.send(f"You don't have a {pet_type} yet! Use !pets to see your available pets.")
        return
    
    await show_pet(ctx, pet_type, ctx.author.id)

@bot.command(name="rename")
async def rename_pet(ctx, pet_type: str = None, *, new_name: str = None):
    """Rename one of your pets"""
    if not pet_type or not new_name:
        await ctx.send("Usage: !rename <pet_type> <new_name> (pet types: cat, dog, dragon)")
        return
    
    pet_type = pet_type.lower()
    if pet_type not in ["cat", "dog", "dragon"]:
        await ctx.send("Invalid pet type! Choose from: cat, dog, dragon")
        return
    
    if len(new_name) > 20:
        await ctx.send("Pet name too long! Please keep it under 20 characters.")
        return
    
    data = load_pet_data()
    str_user_id = str(ctx.author.id)
    
    if str_user_id in data and pet_type in data[str_user_id]:
        old_name = data[str_user_id][pet_type]["name"]
        data[str_user_id][pet_type]["name"] = new_name
        save_pet_data(data)
        
        # Create a cute embed for the renaming
        embed = discord.Embed(
            title="Pet Renamed!",
            description=f"Your {pet_type} has a new name!",
            color=discord.Color.green()
        )
        
        embed.add_field(name="Old Name", value=old_name, inline=True)
        embed.add_field(name="New Name", value=new_name, inline=True)
        embed.set_thumbnail(url=get_pet_gif(pet_type, data[str_user_id][pet_type]))
        
        await ctx.send(embed=embed)
    else:
        await ctx.send("You don't have that pet yet! Use !pets to get started.")

@bot.command(name="explore")
async def explore_command(ctx, pet_type: str = None):
    """Send your pet on an adventure"""
    if not pet_type:
        await ctx.send("Please specify which pet to send exploring: !explore cat, !explore dog, or !explore dragon")
        return
    
    pet_type = pet_type.lower()
    if pet_type not in ["cat", "dog", "dragon"]:
        await ctx.send("Invalid pet type! Choose from: cat, dog, dragon")
        return
    
    pet_data = get_user_pets(ctx.author.id).get(pet_type)
    if not pet_data:
        await ctx.send(f"You don't have a {pet_type}!")
        return
    
    # Check if pet is already busy
    if pet_data.get("current_activity") != "relaxing" and pet_data.get("activity_until"):
        try:
            end_time = datetime.fromisoformat(pet_data["activity_until"])
            now = datetime.now()
            
            if end_time > now:
                minutes_left = int((end_time - now).total_seconds() / 60)
                await ctx.send(f"{pet_data['name']} is currently {pet_data['current_activity']} for {minutes_left} more minutes!")
                return
        except:
            pass
    
    # Check if pet has enough energy
    if pet_data["energy"] < 30:
        await ctx.send(f"{pet_data['name']} is too tired to explore! Try letting them sleep first.")
        return
    
    # Start exploring activity (30 minutes)
    pet_data, _ = update_pet_stats(ctx.author.id, pet_type, {"happiness": 10, "hunger": -10, "energy": -20}, exp_gain=15)
    pet_data = start_pet_activity(ctx.author.id, pet_type, "exploring", 30)
    
    # Different exploration messages by pet type
    exploration_messages = {
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
    
    exploration = random.choice(exploration_messages.get(pet_type, ["goes on an exciting adventure!"]))
    
    embed = discord.Embed(
        title=f"{pet_data['name']} Goes Exploring!",
        description=f"{pet_data['name']} {exploration} 🧭",
        color=discord.Color.gold()
    )
    
    embed.set_image(url=get_pet_gif(pet_type, pet_data))
    embed.add_field(name="Adventure Stats", value=f"XP Gained: +15\nEnergy: -{20}\nHunger: -{10}\nHappiness: +{10}")
    embed.set_footer(text=f"{pet_data['name']} will be exploring for 30 minutes. They'll be back with stories to tell!")
    
    await ctx.send(embed=embed)

@bot.command(name="pethelp")
async def pet_help(ctx):
    """Show help information for the virtual pet bot"""
    embed = discord.Embed(
        title="🐾 Virtual Pet Bot - Commands 🐾",
        description="Here are all the available commands for interacting with your virtual pets:",
        color=discord.Color.blue()
    )
    
    # Add a cute header image
    embed.set_thumbnail(url="https://media.giphy.com/media/Y4pAQv58ETJgRwoLxj/giphy.gif")
    
    # Basic commands
    basic_commands = [
        "!pets - View all your pets and select one to interact with",
        "!pet <type> - Interact directly with a specific pet (cat/dog/dragon)",
        "!rename <type> <name> - Give your pet a new name",
        "!explore <type> - Send your pet on an adventure"
    ]
    
    embed.add_field(
        name="📋 Basic Commands",
        value="\n".join(basic_commands),
        inline=False
    )
    
    # Pet interactions
    pet_interactions = [
        "🖐 *Pet* - Give your pet some affection (+happiness)",
        "🍖 *Feed* - Give your pet some food (+hunger)",
        "🎮 *Play* - Play with your pet (+happiness, -energy)",
        "😴 *Sleep* - Let your pet rest (+energy)",
        "🎓 *Train* - Teach your pet new tricks (+XP, -energy)",
        "📊 *Stats* - View detailed information about your pet"
    ]
    
    embed.add_field(
        name="🤲 Pet Interactions",
        value="\n".join(pet_interactions),
        inline=False
    )
    
    # How pets work
    pet_info = [
        "*Stats* - Pets have happiness, hunger, and energy stats that change over time",
        "*Leveling* - Pets gain XP from interactions and can level up",
        "*Activities* - Pets can be busy with activities like sleeping or exploring",
        "*Mood* - A pet's mood is based on their stats"
    ]
    
    embed.add_field(
        name="ℹ How Pets Work",
        value="\n".join(pet_info),
        inline=False
    )
    
    embed.set_footer(text="Remember to interact with your pets regularly to keep them happy!")
    
    await ctx.send(embed=embed)

# Import missing functions from modules
from modules.pet_activities import get_pet_mood, get_pet_gif
from modules.pet_data import save_pet_data
from datetime import datetime

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)