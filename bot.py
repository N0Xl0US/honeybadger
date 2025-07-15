import discord
from discord.ext import commands
import os
from config import TOKEN
from keep_alive import keep_alive

# Intents
intents = discord.Intents.default()
intents.message_content = False 
# Bot Setup
bot = commands.Bot(command_prefix="!", intents=intents)

# Load Slash Commands from files
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔧 Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

# Load command files
for filename in os.listdir("./commands"):
    if filename.endswith(".py"):
        try:
            bot.load_extension(f"commands.{filename[:-3]}")
            print(f"✅ Loaded: {filename}")
        except Exception as e:
            print(f"❌ Failed to load {filename}: {e}")

        await load_cogs()

async def load_cogs():
    for filename in os.listdir("./tasks"):
        if filename.endswith(".py"):
            await bot.load_extension(f"tasks.{filename[:-3]}")

bot.loop.create_task(load_cogs())
keep_alive()
bot.run(TOKEN)

