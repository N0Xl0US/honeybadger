import discord
from discord.ext import commands
import os
from config import TOKEN
from config import F1_YEAR
from keep_alive import keep_alive
import fastf1
from config import F1_CHANNEL_ID

fastf1.Cache.enable_cache('fastf1_data')

intents = discord.Intents.default()
intents.message_content = True

class HoneybadgerBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        # Load command extensions
        for filename in os.listdir("./commands"):
            if filename.endswith(".py") and filename != "__init__.py":
                try:
                    await self.load_extension(f"commands.{filename[:-3]}")
                    print(f"✅ Loaded: {filename}")
                except Exception as e:
                    print(f"❌ Failed to load {filename}: {e}")
        # Schedule loading cogs from tasks
        self.loop.create_task(load_cogs(self))

# Bot Setup
bot = HoneybadgerBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔧 Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

def keep_alive_and_run():
    keep_alive()
    bot.run(TOKEN)

async def load_cogs(bot):
    for filename in os.listdir("./tasks"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"tasks.{filename[:-3]}")

if __name__ == "__main__":
    keep_alive_and_run()

